class ApplicationService:
    """Handles application tracking."""

    def create_application(self, job_title: str, company: str):
        return {"job_title": job_title, "company": company, "status": "draft"}
