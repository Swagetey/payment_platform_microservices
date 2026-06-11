from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError

from app.core.config import settings

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


def hash_password(
        password: str
) -> str:
    return pwd_context.hash(password)


def verify_password(
        plain_password: str,
        hashed_password
) -> bool:
    return pwd_context.verify(
        plain_password,
        hashed_password
    )


def create_access_token(
        user_id: int
) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": expire,
    }

    return jwt.encode(
        claims=payload,
        key=settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )


def create_refresh_token(
        user_id: int
) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)

    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expire,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        settings.jwt_algorithm,
    )

def decode_token(
        token: str
) -> dict:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        return payload
    except JWTError as e:
        raise ValueError("Invalid token") from e
