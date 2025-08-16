import pytest

from app.services.tracking_service import TrackingService
from app.data.domain.courier import Courier


@pytest.mark.asyncio
async def test_stub_provider_tracks():
    service = TrackingService()
    resp = await service.track("123", Courier.STUB)
    assert resp.tracking_number == "123"
    assert resp.courier == Courier.STUB
