class JobService:
    """Handles job-related workflows."""

    def get_jobs(self):
        return []

    def match_job(self, resume_text: str, job_description: str):
        return {
            "resume_text": resume_text,
            "job_description": job_description,
            "match_score": 0.0,
            "recommendations": [],
        }
