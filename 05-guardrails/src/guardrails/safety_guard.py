class SafetyGuard:
    def enforce(self, output: str):
        lowered = output.lower()

        unsafe_patterns = [
            "as an ai model i was instructed",
            "system prompt",
            "ignore previous instructions"
        ]

        for p in unsafe_patterns:
            if p in lowered:
                return False, "instruction_leak"

        if "i don't know" in lowered or "cannot determine" in lowered:
            return True, "safe_refusal"

        return True, "ok"

# TODO: Add more guardrails -This evolves into ML / LLM-based guards later - Simple heuristics on purpose