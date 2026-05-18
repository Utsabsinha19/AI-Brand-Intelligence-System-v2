class ThresholdManager:
    HIGH_RELEVANCE = 0.80
    MEDIUM_RELEVANCE = 0.60
    LOW_RELEVANCE = 0.40

    @classmethod
    def get_decision(cls, score: float) -> str:
        if score >= cls.HIGH_RELEVANCE:
            return "Highly Relevant"
        elif score >= cls.MEDIUM_RELEVANCE:
            return "Medium Relevance"
        elif score >= cls.LOW_RELEVANCE:
            return "Low Relevance"
        return "Ignore"
