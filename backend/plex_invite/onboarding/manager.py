from pathlib import Path
from typing import Dict, List, Optional
import yaml
from .models import OnboardingPage

class OnboardingManager:
    """Manages storage and retrieval of onboarding pages"""
    
    def __init__(self, storage_path: str = "onboarding_pages"):
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        self._pages: Dict[str, OnboardingPage] = {}
        self._load_existing_pages()

    def _load_existing_pages(self) -> None:
        """Load existing onboarding pages from storage"""
        for page_file in self.storage_path.glob("*.yml"):
            try:
                with open(page_file, 'r') as f:
                    page_data = yaml.safe_load(f)
                    page = OnboardingPage(**page_data)
                    self._pages[page.id] = page
            except Exception:
                continue

    def create_page(self, page: OnboardingPage) -> None:
        """Create a new onboarding page"""
        self._pages[page.id] = page
        self._save_page(page)

    def update_page(self, page_id: str, updated_page: OnboardingPage) -> None:
        """Update an existing onboarding page"""
        if page_id not in self._pages:
            raise ValueError(f"Page with ID {page_id} not found")
        self._pages[page_id] = updated_page
        self._save_page(updated_page)

    def get_page(self, page_id: str) -> Optional[OnboardingPage]:
        """Get an onboarding page by ID"""
        return self._pages.get(page_id)

    def list_pages(self) -> List[OnboardingPage]:
        """List all onboarding pages"""
        return list(self._pages.values())

    def delete_page(self, page_id: str) -> None:
        """Delete an onboarding page"""
        if page_id in self._pages:
            page_file = self.storage_path / f"{page_id}.yml"
            page_file.unlink(missing_ok=True)
            del self._pages[page_id]

    def _save_page(self, page: OnboardingPage) -> None:
        """Save a page to storage"""
        page_file = self.storage_path / f"{page.id}.yml"
        with open(page_file, 'w') as f:
            yaml.safe_dump(page.model_dump(), f)