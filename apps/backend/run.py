# run.py
import asyncio
import uvicorn
from app.db.database import create_tables

async def init_db():
    """Initialize the database on startup."""
    print("Creating database tables...")
    await create_tables()
    print("Database tables created.")

if __name__ == "__main__":
    # Create tables before starting the server
    asyncio.run(init_db())
    
    # Start the FastAPI server
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True  # Set to False in production
    )