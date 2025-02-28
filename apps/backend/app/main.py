# app/main.py
import strawberry
import sqlalchemy
from fastapi import FastAPI, Depends, HTTPException, status, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
import uuid
from datetime import datetime, timedelta

from app.db.database import get_db
from app.db.models import User, Session, Portfolio
from app.schemas import UserCreate, LoginData, PortfolioCreate
from app.auth import get_current_user, hash_password, verify_password

# Create FastAPI app
app = FastAPI(title="Portfolio API", description="Backend API for portfolio management")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Vite default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQL types
@strawberry.type
class UserType:
    id: int
    username: str
    created_at: datetime

@strawberry.type
class PortfolioType:
    id: int
    user_id: int
    role_name: str
    jobs_count: int
    created_at: datetime

@strawberry.type
class AuthPayload:
    success: bool
    message: str
    user: Optional[UserType] = None

@strawberry.input
class UserCreateInput:
    username: str
    password: str

@strawberry.input
class LoginInput:
    username: str
    password: str

@strawberry.input
class PortfolioCreateInput:
    role_name: str
    jobs_count: int

# GraphQL queries
@strawberry.type
class Query:
    @strawberry.field
    async def check_auth(self, info) -> AuthPayload:
        session_id = info.context["session_id"]

        if not session_id:
            return AuthPayload(success=False, message="Not authenticated")
        
        db = info.context["db"]
        current_user = await get_current_user(db, session_id)
        if not current_user:
            return AuthPayload(success=False, message="Invalid or expired session")
        
        return AuthPayload(
            success=True,
            message="Authenticated",
            user=UserType(
                id=current_user.id,
                username=current_user.username,
                created_at=current_user.created_at
            )
        )
    
    @strawberry.field
    async def get_portfolios(self, info) -> List[PortfolioType]:
        session_id = info.context["session_id"]
        db = info.context["db"]

        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        current_user = await get_current_user(db, session_id)
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        # Query for user's portfolios
        stmt = (
            sqlalchemy.select(Portfolio)
            .where(Portfolio.user_id == current_user.id)
            .order_by(Portfolio.created_at.desc())
        )
        result = await db.execute(stmt)
        portfolios = result.scalars().all()
        
        return [
            PortfolioType(
                id=portfolio.id,
                user_id=portfolio.user_id,
                role_name=portfolio.role_name,
                jobs_count=portfolio.jobs_count,
                created_at=portfolio.created_at
            )
            for portfolio in portfolios
        ]

# GraphQL mutations
@strawberry.type
class Mutation:
    @strawberry.mutation
    async def signup(self, info, user_data: UserCreateInput) -> AuthPayload:
        db = info.context["db"]
        
        # Check if username already exists
        stmt = sqlalchemy.select(User).where(User.username == user_data.username)
        result = await db.execute(stmt)
        existing_user = result.scalars().first()
        
        if existing_user:
            return AuthPayload(
                success=False,
                message="Username already exists"
            )
        
        # Create new user
        hashed_password = hash_password(user_data.password)
        new_user = User(
            username=user_data.username,
            password=hashed_password
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        
        # Create session
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        new_session = Session(
            session_id=session_id,
            user_id=new_user.id,
            expires_at=expires_at
        )
        db.add(new_session)
        await db.commit()
        
        # Set cookie in context for response
        info.context["response"].set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=7 * 24 * 60 * 60,  # 7 days
            samesite="lax",
            secure=False,  # Set to True in production with HTTPS
        )
        
        return AuthPayload(
            success=True,
            message="User created successfully",
            user=UserType(
                id=new_user.id,
                username=new_user.username,
                created_at=new_user.created_at
            )
        )
    
    @strawberry.mutation
    async def login(self, info, login_data: LoginInput) -> AuthPayload:
        db = info.context["db"]
        
        # Find user
        stmt = sqlalchemy.select(User).where(User.username == login_data.username)
        result = await db.execute(stmt)
        user = result.scalars().first()
        
        if not user or not verify_password(login_data.password, user.password):
            return AuthPayload(
                success=False,
                message="Invalid username or password"
            )
        
        # Create new session
        session_id = str(uuid.uuid4())
        expires_at = datetime.utcnow() + timedelta(days=7)
        
        new_session = Session(
            session_id=session_id,
            user_id=user.id,
            expires_at=expires_at
        )
        db.add(new_session)
        await db.commit()
        
        # Set cookie in context for response
        info.context["response"].set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            max_age=7 * 24 * 60 * 60,  # 7 days
            samesite="lax",
            secure=False,  # Set to True in production with HTTPS
        )
        
        return AuthPayload(
            success=True,
            message="Login successful",
            user=UserType(
                id=user.id,
                username=user.username,
                created_at=user.created_at
            )
        )
    
    @strawberry.mutation
    async def logout(self, info) -> AuthPayload:
        session_id = info.context["session_id"]

        if not session_id:
            return AuthPayload(success=False, message="Not authenticated")
        
        db = info.context["db"]
        
        # Delete session from database
        stmt = sqlalchemy.delete(Session).where(Session.session_id == session_id)
        await db.execute(stmt)
        await db.commit()
        
        # Clear cookie
        info.context["response"].delete_cookie(key="session_id")
        
        return AuthPayload(
            success=True,
            message="Logged out successfully"
        )
    
    @strawberry.mutation
    async def create_portfolio(self, info, portfolio_data: PortfolioCreateInput) -> PortfolioType:
        session_id = info.context["session_id"]
        db = info.context["db"]
        
        if not session_id:
            raise HTTPException(status_code=401, detail="Not authenticated")
        
        current_user = await get_current_user(db, session_id)
        if not current_user:
            raise HTTPException(status_code=401, detail="Invalid or expired session")
        
        # Create new portfolio
        new_portfolio = Portfolio(
            user_id=current_user.id,
            role_name=portfolio_data.role_name,
            jobs_count=portfolio_data.jobs_count
        )
        db.add(new_portfolio)
        await db.commit()
        await db.refresh(new_portfolio)
        
        return PortfolioType(
            id=new_portfolio.id,
            user_id=new_portfolio.user_id,
            role_name=new_portfolio.role_name,
            jobs_count=new_portfolio.jobs_count,
            created_at=new_portfolio.created_at
        )

schema = strawberry.Schema(query=Query, mutation=Mutation)

# Context dependency for GraphQL
async def get_context(
    db: AsyncSession = Depends(get_db),
    response: Response = None,
    session_id: Optional[str] = Cookie(None)
):
    return {
        "db": db,
        "response": response,
        "session_id": session_id
    }

# Add GraphQL endpoint
from strawberry.fastapi import GraphQLRouter
graphql_app = GraphQLRouter(
    schema,
    context_getter=get_context
)

app.include_router(graphql_app, prefix="/graphql")

# For simplicity, add a health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}