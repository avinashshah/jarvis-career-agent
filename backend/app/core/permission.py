class PermissionService:
    """Placeholder permission checks for user actions."""

    def can_access(self, user_id: str, resource: str) -> bool:
        return bool(user_id) and bool(resource)
