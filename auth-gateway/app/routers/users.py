"""
User management endpoints (Admin only)
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas.user import (
    UserCreate, UserResponse, UserUpdate,
    PermissionsUpdate, RoleUpdate, AdminPasswordReset
)
from ..services.auth_service import AuthService, get_current_admin
from ..models.user import User, DEFAULT_ANALYST_PERMISSIONS, DEFAULT_ADMIN_PERMISSIONS

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """List all users (Admin only)"""
    users = db.query(User).offset(skip).limit(limit).all()
    return [UserResponse.from_orm_with_permissions(u) for u in users]


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Create a new user (Admin only)"""
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )

    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Validate role
    if user_data.role not in ["admin", "analyst"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Role must be 'admin' or 'analyst'"
        )

    # Set default permissions based on role
    if user_data.permissions:
        permissions = user_data.permissions.model_dump()
    else:
        permissions = DEFAULT_ADMIN_PERMISSIONS if user_data.role == "admin" else DEFAULT_ANALYST_PERMISSIONS

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password_hash=AuthService.get_password_hash(user_data.password),
        role=user_data.role,
        full_name=user_data.full_name,
        is_active=True
    )
    new_user.set_permissions(permissions)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return UserResponse.from_orm_with_permissions(new_user)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Get user by ID (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return UserResponse.from_orm_with_permissions(user)


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update user (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Update fields if provided
    if user_data.email is not None:
        # Check if email is already taken by another user
        existing = db.query(User).filter(
            User.email == user_data.email,
            User.id != user_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use"
            )
        user.email = user_data.email

    if user_data.full_name is not None:
        user.full_name = user_data.full_name

    if user_data.password is not None:
        user.password_hash = AuthService.get_password_hash(user_data.password)

    if user_data.is_active is not None:
        user.is_active = user_data.is_active

    db.commit()
    db.refresh(user)

    return UserResponse.from_orm_with_permissions(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Delete user (Admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete yourself"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    db.delete(user)
    db.commit()


@router.put("/{user_id}/role", response_model=UserResponse)
async def update_user_role(
    user_id: int,
    role_data: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Change user role (Admin only)"""
    if user_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot change your own role"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.role = role_data.role

    # Update permissions based on new role
    if role_data.role == "admin":
        user.set_permissions(DEFAULT_ADMIN_PERMISSIONS)
    else:
        # Keep current permissions or set defaults for analyst
        current_perms = user.get_permissions()
        user.set_permissions(current_perms)

    db.commit()
    db.refresh(user)

    return UserResponse.from_orm_with_permissions(user)


@router.put("/{user_id}/permissions", response_model=UserResponse)
async def update_user_permissions(
    user_id: int,
    permissions_data: PermissionsUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Update user permissions (Admin only). Only applies to analysts."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    if user.role == "admin":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot modify permissions for admin users (they have full access)"
        )

    user.set_permissions(permissions_data.permissions.model_dump())
    db.commit()
    db.refresh(user)

    return UserResponse.from_orm_with_permissions(user)


@router.put("/{user_id}/password", response_model=UserResponse)
async def reset_user_password(
    user_id: int,
    password_data: AdminPasswordReset,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_admin)
):
    """Reset user password (Admin only)"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    user.password_hash = AuthService.get_password_hash(password_data.new_password)
    db.commit()
    db.refresh(user)

    return UserResponse.from_orm_with_permissions(user)
