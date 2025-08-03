from abc import ABC, abstractmethod

from app.data.response.tracking_response import TrackingResponse


class Provider(ABC):
    @abstractmethod
    async def track(self, tracking_number: str) -> TrackingResponse:
        ...
