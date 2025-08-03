import pytest

from app.services.tracking_service import TrackingService


@pytest.mark.asyncio
async def test_stub_provider_tracks():
    service = TrackingService()
    resp = await service.track("123", "stub")
    assert resp.tracking_number == "123"
    assert resp.courier == "stub"
