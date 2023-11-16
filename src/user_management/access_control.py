import logging

class AccessControlManager:

    def __init__(self, user_role_repository, permission_repository):
        self.logger = logging.getLogger(__name__)
        self.user_role_repository = user_role_repository
        self.permission_repository = permission_repository

    def has_permission(self, user_id, resource, action):
        try:
            # Retrieve the user's roles
            user_roles = self.user_role_repository.get_user_roles(user_id)

            # Check if any of the user's roles have the required permission
            for role in user_roles:
                role_permissions = self.permission_repository.get_role_permissions(role.id)
                if (resource, action) in role_permissions:
                    return True

            return False
        except Exception as e:
            self.logger.error(f'Failed to check permission for user {user_id}:', e)
            return False
