from typing import Optional

from .base import BaseRequest


class CampaignsOrdersRequest(BaseRequest):
    """Информация о заказах."""
    orderIds: Optional[list[int]]
    status: Optional[list[str]]
    substatus: Optional[list[str]]
    fromDate: Optional[str]
    toDate: Optional[str]
    supplierShipmentDateFrom: Optional[str]
    supplierShipmentDateTo: Optional[str]
    updatedAtFrom: Optional[str]
    updatedAtTo: Optional[str]
    dispatchType: Optional[str]
    fake: bool = False
    hasCis: bool = False
    onlyWaitingForCancellationApprove: bool = False
    onlyEstimatedDelivery: bool = False
    buyerType: Optional[str]
    page: int = 1
    pageSize: int = 50


