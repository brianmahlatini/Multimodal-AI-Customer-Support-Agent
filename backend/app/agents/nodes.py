from app.agents.state import SupportState
from app.services.account_service import AccountService
from app.services.intent_service import IntentService
from app.services.knowledge_service import KnowledgeService
from app.services.openai_service import MockOpenAIService


def intake_node(state: SupportState) -> SupportState:
    request = state["request"]
    state["normalized_message"] = request.message.strip()
    state["audit_trail"] = [{"node": "intake", "event": "case_normalized"}]
    return state


def transcription_node(state: SupportState) -> SupportState:
    request = state["request"]
    audio_files = [item for item in request.attachments if item.content_type.startswith("audio/")]
    if audio_files:
        transcript = MockOpenAIService().transcribe(audio_files[0].filename)
        state["transcript"] = transcript
        state["normalized_message"] = f"{state['normalized_message']}\n{transcript}".strip()
    state["audit_trail"].append({"node": "transcription", "event": "audio_checked", "audio_files": len(audio_files)})
    return state


def understanding_node(state: SupportState) -> SupportState:
    result = IntentService().classify(state["normalized_message"])
    state.update(result)
    state["audit_trail"].append({"node": "understanding", "event": "intent_sentiment_detected"})
    return state


def account_node(state: SupportState) -> SupportState:
    state["account"] = AccountService().get_account(state["request"].customer_id)
    state["audit_trail"].append({"node": "account", "event": "account_loaded"})
    return state


def retrieval_node(state: SupportState) -> SupportState:
    state["knowledge"] = KnowledgeService().search(state["intent"], state["normalized_message"])
    state["audit_trail"].append({"node": "retrieval", "event": "knowledge_retrieved"})
    return state


def resolution_node(state: SupportState) -> SupportState:
    result = MockOpenAIService().recommend_resolution(
        message=state["normalized_message"],
        intent=state["intent"],
        account=state["account"],
        knowledge=state["knowledge"],
    )
    state["recommendation"] = result["recommendation"]
    state["confidence"] = result["confidence"]
    state["audit_trail"].append({"node": "resolution", "event": "resolution_recommended"})
    return state


def handover_node(state: SupportState) -> SupportState:
    risky_intents = {"billing_dispute", "cancel_subscription", "fraud", "security", "legal"}
    asks_for_human = "human" in state["normalized_message"].lower() or "agent" in state["normalized_message"].lower()
    account_risk = state["account"].get("account_status") in {"suspended", "delinquent", "under_review"}
    sentiment_risk = state["sentiment"] <= -0.55
    confidence_risk = state["confidence"] < 0.68

    state["handover_required"] = (
        state["intent"] in risky_intents or asks_for_human or account_risk or sentiment_risk or confidence_risk
    )
    if state["handover_required"]:
        state["handover_reason"] = "Escalation policy matched for sentiment, intent, account risk, or confidence."
    else:
        state["handover_reason"] = "Automated recommendation is within policy."
    state["ticket_subject"] = f"{state['intent'].replace('_', ' ').title()} - {state['request'].customer_id}"
    state["audit_trail"].append({"node": "handover", "event": "handover_policy_evaluated"})
    return state
