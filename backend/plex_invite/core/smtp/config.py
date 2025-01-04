from pydantic import BaseModel, Field, field_validator

class SMTPConfig(BaseModel):
    """Configuration model for SMTP server"""
    host: str = Field(..., description="SMTP server host")
    port: int = Field(default=587, description="SMTP server port")
    username: str = Field(..., description="SMTP username")
    password: str = Field(..., description="SMTP password")
    use_tls: bool = Field(default=True, description="Use TLS encryption")
    from_email: str = Field(..., description="Sender email address")
    timeout: int = Field(default=10, description="Connection timeout in seconds")

    @field_validator("host")
    def validate_host(cls, value: str) -> str:
        """Validate SMTP host"""
        value = value.strip()
        if not value:
            raise ValueError("SMTP host cannot be empty")
        return value

    @field_validator("port")
    def validate_port(cls, value: int) -> int:
        """Validate SMTP port"""
        if not 1 <= value <= 65535:
            raise ValueError("Port must be between 1 and 65535")
        return value

    @field_validator("from_email")
    def validate_from_email(cls, value: str) -> str:
        """Validate sender email address"""
        if "@" not in value:
            raise ValueError("Invalid email address format")
        return value.strip()