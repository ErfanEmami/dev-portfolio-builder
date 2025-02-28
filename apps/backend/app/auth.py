# app/auth.py
import bcrypt
from fastapi import HTTPException, status
from sqlalchemy import select
from datetime import datetime
from app.db.models import User, Session

# Password hashing functions
def hash_password(password: str) -> str:
    """Hash a password for storing."""
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a stored password against one provided by user."""
    return bcrypt.checkpw(
        plain_password.encode('utf-8'),
        hashed_password.encode('utf-8')
    )

# Get current user from session
async def get_current_user(db, session_id: str):
    """Get the current user from a session ID."""
    if not session_id:
        return None
    
    # Get the session
    stmt = (
        select(Session)
        .where(Session.session_id == session_id)
        .where(Session.expires_at > datetime.utcnow())
    )
    result = await db.execute(stmt)
    session = result.scalars().first()
    
    if not session:
        return None
    
    # Get the user
    stmt = select(User).where(User.id == session.user_id)
    result = await db.execute(stmt)
    user = result.scalars().first()
    
    return user