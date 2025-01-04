from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class PlexUser(BaseModel):
    """Model representing a Plex user"""
    username: str
    email: Optional[str] = None
    plex_id: str
    access_key: Optional[str] = None
    joined_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True

class UserStats(BaseModel):
    """Statistics about user activity"""
    total_users: int
    active_users: int
    invited_users: int
    last_activity: Optional[datetime] = None