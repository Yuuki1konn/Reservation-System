from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import TokenResponse
from app.schemas.user import UserCreate, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_user,
    get_user_by_email,
)

router = APIRouter(
    prefix="/auth",
    tags=["认证"],
)
@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Session = Depends(get_db),
) -> UserResponse:
    normalized_email = str(user_data.email).lower()
    existing_user = get_user_by_email(
        db,
        normalized_email,
    )
    if existing_user is not None:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="邮箱已被注册",
        )
    return create_user(
        db,
        email = normalized_email,
        password=user_data.password,
    )

@router.post(
    "/login",
    response_model = TokenResponse,
)
def login(
    form_data: OAuth2PasswordRequestForm =Depends(),
    db: Session = Depends(get_db),
) -> TokenResponse:
    email = form_data.username.lower()
    user = authenticate_user(
        db,
        email=email,
        password=form_data.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        subject=str(user.id),
    )
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
    )