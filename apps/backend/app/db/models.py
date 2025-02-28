# app/db/models.py
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    username = sa.Column(sa.String, unique=True, index=True, nullable=False)
    password = sa.Column(sa.String, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)

class Session(Base):
    __tablename__ = "sessions"
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    session_id = sa.Column(sa.String, unique=True, index=True, nullable=False)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)
    expires_at = sa.Column(sa.DateTime, nullable=False)

class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = sa.Column(sa.Integer, primary_key=True, index=True)
    user_id = sa.Column(sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    role_name = sa.Column(sa.String, nullable=False)
    jobs_count = sa.Column(sa.Integer, default=0, nullable=False)
    created_at = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)