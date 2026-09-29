class ResumeService:
    """Handles resume parsing and storage."""

    def parse_resume(self, text: str):
        return {"content": text, "skills": [], "summary": ""}

    def save_resume(self, filename: str, content: str):
        return {"filename": filename, "saved": True, "content_length": len(content)}
