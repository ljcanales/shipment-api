import httpx
import logging
import pytest

from app.services.providers.andreani import AndreaniProvider
from app.services.providers.base import ProviderError


class DummyResponse:
    def raise_for_status(self) -> None:  # pragma: no cover - simple stub
        pass

    def json(self):  # pragma: no cover - simple stub
        return []


@pytest.mark.asyncio
async def test_andreani_provider_uses_env_configuration(monkeypatch):
    monkeypatch.setenv("ANDREANI_BASE_URL", "https://example.com")
    monkeypatch.setenv("ANDREANI_CONNECT_TIMEOUT", "1")
    monkeypatch.setenv("ANDREANI_READ_TIMEOUT", "2")
    monkeypatch.setenv("ANDREANI_WRITE_TIMEOUT", "3")
    monkeypatch.setenv("ANDREANI_POOL_TIMEOUT", "4")

    captured = {}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            captured["base_url"] = str(kwargs.get("base_url"))
            captured["timeout"] = kwargs.get("timeout")

        async def get(self, url):
            return DummyResponse()

        async def aclose(self):
            captured["closed"] = True

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)

    provider = AndreaniProvider()
    await provider.track("CODE123")
    await provider.aclose()

    assert captured["base_url"] == "https://example.com"
    timeout = captured["timeout"]
    assert timeout.connect == 1.0
    assert timeout.read == 2.0
    assert timeout.write == 3.0
    assert timeout.pool == 4.0
    assert captured["closed"] is True



@pytest.mark.asyncio
async def test_andreani_provider_raises_provider_error(monkeypatch, caplog):
    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def get(self, url):
            raise httpx.RequestError("boom")

        async def aclose(self):
            pass

    monkeypatch.setattr(httpx, "AsyncClient", DummyAsyncClient)

    provider = AndreaniProvider()

    with caplog.at_level(logging.ERROR):
        with pytest.raises(ProviderError) as exc:
            await provider.track("CODE123")

    assert isinstance(exc.value.__cause__, httpx.RequestError)
    assert any("Andreani request failed" in record.message for record in caplog.records)
