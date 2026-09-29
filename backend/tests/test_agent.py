from app.agent import JarvisAgent
from app.core.memory import MemoryStore
from app.services.job_search_service import JobSearchService
from app.services.linkedin_service import LinkedInService
from app.services.llm_service import LLMService


def test_agent_routes_job_queries():
    agent = JarvisAgent()
    result = agent.process_query("Find AI Developer roles in the last 24 hours")

    assert result["intent"] == "job_search"
    assert "Find AI Jobs" in result["actions"]


def test_llm_service_fallback_works_without_api_key():
    service = LLMService()
    result = service.generate("Help me prepare for a software engineering interview")

    assert "interview" in result["response"].lower() or "help" in result["response"].lower()


def test_linkedin_oauth_url_contains_expected_params():
    service = LinkedInService()
    service.client_id = "abc123"
    service.redirect_uri = "http://localhost:8000/auth/linkedin/callback"

    url = service.build_oauth_url()

    assert "linkedin.com/oauth/v2/authorization" in url
    assert "client_id=abc123" in url
    assert "redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fauth%2Flinkedin%2Fcallback" in url


def test_scrum_master_job_queries_are_treated_as_job_search():
    agent = JarvisAgent()
    result = agent.process_query("search SCRUM master job")

    assert result["intent"] == "job_search"
    assert "Scrum" in result["response"] or "scrum" in result["response"].lower()


def test_job_search_requires_configuration():
    service = JobSearchService()
    result = service.search_jobs("python developer")

    assert result["status"] == "not_configured"


def test_memory_store_persists_profile_data():
    store = MemoryStore(path="backend/.tmp-memory.json")
    store.save_profile({"id": "user-1", "name": "Ava"})

    assert store.get_profile("user-1")["name"] == "Ava"
