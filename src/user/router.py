from fastapi import APIRouter,Depends,status, Request
from src.user import controler
from src.user.dtos import UserResponseSchema, UserSchema, UserLoginSchema
from src.utils.db import get_db
from typing import List
from sqlalchemy.orm import Session
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

user_router = APIRouter(prefix="/users")

@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def register_user(body: UserSchema, db: Session = Depends(get_db)):
    return controler.register(body, db)

@user_router.post("/login", status_code=status.HTTP_200_OK)
def login_user(body: UserLoginSchema, db: Session = Depends(get_db)):
    return controler.login(body, db)

@user_router.get("/is_authenticated", status_code=status.HTTP_200_OK)
def is_authenticated(request: Request, db: Session = Depends(get_db), credentials: HTTPAuthorizationCredentials = Depends(controler.security)):    
    return controler.is_authenticated(request, db, credentials)