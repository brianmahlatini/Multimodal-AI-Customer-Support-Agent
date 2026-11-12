class MockOpenAIService:
    """Deterministic provider used until live OpenAI credentials are configured."""

    def transcribe(self, filename: str) -> str:
        return f"Transcribed customer voice note from {filename}: customer needs urgent support."

    def recommend_resolution(self, message: str, intent: str, account: dict, knowledge: list[dict]) -> dict:
        top_policy = knowledge[0]["title"] if knowledge else "standard support policy"
        if intent == "billing_dispute":
            recommendation = (
                f"Apologize, verify invoices for {account['email']}, check duplicate payment records, "
                "and offer a billing-specialist review before refund action."
            )
            confidence = 0.72
        elif intent == "password_reset":
            recommendation = "Send the secure password reset flow and confirm multi-factor authentication status."
            confidence = 0.86
        elif intent == "technical_issue":
            recommendation = "Collect browser, device, screenshot, and reproduction steps, then route to product support."
            confidence = 0.76
        else:
            recommendation = f"Use {top_policy} and respond with a concise next step."
            confidence = 0.7
        return {"recommendation": recommendation, "confidence": confidence}
