from fastapi import APIRouter, Depends

from app.services.tracking_service import TrackingService
from app.data.response.tracking_response import TrackingResponse
from app.data.domain.courier import Courier


async def get_tracking_service():
    service = TrackingService()
    try:
        yield service
    finally:
        await service.aclose()

router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def health():
    return {"status": "ok"}


@router.get("/shipments/{tracking_number}", response_model=TrackingResponse)
async def get_tracking(
    tracking_number: str,
    courier: Courier,
    service: TrackingService = Depends(get_tracking_service),
):
    return await service.track(tracking_number, courier)
