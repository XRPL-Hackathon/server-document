from fastapi import APIRouter

from src.main.health.router import HealthAPIRouter
from src.main.file.router.FileAPIRouter import router as file_router


router = APIRouter(
    prefix="",
)

router.include_router(HealthAPIRouter.router)
router.include_router(file_router)