from .auth import router as auth_router
from .users import router as users_router
from .files import router as files_router
from .reports import router as reports_router
from .alerts import router as alerts_router
from .predictions import router as predictions_router
from .monthly_reports import router as monthly_reports_router
from .profile import router as profile_router

__all__ = ["auth_router", "users_router", "files_router", "reports_router", "alerts_router", "predictions_router", "monthly_reports_router", "profile_router"]
