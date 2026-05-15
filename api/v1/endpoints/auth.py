from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.user import UserCreate, UserLogin, UserResponse
from services.user_service import UserService
from utlis.response import api_response

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    
    - **username**: Unique username
    - **email**: Valid email address
    - **password**: Password for the account
    """
    user = UserService.create_user(db, user_data)
    return api_response(
        message="User created successfully",
        data=UserResponse.model_validate(user).model_dump(mode="json"),
        status_code=status.HTTP_201_CREATED,
    )

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(login_data: UserLogin, db: Session = Depends(get_db)):
    """
    Login user and get access token
    
    - **email**: User's email
    - **password**: User's password
    
    Returns access token for authenticated requests
    """
    result = UserService.login_user(db, login_data)
    return api_response(
        message="Login successful",
        data=result,
        status_code=status.HTTP_200_OK,
    )
