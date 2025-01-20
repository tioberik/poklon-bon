from .database import Base
from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

def end_of_year():
    today = datetime.now(timezone.utc)
    return datetime(today.year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

class PoklonBon(Base):
    __tablename__ = 'poklon-bonovi'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    barcode = Column(String(50), unique=True, nullable=False)
    value = Column(DECIMAL(10, 2), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    expires_at = Column(DateTime, nullable=False, default=end_of_year)
    status = Column(String(20), default="active")
    user_id = Column(Integer, ForeignKey("users.id"))
    customer_name = Column(String(100), nullable=True)  # Opciono ime kupca

    creator = relationship("User", back_populates="bonovi")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(150), nullable=False)

    bonovi = relationship("PoklonBon", back_populates="creator")
