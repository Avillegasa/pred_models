"""
User model for authentication
"""
import json
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.sql import func
from ..database import Base


# Default permissions for analysts
DEFAULT_ANALYST_PERMISSIONS = {
    "dashboard": True,
    "predictions": False,
    "reports": True,
    "alerts": True
}

# Admin has full access (permissions field is ignored)
DEFAULT_ADMIN_PERMISSIONS = {
    "dashboard": True,
    "predictions": True,
    "reports": True,
    "alerts": True
}


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(20), nullable=False)  # 'admin' or 'analyst'
    full_name = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    # Permissions per module (JSON string) - only applies to analysts
    permissions = Column(Text, default=json.dumps(DEFAULT_ANALYST_PERMISSIONS))

    def get_permissions(self) -> dict:
        """Get permissions as a dictionary"""
        if self.role == "admin":
            return DEFAULT_ADMIN_PERMISSIONS
        if self.permissions:
            try:
                return json.loads(self.permissions)
            except json.JSONDecodeError:
                return DEFAULT_ANALYST_PERMISSIONS
        return DEFAULT_ANALYST_PERMISSIONS

    def set_permissions(self, permissions: dict):
        """Set permissions from a dictionary"""
        self.permissions = json.dumps(permissions)

    def has_permission(self, permission: str) -> bool:
        """Check if user has a specific permission"""
        if self.role == "admin":
            return True
        perms = self.get_permissions()
        return perms.get(permission, False)
