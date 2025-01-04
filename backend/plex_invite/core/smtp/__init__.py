"""SMTP Integration Module"""
from .config import SMTPConfig
from .sender import SMTPSender

__all__ = ["SMTPConfig", "SMTPSender"]