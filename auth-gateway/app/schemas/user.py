"""
User schemas
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, Literal
from datetime import datetime


class UserPermissions(BaseModel):
    """Permissions per module for analysts"""
    dashboard: bool = True
    predictions: bool = False
    reports: bool = True
    alerts: bool = True


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str  # 'admin' or 'analyst'


class UserCreate(UserBase):
    password: str
    permissions: Optional[UserPermissions] = None


class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    permissions: UserPermissions

    class Config:
        from_attributes = True

    @classmethod
    def from_orm_with_permissions(cls, user):
        """Create response with parsed permissions"""
        return cls(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at,
            permissions=UserPermissions(**user.get_permissions())
        )


# New schemas for permissions and role management
class PermissionsUpdate(BaseModel):
    """Schema for updating user permissions"""
    permissions: UserPermissions


class RoleUpdate(BaseModel):
    """Schema for updating user role"""
    role: Literal["admin", "analyst"]


class AdminPasswordReset(BaseModel):
    """Schema for admin resetting a user's password"""
    new_password: str = Field(..., min_length=6)


class PasswordChange(BaseModel):
    """Schema for user changing their own password"""
    current_password: str
    new_password: str = Field(..., min_length=6)


class ProfileResponse(BaseModel):
    """Full profile response for current user"""
    id: int
    username: str
    email: str
    full_name: Optional[str]
    role: str
    permissions: UserPermissions
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class ProfileUpdate(BaseModel):
    """Schema for updating own profile"""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
