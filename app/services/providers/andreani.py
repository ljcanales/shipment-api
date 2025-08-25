import os
from datetime import datetime
from typing import List

import httpx

from app.data.domain.courier import Courier
from app.data.domain.tracking import TrackingStatus
from app.data.response.tracking_response import TrackingResponse, TrackingEvent
from .base import Provider


class AndreaniProvider(Provider):
    """Provider implementation for the Andreani courier service."""

    DEFAULT_BASE_URL = "https://apidestinatarios.andreani.com"

    def __init__(self) -> None:
        """Configure the HTTP client used to communicate with Andreani's API."""

        base_url = os.getenv("ANDREANI_BASE_URL", self.DEFAULT_BASE_URL)
        timeout = httpx.Timeout(
            connect=float(os.getenv("ANDREANI_CONNECT_TIMEOUT", "5")),
            read=float(os.getenv("ANDREANI_READ_TIMEOUT", "10")),
            write=float(os.getenv("ANDREANI_WRITE_TIMEOUT", "5")),
            pool=float(os.getenv("ANDREANI_POOL_TIMEOUT", "5")),
        )
        self._client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def track(self, tracking_number: str) -> TrackingResponse:
        """Fetch tracking events for ``tracking_number`` from Andreani's API."""

        response = await self._client.get(f"/api/envios/{tracking_number}/trazas")
        response.raise_for_status()
        data = response.json()

        events: List[TrackingEvent] = []
        for item in data or []:
            description = item["estado"]
            try:
                timestamp = datetime.strptime(
                    f"{item['fecha']['dia']} {item['fecha']['hora']}", "%d-%m-%Y %H:%M"
                )
            except ValueError:
                timestamp = datetime.utcnow()
            events.append(TrackingEvent(description=description, timestamp=timestamp))

        events.sort(key=lambda e: e.timestamp)

        summary_desc = data[0]["evento"] if data else ""
        status = (
            TrackingStatus.DELIVERED
            if summary_desc == "EnvioEntregado"
            else TrackingStatus.IN_TRANSIT
        )

        last_updated = events[-1].timestamp if events else datetime.utcnow()

        return TrackingResponse(
            tracking_number=tracking_number,
            courier=Courier.ANDREANI,
            status=status,
            last_updated=last_updated,
            events=events,
        )

    async def aclose(self) -> None:
        """Close the underlying HTTP client session."""

        await self._client.aclose()
