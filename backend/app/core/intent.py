class IntentClassifier:
    """Basic but practical intent classification for career guidance."""

    def classify(self, text: str):
        text = (text or "").lower()

        if any(k in text for k in ["linkedin", "profile", "network", "connection", "recruiter"]):
            return "linkedin"
        if any(k in text for k in ["resume", "cv", "ats", "keywords", "profile summary", "resume review"]):
            return "resume"
        if any(k in text for k in ["scrum", "agile", "job", "role", "opportunity", "hiring", "positions", "search"]):
            return "job_search"
        if any(k in text for k in ["application", "apply", "follow up", "outreach", "track"]):
            return "application"
        if any(k in text for k in ["interview", "mock", "prep", "behavioral", "technical"]):
            return "interview"
        if any(k in text for k in ["skill", "learning", "gap", "upskill", "training"]):
            return "skill_gap"
        return "general"
