from jose import jwt
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from passlib.context import CryptContext
from pydantic import UUID4, BaseModel
from app.core.user.models import Users
import uuid
from app.core.config import settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Auth:

    @staticmethod
    async def authenticate(email: str, password: str):
        user = await Users.get_or_none(email=email).values()

        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        if not Users.verify_password(password, user["password_hash"]):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        user.pop('created_at')
        user.pop('modified_at')
        user.pop('password_hash')

        access_token = Auth.create_access_token(user)
        refresh_token = Auth.create_refresh_token(user)

        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    @staticmethod
    def create_access_token(data: dict, expires_delta: int = None) -> str:
        to_encode = data.copy()

        if expires_delta is not None:
            access_token_expires = datetime.utcnow() + expires_delta
        else:
            access_token_expires = datetime.utcnow(
            ) + timedelta(minutes=int(settings.ACCESS_TOKEN_EXPIRE_MINUTES))

        to_encode.update({
            "exp": str(access_token_expires.isoformat()),
            "iss": settings.APP_NAME
        })
        return jwt.encode(to_encode, settings.JWT_SECRET_KEY, settings.TOKEN_ALGORITHM)

    @staticmethod
    def create_refresh_token(data: dict, expires_delta: int = None) -> str:
        to_encode = data.copy()

        if expires_delta is not None:
            refresh_token_expires = datetime.utcnow() + expires_delta
        else:
            refresh_token_expires = datetime.utcnow(
            ) + timedelta(minutes=int(settings.REFRESH_TOKEN_EXPIRE_MINUTES))

        to_encode.update({
            "exp": str(refresh_token_expires.isoformat()),
            "iss": settings.APP_NAME
        })
        return jwt.encode(to_encode, settings.JWT_REFRESH_SECRET_KEY, settings.TOKEN_ALGORITHM)

    @staticmethod
    def get_confirmation_token(user_id: UUID4):
        jti = uuid.uuid4()
        claims = {
            "sub": user_id,
            "scope": "registration",
            "jti": jti
        }
        return {
            "jti": jti,
            "token": Auth.get_token(
                claims,
                settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )
        }


class Protect:

    __oauth2_password: OAuth2PasswordBearer = None

    @classmethod
    def end_point_by_password(cls):
        if cls.__oauth2_password is None:
            cls.__oauth2_password = OAuth2PasswordBearer(
                tokenUrl="/users/login")
        return cls.__oauth2_password
