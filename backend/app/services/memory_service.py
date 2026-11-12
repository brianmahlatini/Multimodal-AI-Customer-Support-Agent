class MemoryService:
    def __init__(self) -> None:
        self._memory: dict[str, list[dict]] = {}

    def append(self, customer_id: str, item: dict) -> None:
        self._memory.setdefault(customer_id, []).append(item)

    def recent(self, customer_id: str, limit: int = 5) -> list[dict]:
        return self._memory.get(customer_id, [])[-limit:]
