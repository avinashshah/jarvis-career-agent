# JARVIS Career Agent

A voice-first AI career assistant with a FastAPI backend, a dashboard UI, secure OAuth hooks, live job-search integration placeholders, and persistent profile memory.

## Structure

- `backend/` - FastAPI app and services
- `frontend/` - static UI
- `backend/resumes/` - resume files

## Run backend

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --app-dir .
```

## Required environment variables

Set these in `backend/.env` before using live authentication and provider integrations:

```env
OPENAI_API_KEY=your_openai_api_key_here
APP_ENV=development
DATABASE_URL=sqlite:///./jarvis.db

LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_REDIRECT_URI=http://localhost:8000/api/auth/linkedin/callback

JOB_SEARCH_PROVIDER=
JOB_SEARCH_API_KEY=
```

## Features

- LinkedIn OAuth route at `/api/auth/linkedin`
- Callback route at `/api/auth/linkedin/callback`
- Job search route at `/api/jobs/search`
- Profile save and retrieval routes at `/api/profile/save` and `/api/profile/{user_id}`
- Persistent memory support via `backend/memory.json`
- Voice-first web UI for career assistant interactions

## Important note

Use OAuth and provider credentials only through official developer dashboards. Do not share personal LinkedIn email/password in code, scripts, or chat.
