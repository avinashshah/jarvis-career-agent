from pydantic import BaseModel


class ResumeUpload(BaseModel):
    filename: str
    content: str = ""


class JobMatchRequest(BaseModel):
    resume_text: str
    job_description: str


class ApplicationCreate(BaseModel):
    job_title: str
    company: str


class QueryRequest(BaseModel):
    query: str
