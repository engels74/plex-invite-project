import random
import string
from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator

class AccessKeyConfig(BaseModel):
    """Configuration for access key generation"""
    length: int = Field(default=10, ge=8, le=20, description="Length of the access key")
    valid_days: int = Field(default=30, ge=1, description="Number of days the key is valid")
    max_uses: int = Field(default=1, ge=1, description="Maximum number of uses")
    libraries: list[str] = Field(default_factory=list, description="List of library keys to share")

    @field_validator("libraries")
    def validate_libraries(cls, value: list[str]) -> list[str]:
        """Validate library keys are not empty"""
        if not value:
            raise ValueError("At least one library must be selected")
        return value

class AccessKeyGenerator:
    """Generates random access keys for Plex invitations"""
    
    def __init__(self, config: AccessKeyConfig):
        self.config = config

    def generate_key(self) -> str:
        """Generate a random access key"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(self.config.length))

    def get_expiration_date(self) -> datetime:
        """Calculate expiration date based on valid_days"""
        return datetime.now() + timedelta(days=self.config.valid_days)