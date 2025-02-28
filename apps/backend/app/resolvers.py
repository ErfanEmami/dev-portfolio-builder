import strawberry
from app.models import User
from app.database import SessionLocal

@strawberry.type
class Query:
    @strawberry.field
    def get_user(self, user_id: int) -> User:
        db = SessionLocal()
        user = db.query(User).filter(User.id == user_id).first()
        return user
