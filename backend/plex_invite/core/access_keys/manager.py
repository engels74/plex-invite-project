from datetime import datetime, timedelta
from typing import Dict, Optional
from pydantic import BaseModel, Field
from .generator import AccessKeyConfig, AccessKeyGenerator

class AccessKeyRecord(BaseModel):
    """Record of a generated access key"""
    key: str
    config: AccessKeyConfig
    created_at: datetime = Field(default_factory=datetime.now)
    uses: int = 0
    is_active: bool = True

class AccessKeyManager:
    """Manages storage and validation of access keys"""
    
    def __init__(self):
        self._keys: Dict[str, AccessKeyRecord] = {}

    def create_key(self, config: AccessKeyConfig) -> AccessKeyRecord:
        """Create and store a new access key"""
        generator = AccessKeyGenerator(config)
        key = generator.generate_key()
        record = AccessKeyRecord(key=key, config=config)
        self._keys[key] = record
        return record

    def get_key(self, key: str) -> Optional[AccessKeyRecord]:
        """Retrieve an access key record"""
        return self._keys.get(key)

    def validate_key(self, key: str) -> bool:
        """Validate if a key is still valid"""
        record = self.get_key(key)
        if not record or not record.is_active:
            return False
        
        # Check expiration
        expiration = record.created_at + timedelta(days=record.config.valid_days)
        if datetime.now() > expiration:
            return False
            
        # Check usage limit
        if record.uses >= record.config.max_uses:
            return False
            
        return True

    def deactivate_key(self, key: str) -> None:
        """Deactivate an access key"""
        if record := self.get_key(key):
            record.is_active = False

    def increment_usage(self, key: str) -> None:
        """Increment usage count for a key"""
        if record := self.get_key(key):
            record.uses += 1