from fastapi import HTTPException, Depends, Request,status
from sqlalchemy.orm import Session
from src.user.model import UserModel
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
from src.utils.settings import settings
from src.utils.db import get_db
security = HTTPBearer()

def is_authenticated(request: Request, db: Session = Depends(get_db),
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