from app.data.response.tracking_response import TrackingResponse
from app.services.providers.stub import StubProvider
from app.services.providers.andreani import AndreaniProvider
from app.data.domain.courier import Courier


class TrackingService:
    def __init__(self):
        self.providers = {
            Courier.STUB: StubProvider(),
            Courier.ANDREANI: AndreaniProvider(),
        }

    async def track(self, tracking_number: str, courier: Courier) -> TrackingResponse:
        provider = self.providers.get(courier)
        if not provider:
            raise ValueError("unsupported courier")
        return await provider.track(tracking_number)

    async def aclose(self) -> None:
        for provider in self.providers.values():
            close = getattr(provider, "aclose", None)
            if close:
                await close()
