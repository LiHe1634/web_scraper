from sqlalchemy import Column, Integer, String, DateTime, Boolean, Float
from datetime import datetime

from app.db.base_class import Base

class Proxy(Base):
    __tablename__ = "proxies"

    id = Column(Integer, primary_key=True, index=True)
    host = Column(String, index=True)
    port = Column(Integer)
    protocol = Column(String)  # http, https, socks4, socks5
    username = Column(String, nullable=True)
    password = Column(String, nullable=True)
    
    # Status
    is_active = Column(Boolean, default=True)
    last_checked = Column(DateTime, default=datetime.utcnow)
    last_used = Column(DateTime, nullable=True)
    
    # Performance metrics
    success_count = Column(Integer, default=0)
    failure_count = Column(Integer, default=0)
    average_response_time = Column(Float, default=0.0)
    
    # Metadata
    country = Column(String, nullable=True)
    anonymity = Column(String, nullable=True)  # transparent, anonymous, elite
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def url(self):
        auth = f"{self.username}:{self.password}@" if self.username and self.password else ""
        return f"{self.protocol}://{auth}{self.host}:{self.port}"
