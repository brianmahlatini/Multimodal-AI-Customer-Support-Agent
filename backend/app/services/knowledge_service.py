import json
from pathlib import Path


class KnowledgeService:
    def __init__(self) -> None:
        self.knowledge_path = Path(__file__).resolve().parents[1] / "data" / "knowledge_base.json"

    def search(self, intent: str, message: str, limit: int = 3) -> list[dict]:
        documents = json.loads(self.knowledge_path.read_text(encoding="utf-8"))
        terms = set(message.lower().split()) | set(intent.split("_"))
        scored = []
        for document in documents:
            document_terms = set((document["title"] + " " + document["content"]).lower().split())
            score = len(terms & document_terms)
            if intent in document.get("intents", []):
                score += 5
            scored.append({**document, "score": score})
        return sorted(scored, key=lambda item: item["score"], reverse=True)[:limit]
