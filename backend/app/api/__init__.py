from fastapi import APIRouter
from app.api.admin_users import router as admin_user_router
from app.api.auth import router as auth_router
from app.api.roles import router as roles_router

router = APIRouter(prefix='/api/auths')

router.include_router(auth_router)
router.include_router(admin_user_router)
router.include_router(roles_router)


