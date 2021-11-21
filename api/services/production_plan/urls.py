from fastapi import APIRouter
from .app import api


router = APIRouter()
router.include_router(api)
