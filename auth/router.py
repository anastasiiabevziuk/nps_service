from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from auth.schemas import TokenRequest, TokenResponse, UserInDB
from auth.utils import verify_password, create_access_token, decode_access_token
from datetime import timedelta
from typing import Optional
import os

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


router = APIRouter(tags=["Auth"])


MOCKED_USER = {
    "user_id": int(os.getenv("MOCK_USER_ID")),
    "username": os.getenv("MOCK_USERNAME"),
    "hashed_password": os.getenv("MOCK_HASHED_PASSWORD"),
}


def authenticate_user(username: str, password: str) -> Optional[UserInDB]:
    """Verify user credentials (moc)"""
    if username == MOCKED_USER["username"]:
        if verify_password(password, MOCKED_USER["hashed_password"]):
            return UserInDB(**MOCKED_USER)
    return None


def get_user_from_payload(payload: dict) -> Optional[UserInDB]:
    """Get user from decoded token payload."""
    if payload and "user_id" in payload:
        if payload["user_id"] == MOCKED_USER["user_id"]:
            return UserInDB(**MOCKED_USER)
    return None


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(form_data: TokenRequest):
    """Authorizes the user and returns a JWT access token."""
    user = authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"user_id": user.user_id}, expires_delta=access_token_expires
    )

    return {"access_token": access_token}


async def get_current_user(token: str = Depends(oauth2_scheme)) -> UserInDB:
    """Dependency that verifies the token and returns the current user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)

    if payload is None:
        raise credentials_exception

    user = get_user_from_payload(payload)

    if user is None:
        raise credentials_exception

    return user
