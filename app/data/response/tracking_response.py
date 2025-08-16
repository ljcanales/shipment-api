from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.data.domain.tracking import TrackingStatus
from app.data.domain.courier import Courier


class TrackingEvent(BaseModel):
    description: str
    timestamp: datetime


class TrackingResponse(BaseModel):
    tracking_number: str
    courier: Courier
    status: TrackingStatus
    last_updated: datetime
    events: List[TrackingEvent] = []
