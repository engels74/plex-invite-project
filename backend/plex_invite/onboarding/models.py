from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class OnboardingStep(BaseModel):
    """A single step in the onboarding process"""
    title: str
    content: str
    requires_confirmation: bool = Field(default=False, description="Whether user must confirm understanding")
    confirmation_text: Optional[str] = Field(None, description="Text for confirmation checkbox")

class OnboardingPage(BaseModel):
    """A complete onboarding page with multiple steps"""
    id: str
    title: str
    description: Optional[str] = None
    steps: List[OnboardingStep]
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    is_active: bool = True