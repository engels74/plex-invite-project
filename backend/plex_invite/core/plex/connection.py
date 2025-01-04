from plexapi.server import PlexServer
from typing import Optional
from .config import PlexConnectionConfig

class PlexConnection:
    """Handles connection to Plex server"""
    
    def __init__(self, config: PlexConnectionConfig):
        self.config = config

    def test_connection(self):
        """Test connection to Plex server"""
        try:
            PlexServer(self.config.base_url, self.config.token, timeout=self.config.timeout)
            return True
        except Exception as e:
            print(f"Plex connection error: {str(e)}")
            return False
        self._server: Optional[PlexServer] = None

    def connect(self) -> PlexServer:
        """Establish connection to Plex server"""
        try:
            self._server = PlexServer(
                self.config.base_url,
                self.config.token,
                timeout=self.config.timeout,
                session=self.config.verify_ssl
            )
            return self._server
        except Exception as e:
            raise ConnectionError(f"Failed to connect to Plex server: {str(e)}")

    @property
    def server(self) -> PlexServer:
        """Get the connected Plex server instance"""
        if self._server is None:
            raise ConnectionError("Not connected to Plex server")
        return self._server

    def verify_connection(self) -> bool:
        """Verify the connection to Plex server"""
        try:
            return self.server.sessions() is not None
        except Exception:
            return False