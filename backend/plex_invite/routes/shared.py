from backend.plex_invite.config import ConfigLoader
from backend.plex_invite.config.schema import AppConfig
from backend.plex_invite.core.plex.connection import PlexConnection

config_loader = ConfigLoader()

def get_config():
    """Get configuration with fallback to empty config"""
    try:
        return config_loader.load()
    except FileNotFoundError:
        config = AppConfig(
            plex=None,
            smtp=None,
            admin_email=None
        )
        config_loader.save(config)
        return config

def get_plex_connection():
    """Get Plex connection if configured"""
    config = get_config()
    if config.plex is None:
        return None
    return PlexConnection(config.plex)