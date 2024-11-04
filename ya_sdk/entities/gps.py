from .base import BaseEntity


class GpsDTO(BaseEntity):
    """GPS-координаты широты и долготы."""
    latitude: float = None
    longitude: float = None
