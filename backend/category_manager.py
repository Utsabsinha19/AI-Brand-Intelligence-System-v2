class CategoryManager:
    @staticmethod
    def get_relevant_topics():
        return [
            "customer complaint",
            "product feedback",
            "delivery issue",
            "refund problem",
            "pricing concern",
            "customer support issue",
            "product quality review",
            "feature request",
            "service experience",
            "purchase satisfaction"
        ]

    @staticmethod
    def get_noise_topics():
        return [
            "funny meme and viral joke",
            "random unrelated chat and off-topic",
            "spam link, crypto and phishing",
            "engagement bait, like and retweet",
            "political debate and unrelated news",
            "sarcasm without business context",
            "trend hijacking",
            "emoji-only spam"
        ]
