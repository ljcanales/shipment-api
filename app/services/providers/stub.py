from datetime import datetime

from app.data.response.tracking_response import TrackingResponse, TrackingEvent
from app.data.domain.tracking import TrackingStatus
from app.data.domain.courier import Courier
from .base import Provider


class StubProvider(Provider):
    async def track(self, tracking_number: str) -> TrackingResponse:
        event = TrackingEvent(description="Package received", timestamp=datetime.utcnow())
        return TrackingResponse(
            tracking_number=tracking_number,
            courier=Courier.STUB,
            status=TrackingStatus.IN_TRANSIT,
            last_updated=datetime.utcnow(),
            events=[event],
        )
