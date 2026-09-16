from fastapi import APIRouter
from app.api.admin_users import router as admin_user_router
from app.api.auth import router as auth_router
from app.api.roles import router as roles_router
from app.api.department import router as department_router
from app.api.staff import router as staff_router
from app.api.position import router as position_router
from app.api.attendance import router as attendance_router

router = APIRouter(prefix='/api')

router.include_router(auth_router)
router.include_router(admin_user_router)
router.include_router(roles_router)
router.include_router(department_router)
router.include_router(staff_router)
router.include_router(position_router)
router.include_router(attendance_router)


