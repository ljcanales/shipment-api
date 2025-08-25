from app.data.response.tracking_response import TrackingResponse
from app.services.providers.stub import StubProvider
from app.services.providers.andreani import AndreaniProvider
from app.services.providers.base import ProviderError
from app.data.domain.courier import Courier


class TrackingService:
    """Service to fetch tracking information from providers."""

    def __init__(self):
        self.providers = {
            Courier.STUB: StubProvider(),
            Courier.ANDREANI: AndreaniProvider(),
        }

    async def track(self, tracking_number: str, courier: Courier) -> TrackingResponse:
        """Fetch tracking info for the given courier.

        Raises:
            ProviderError: If the provider fails to retrieve data.
            ValueError: If the courier is unsupported.
        """
        provider = self.providers.get(courier)
        if not provider:
            raise ValueError("unsupported courier")
        try:
            return await provider.track(tracking_number)
        except ProviderError:
            raise

    async def aclose(self) -> None:
        for provider in self.providers.values():
            close = getattr(provider, "aclose", None)
            if close:
                await close()
