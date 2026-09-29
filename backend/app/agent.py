from app.core.intent import IntentClassifier
from app.services.linkedin_service import LinkedInService
from app.services.llm_service import LLMService


class JarvisAgent:
    """Career assistant with intent-aware routing and LinkedIn-aware guidance."""

    def __init__(self, name: str = "JARVIS"):
        self.name = name
        self.intent_classifier = IntentClassifier()
        self.linkedin = LinkedInService()
        self.llm = LLMService()

    def run(self, *args, **kwargs):
        return {"agent": self.name, "status": "ready", "mode": "voice-first"}

    def process_query(self, query: str):
        text = (query or "").strip()
        if not text:
            response = "I am ready to help. Ask me about jobs, resumes, interviews, LinkedIn, or career planning."
            return {
                "intent": "general",
                "response": response,
                "actions": ["Find AI Jobs", "Analyze a Job", "Prepare Application", "Interview Prep"],
                "linkedin_status": self.linkedin.get_profile_context(),
            }

        intent = self.intent_classifier.classify(text)

        if intent == "job_search":
            response = (
                "I can scan the market for relevant roles, prioritize strong-fit opportunities, "
                "and help you focus on the best next steps for your target job search."
            )
            if "scrum" in text.lower() or "agile" in text.lower():
                response = (
                    "I can help you find Scrum Master and Agile delivery roles, refine your fit, "
                    "and prepare to target the right companies and interview stories."
                )
            actions = ["Find AI Jobs", "Analyze a Job", "Prepare Application"]
        elif intent == "resume":
            response = "I can review your resume against a role, surface missing keywords, and suggest stronger positioning for target jobs."
            actions = ["Update Resume", "Match Skills", "Review ATS Fit"]
        elif intent == "interview":
            response = "I can help you prepare for interviews by practicing strong answers, refining your story, and simulating realistic questions."
            actions = ["Mock Interview", "Answer Prep", "Behavioral Questions"]
        elif intent == "application":
            response = "I can organize your applications, track next steps, and prepare personalized outreach and follow-ups."
            actions = ["Prepare Application", "Track Status", "Write Follow-up"]
        elif intent == "linkedin":
            linkedin_status = self.linkedin.get_profile_context()
            if linkedin_status.get("status") == "oauth_required":
                response = "LinkedIn access is not connected yet. I can still help with job targeting and profile strategy, and we can enable secure OAuth when your credentials are ready."
            else:
                response = "I can use your LinkedIn profile context to tailor outreach, role matching, and career recommendations to your background."
            actions = ["Optimize Profile", "Find Connections", "Tailor Outreach"]
        elif intent == "skill_gap":
            response = "I can identify skill gaps, recommend learning paths, and suggest the fastest way to become competitive for your target roles."
            actions = ["Skill Gap Review", "Learning Plan", "Upskill Roadmap"]
        else:
            response = "I can help with job search strategy, resume alignment, interview coaching, and career planning. Tell me what you want to do next."
            actions = ["Find AI Jobs", "Analyze a Job", "Prepare Application", "Interview Prep"]

        llm_payload = self.llm.generate(f"You are JARVIS, a career assistant. User asks: {text}. Respond with targeted advice and action steps.")
        llm_response = (llm_payload.get("response") or "").strip()
        generic_markers = [
            "i am ready to help with your career goals",
            "i can help with job search strategy",
            "ask me about jobs, resume optimization",
        ]
        if llm_response and not any(marker in llm_response.lower() for marker in generic_markers):
            response = llm_response

        return {
            "intent": intent,
            "response": response,
            "actions": actions,
            "linkedin_status": self.linkedin.get_profile_context(),
            "query": text,
        }
