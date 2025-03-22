from fastapi import APIRouter

from src.main.health.router import HealthAPIRouter
from src.main.file.router import FileAPIRouter


router = APIRouter(
    prefix="",
)

router.include_router(HealthAPIRouter.router)
router.include_router(FileAPIRouter.router)