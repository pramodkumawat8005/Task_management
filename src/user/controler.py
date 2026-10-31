from sqlalchemy.orm import Session
from src.user.dtos import UserSchema, UserLoginSchema
from src.user.model import UserModel
from fastapi import HTTPException,Request,Depends
from pwdlib import PasswordHash
from src.utils.settings import settings
import jwt
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta

password_hash = PasswordHash.recommended()
security = HTTPBearer() 
def get_password_hash(password):
    return password_hash.hash(password)

def register(body: UserSchema, db: Session):
    is_user = db.query(UserModel).filter((UserModel.username == body.username)).first()
    if is_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    is_email = db.query(UserModel).filter((UserModel.email == body.email)).first()
    if is_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    hashed_password = get_password_hash(body.password)
    
    new_user = UserModel(name=body.name,
                         username=body.username,
                         email=body.email,
                         hashed_password=hashed_password
                         )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(body: UserLoginSchema, db: Session):
    user = db.query(UserModel).filter((UserModel.username == body.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not password_hash.verify(body.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")
    exp_time = datetime.now() + timedelta(minutes=settings.EXPIRATION_TIME_MINUTES)
    token = jwt.encode({"sub": str(user.id), "exp": exp_time}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return {"token": token}

def is_authenticated(request: Request, db: Session,
                     credentials: HTTPAuthorizationCredentials = Depends(security)
                    ):
    token = credentials.credentials

    try:
        payload = jwt.decode(token,settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(status_code=401,detail="Invalid token")

        user = db.query(UserModel).filter(UserModel.id == user_id).first()

        if not user:
            raise HTTPException(status_code=404,detail="User not found")

        return user

    except jwt.ExpiredSignatureError:
     raise HTTPException(
        status_code=401,
        detail="Token has expired"
     )

    except jwt.InvalidTokenError as e:
     print("JWT ERROR:", type(e).__name__, str(e))
     raise HTTPException(
        status_code=401,
        detail=f"Invalid token: {str(e)}"
     )
    