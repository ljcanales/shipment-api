from enum import Enum


class TrackingStatus(str, Enum):
    IN_TRANSIT = "in_transit"
    DELIVERED = "delivered"
