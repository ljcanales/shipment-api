from app.data.response.tracking_response import TrackingResponse
from app.services.providers.stub import StubProvider
from app.data.domain.courier import Courier


class TrackingService:
    def __init__(self):
        self.providers = {Courier.STUB: StubProvider()}

    async def track(self, tracking_number: str, courier: Courier) -> TrackingResponse:
        provider = self.providers.get(courier)
        if not provider:
            raise ValueError("unsupported courier")
        return await provider.track(tracking_number)
