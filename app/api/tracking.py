"""API routes for shipment tracking and service health checks."""

from fastapi import APIRouter, Depends

from app.services.tracking_service import TrackingService
from app.data.response.tracking_response import TrackingResponse
from app.data.domain.courier import Courier


async def get_tracking_service():
    """Yield a ``TrackingService`` instance and ensure proper cleanup."""

    service = TrackingService()
    try:
        yield service
    finally:
        await service.aclose()


router = APIRouter(prefix="/api/v1")


@router.get("/health")
async def health():
    """Return a simple status response confirming the service is running."""

    return {"status": "ok"}


@router.get("/shipments/{tracking_number}", response_model=TrackingResponse)
async def get_tracking(
    tracking_number: str,
    courier: Courier,
    service: TrackingService = Depends(get_tracking_service),
):
    """Fetch tracking details for a shipment from the specified courier."""

    return await service.track(tracking_number, courier)
