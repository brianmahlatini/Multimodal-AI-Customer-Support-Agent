class IntentService:
    billing_terms = {"charged", "charge", "invoice", "refund", "billing", "payment", "paid", "duplicate"}
    cancellation_terms = {"cancel", "cancellation", "unsubscribe", "terminate"}
    security_terms = {"password", "login", "hacked", "security", "locked", "reset"}
    technical_terms = {"error", "bug", "broken", "screenshot", "crash", "checkout", "failed"}
    shipping_terms = {"shipping", "delivery", "package", "late", "tracking"}

    negative_terms = {"angry", "upset", "terrible", "charged twice", "fraud", "bad", "cancel", "complaint"}
    positive_terms = {"thanks", "great", "helpful", "resolved", "appreciate"}

    def classify(self, text: str) -> dict[str, str | float]:
        lowered = text.lower()
        intent = self._intent(lowered)
        sentiment = self._sentiment(lowered)
        priority = "high" if sentiment <= -0.5 or intent in {"billing_dispute", "fraud", "security"} else "medium"
        if intent in {"password_reset", "shipping_delay"} and sentiment > -0.4:
            priority = "normal"
        return {"intent": intent, "sentiment": sentiment, "priority": priority}

    def _intent(self, lowered: str) -> str:
        if "fraud" in lowered or "hacked" in lowered:
            return "fraud"
        if any(term in lowered for term in self.cancellation_terms):
            return "cancel_subscription"
        if any(term in lowered for term in self.billing_terms):
            return "billing_dispute"
        if any(term in lowered for term in self.security_terms):
            return "password_reset"
        if any(term in lowered for term in self.technical_terms):
            return "technical_issue"
        if any(term in lowered for term in self.shipping_terms):
            return "shipping_delay"
        return "general_support"

    def _sentiment(self, lowered: str) -> float:
        score = 0.0
        score -= sum(0.25 for term in self.negative_terms if term in lowered)
        score += sum(0.2 for term in self.positive_terms if term in lowered)
        return max(min(round(score, 2), 1.0), -1.0)
