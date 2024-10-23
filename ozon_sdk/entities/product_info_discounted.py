from .base import BaseEntity


class ProductInfoDiscounted(BaseEntity):
    """Информация об уценке и основном товаре."""
    comment_reason_damaged: str = None
    condition: str = None
    condition_estimation: str = None
    defects: str = None
    discounted_sku: int = None
    mechanical_damage: str = None
    package_damage: str = None
    packaging_violation: str = None
    reason_damaged: str = None
    repair: str = None
    shortage: str = None
    sku: int = None
    warranty_type: str = None
