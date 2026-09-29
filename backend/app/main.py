from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.agent import JarvisAgent
from app.core.memory import MemoryStore
from app.models.schemas import QueryRequest
from app.services.job_search_service import JobSearchService
from app.services.linkedin_service import LinkedInService

app = FastAPI(title="JARVIS Career Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

jarvis = JarvisAgent()
memory = MemoryStore(path="backend/memory.json")
linkedin = LinkedInService()
job_search = JobSearchService()


@app.get("/")
def read_root():
    return {"message": "JARVIS Career Agent is running", "status": "online"}


@app.get("/api/auth/linkedin")
def linkedin_auth():
    if not linkedin.client_id or not linkedin.redirect_uri:
        raise HTTPException(status_code=400, detail="LinkedIn OAuth is not configured.")
    return {"oauth_url": linkedin.build_oauth_url()}


@app.get("/api/auth/linkedin/callback")
def linkedin_callback(code: str = Query(...), state: str = Query("jarvis-career-agent")):
    if not code:
        raise HTTPException(status_code=400, detail="Missing authorization code.")

    token_exchange = linkedin.exchange_code_for_token(code)
    return {
        "status": token_exchange.get("status", "unknown"),
        "state": state,
        "message": token_exchange.get("message", "LinkedIn OAuth callback received."),
        "token": token_exchange.get("token"),
        "code": code,
    }


@app.post("/api/assistant/query")
def process_query(payload: QueryRequest):
    return jarvis.process_query(payload.query)


@app.post("/api/jobs/search")
def search_jobs(payload: QueryRequest):
    result = job_search.search_jobs(payload.query)
    return result


@app.post("/api/profile/save")
def save_profile(payload: dict):
    profile = memory.save_profile(payload)
    return {"status": "saved", "profile": profile}


@app.post("/api/profile/session")
def save_session(payload: dict):
    user_id = payload.get("user_id", "anonymous")
    session = memory.save_session(user_id, payload)
    return {"status": "saved", "session": session}


@app.get("/api/profile/{user_id}")
def get_profile(user_id: str):
    profile = memory.get_profile(user_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@app.get("/api/session/{user_id}")
def get_session(user_id: str):
    session = memory.get_session(user_id)
    return session
