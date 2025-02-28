# app/schemas.py
from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    username: str
    
    @validator('username')
    def username_validator(cls, v):
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return v

class UserCreate(UserBase):
    password: str
    
    @validator('password')
    def password_validator(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserRead(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

# Login schema
class LoginData(BaseModel):
    username: str
    password: str

# Portfolio schemas
class PortfolioBase(BaseModel):
    role_name: str
    jobs_count: int
    
    @validator('jobs_count')
    def jobs_count_validator(cls, v):
        if v < 0:
            raise ValueError('Jobs count cannot be negative')
        return v

class PortfolioCreate(PortfolioBase):
    pass

class PortfolioRead(PortfolioBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True