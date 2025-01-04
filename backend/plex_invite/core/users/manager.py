from typing import Dict, List, Optional
from .models import PlexUser, UserStats
from ..plex.connection import PlexConnection

class UserManager:
    """Manages tracking and operations on Plex users"""
    
    def __init__(self, plex_connection: PlexConnection):
        self.connection = plex_connection
        self._users: Dict[str, PlexUser] = {}

    def sync_users(self) -> None:
        """Sync users from Plex server"""
        try:
            plex_users = self.connection.server.myPlexAccount().users()
            for plex_user in plex_users:
                if plex_user and hasattr(plex_user, 'title') and hasattr(plex_user, 'email'):
                    user = PlexUser(
                        username=plex_user.title,
                        email=plex_user.email,
                        plex_id=str(plex_user.id)
                    )
                    self._users[str(plex_user.id)] = user
        except Exception as e:
            raise RuntimeError(f"Failed to sync users: {str(e)}")

    def get_user(self, user_id: str) -> Optional[PlexUser]:
        """Get a user by their Plex ID"""
        return self._users.get(user_id)

    def get_users(self) -> List[PlexUser]:
        """Get all tracked users"""
        return list(self._users.values())

    def get_user_stats(self) -> UserStats:
        """Get statistics about users"""
        users = self.get_users()
        return UserStats(
            total_users=len(users),
            active_users=sum(1 for u in users if u.is_active),
            invited_users=sum(1 for u in users if u.access_key is not None),
            last_activity=max((u.joined_at for u in users), default=None)
        )

    def assign_access_key(self, user_id: str, access_key: str) -> None:
        """Assign an access key to a user"""
        if user := self.get_user(user_id):
            user.access_key = access_key

    def remove_access_key(self, user_id: str) -> None:
        """Remove access key from a user"""
        if user := self.get_user(user_id):
            user.access_key = None