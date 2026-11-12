from app.services.intent_service import IntentService


def test_detects_billing_dispute_and_negative_sentiment() -> None:
    result = IntentService().classify("I was charged twice and this is terrible")

    assert result["intent"] == "billing_dispute"
    assert result["sentiment"] < 0
    assert result["priority"] == "high"


def test_detects_password_reset() -> None:
    result = IntentService().classify("Please help me reset my password")

    assert result["intent"] == "password_reset"
    assert result["priority"] == "normal"
