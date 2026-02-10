"""
Profile management endpoints (Authenticated users)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import ProfileResponse, ProfileUpdate, PasswordChange, UserPermissions
from ..services.auth_service import AuthService, get_current_user
from ..models.user import User

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("", response_model=ProfileResponse)
async def get_my_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user's profile"""
    return ProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        permissions=UserPermissions(**current_user.get_permissions()),
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.put("", response_model=ProfileResponse)
async def update_my_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update current user's profile (email and full_name only)"""
    # Update email if provided
    if profile_data.email is not None:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            User.email == profile_data.email,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        current_user.email = profile_data.email

    # Update full_name if provided
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name

    db.commit()
    db.refresh(current_user)

    return ProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        role=current_user.role,
        permissions=UserPermissions(**current_user.get_permissions()),
        is_active=current_user.is_active,
        created_at=current_user.created_at
    )


@router.put("/password")
async def change_my_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Change current user's password"""
    # Verify current password
    if not AuthService.verify_password(password_data.current_password, current_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect"
        )

    # Update password
    current_user.password_hash = AuthService.get_password_hash(password_data.new_password)
    db.commit()

    return {"message": "Password changed successfully"}
