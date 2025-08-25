from abc import ABC, abstractmethod

from app.data.response.tracking_response import TrackingResponse


class ProviderError(Exception):
    """Raised when a provider fails to fetch tracking information."""


class Provider(ABC):
    """Abstract base class for tracking providers."""

    @abstractmethod
    async def track(self, tracking_number: str) -> TrackingResponse:
        """Return tracking information for ``tracking_number``."""
        ...
