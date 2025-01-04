from pydantic import BaseModel, Field, field_validator

class PlexConnectionConfig(BaseModel):
    """Configuration model for Plex server connection"""
    base_url: str = Field(..., description="Base URL of the Plex server")
    token: str = Field(..., description="Authentication token for the Plex server")
    timeout: int = Field(default=30, description="Connection timeout in seconds")
    verify_ssl: bool = Field(default=True, description="Verify SSL certificates")

    @field_validator("base_url")
    def validate_base_url(cls, value: str) -> str:
        """Validate and normalize the base URL"""
        value = value.strip("/")
        if not value.startswith(("http://", "https://")):
            raise ValueError("Base URL must start with http:// or https://")
        return value