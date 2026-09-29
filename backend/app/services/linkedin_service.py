import json
import os
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class LinkedInService:
    """LinkedIn OAuth and profile access helper."""

    def __init__(self):
        self.client_id = os.getenv("LINKEDIN_CLIENT_ID", "")
        self.client_secret = os.getenv("LINKEDIN_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("LINKEDIN_REDIRECT_URI", "")
        self.scope = "r_liteprofile r_emailaddress w_member_social"

    def is_configured(self) -> bool:
        return bool(self.client_id and self.client_secret and self.redirect_uri)

    def build_oauth_url(self):
        params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scope": self.scope,
            "state": "jarvis-career-agent",
        }
        return "https://www.linkedin.com/oauth/v2/authorization?" + urlencode(params)

    def exchange_code_for_token(self, code: str):
        if not self.is_configured():
            return {
                "status": "not_configured",
                "message": "LinkedIn OAuth is not configured. Add client_id, client_secret, and redirect_uri.",
            }

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        data = urlencode(payload).encode("utf-8")
        request = Request(
            "https://www.linkedin.com/oauth/v2/accessToken",
            data=data,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            method="POST",
        )

        try:
            with urlopen(request, timeout=20) as response:
                body = response.read().decode("utf-8")
                token_data = json.loads(body)
                return {"status": "success", "token": token_data}
        except Exception as exc:
            return {
                "status": "error",
                "message": f"LinkedIn token exchange failed: {exc}",
            }

    def get_profile_context(self):
        if not self.is_configured():
            return {
                "status": "oauth_required",
                "message": "LinkedIn OAuth is not configured yet. Add your app credentials to enable secure profile access.",
                "oauth_url": self.build_oauth_url() if self.client_id and self.redirect_uri else None,
            }
        return {
            "status": "ready",
            "message": "LinkedIn access is configured and ready for profile-aware job assistance.",
            "oauth_url": self.build_oauth_url(),
        }
