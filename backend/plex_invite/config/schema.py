from pydantic import BaseModel, Field
from typing import Optional
from ..core.plex.connection import PlexConnectionConfig
from ..core.smtp.config import SMTPConfig

class AccessKeyDefaults(BaseModel):
    """Default settings for access keys"""
    valid_days: int = Field(default=30, description="Default validity period in days")
    max_uses: int = Field(default=1, description="Default maximum uses")
    default_libraries: list[str] = Field(default_factory=list, description="Default libraries to share")

class AppConfig(BaseModel):
    """Main application configuration"""
    plex: Optional[PlexConnectionConfig] = Field(None, description="Plex server configuration")
    smtp: Optional[SMTPConfig] = Field(None, description="SMTP email configuration")
    access_key_defaults: AccessKeyDefaults = Field(default_factory=AccessKeyDefaults)
    admin_email: Optional[str] = Field(None, description="Admin email for notifications")
    invitation_url_base: str = Field(
        default="https://clients.plex.tv/servers/shared_servers/accept",
        description="Base URL for invitation links"
    )

    def is_initial_setup_complete(self) -> bool:
        """Check if required configurations are present"""
        return self.plex is not None and self.smtp is not None