import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class JobSearchService:
    """Provider-agnostic job search service with Adzuna support and graceful fallback."""

    def __init__(self):
        self.api_key = os.getenv("JOB_SEARCH_API_KEY", "")
        self.provider = os.getenv("JOB_SEARCH_PROVIDER", "").lower()
        self.app_id = os.getenv("JOB_SEARCH_APP_ID", "")

    def is_configured(self):
        return bool(self.api_key and self.provider)

    def search_jobs(self, query: str):
        if not self.is_configured():
            return {
                "status": "not_configured",
                "message": "No job-search provider is configured yet. Add JOB_SEARCH_API_KEY and JOB_SEARCH_PROVIDER to enable live job discovery.",
                "results": [],
            }

        if self.provider == "adzuna":
            params = urlencode({
                "app_id": self.app_id,
                "app_key": self.api_key,
                "what": query,
                "results_per_page": 10,
            })
            url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?{params}"
            try:
                request = Request(url, method="GET")
                with urlopen(request, timeout=20) as response:
                    raw = response.read().decode("utf-8")
                    import json
                    data = json.loads(raw)
                    jobs = data.get("results", [])[:10]
                    return {
                        "status": "ready",
                        "provider": self.provider,
                        "query": query,
                        "results": jobs,
                    }
            except Exception as exc:
                return {
                    "status": "error",
                    "provider": self.provider,
                    "message": f"Live job search request failed: {exc}",
                    "results": [],
                }

        return {
            "status": "ready",
            "provider": self.provider,
            "message": "Job search is configured for a supported provider.",
            "query": query,
            "results": [],
        }
