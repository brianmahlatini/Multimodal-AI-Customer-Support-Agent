from langgraph.graph import END, StateGraph

from app.agents.nodes import (
    account_node,
    handover_node,
    intake_node,
    resolution_node,
    retrieval_node,
    transcription_node,
    understanding_node,
)
from app.agents.state import SupportState
from app.schemas.case import CaseCreateRequest


def build_support_graph():
    graph = StateGraph(SupportState)
    graph.add_node("intake", intake_node)
    graph.add_node("transcription", transcription_node)
    graph.add_node("understanding", understanding_node)
    graph.add_node("account", account_node)
    graph.add_node("retrieval", retrieval_node)
    graph.add_node("resolution", resolution_node)
    graph.add_node("handover", handover_node)

    graph.set_entry_point("intake")
    graph.add_edge("intake", "transcription")
    graph.add_edge("transcription", "understanding")
    graph.add_edge("understanding", "account")
    graph.add_edge("account", "retrieval")
    graph.add_edge("retrieval", "resolution")
    graph.add_edge("resolution", "handover")
    graph.add_edge("handover", END)
    return graph.compile()


def run_support_graph(request: CaseCreateRequest) -> SupportState:
    return build_support_graph().invoke({"request": request})
