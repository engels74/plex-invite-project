from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, JSON, DateTime
from sqlalchemy.orm import relationship
from backend.plex_invite.core.database.base import Base

class SetupState(Base):
    __tablename__ = "setup_state"
    
    id = Column(Integer, primary_key=True, index=True)
    admin_created = Column(Boolean, default=False)
    plex_configured = Column(Boolean, default=False)
    smtp_configured = Column(Boolean, default=False)
    setup_complete = Column(Boolean, default=False)
    completed_at = Column(DateTime)

class AdminUser(Base):
    __tablename__ = "admin_user"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

class AccessKey(Base):
    __tablename__ = "access_keys"
    
    id = Column(Integer, primary_key=True, index=True)
    key = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    valid_until = Column(DateTime)
    max_uses = Column(Integer)
    use_count = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    plex_libraries = Column(JSON)
    
    invitations = relationship("Invitation", back_populates="access_key")

class Invitation(Base):
    __tablename__ = "invitations"
    
    id = Column(Integer, primary_key=True, index=True)
    access_key_id = Column(Integer, ForeignKey("access_keys.id"))
    invited_email = Column(String)
    invited_at = Column(DateTime, default=datetime.utcnow)
    accepted_at = Column(DateTime)
    status = Column(String, default="pending")
    
    access_key = relationship("AccessKey", back_populates="invitations")

class PlexUser(Base):
    __tablename__ = "plex_users"
    
    id = Column(Integer, primary_key=True, index=True)
    plex_id = Column(String, unique=True)
    plex_username = Column(String)
    access_key_id = Column(Integer, ForeignKey("access_keys.id"))
    added_at = Column(DateTime, default=datetime.utcnow)