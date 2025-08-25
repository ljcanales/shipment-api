from app.data.response.tracking_response import TrackingResponse
from app.services.providers.stub import StubProvider
from app.services.providers.andreani import AndreaniProvider
from app.data.domain.courier import Courier


class TrackingService:
    """Coordinate tracking lookups across available courier providers."""

    def __init__(self) -> None:
        """Initialize provider instances for each supported courier."""

        self.providers = {
            Courier.STUB: StubProvider(),
            Courier.ANDREANI: AndreaniProvider(),
        }

    async def track(self, tracking_number: str, courier: Courier) -> TrackingResponse:
        """Retrieve tracking information from the provider for ``courier``."""

        provider = self.providers.get(courier)
        if not provider:
            raise ValueError("unsupported courier")
        return await provider.track(tracking_number)

    async def aclose(self) -> None:
        """Close any provider clients that expose an asynchronous close method."""

        for provider in self.providers.values():
            close = getattr(provider, "aclose", None)
            if close:
                await close()
