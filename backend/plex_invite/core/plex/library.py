from typing import List, Optional
from plexapi.library import LibrarySection
from pydantic import BaseModel

class PlexLibraryInfo(BaseModel):
    """Model representing Plex library information"""
    title: str
    type: str
    key: str
    size: int

class PlexLibraryManager:
    """Manages operations related to Plex libraries"""
    
    def __init__(self, connection):
        self.connection = connection

    def get_libraries(self) -> List[PlexLibraryInfo]:
        """Get all available libraries from Plex server"""
        try:
            libraries = self.connection.server.library.sections()
            return [
                PlexLibraryInfo(
                    title=lib.title,
                    type=lib.type,
                    key=lib.key,
                    size=lib.totalSize
                )
                for lib in libraries
            ]
        except Exception as e:
            raise RuntimeError(f"Failed to retrieve libraries: {str(e)}")

    def get_library_by_key(self, key: str) -> Optional[LibrarySection]:
        """Get a specific library by its key"""
        try:
            return self.connection.server.library.sectionByID(key)
        except Exception:
            return None

    def get_library_by_title(self, title: str) -> Optional[LibrarySection]:
        """Get a specific library by its title"""
        try:
            return self.connection.server.library.section(title)
        except Exception:
            return None