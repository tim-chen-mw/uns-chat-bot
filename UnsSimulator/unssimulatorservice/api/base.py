from fastapi import APIRouter
from ..util.metrics import metrics_response


router = APIRouter()


@router.get("/")
def root():
    return "Template Service"


@router.get('/metrics')
def metrics():
    """Expose service metrics"""
    return metrics_response()
