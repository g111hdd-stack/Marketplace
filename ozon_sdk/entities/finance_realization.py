from typing import Optional

from .base import BaseEntity


class FinanceRealizationHeader(BaseEntity):
    """Титульный лист отчёта."""
    contract_date: str = None
    contract_number: str = None
    currency_sys_name: str = None
    doc_amount: float = None
    doc_date: str = None
    number: str = None
    payer_inn: str = None
    payer_kpp: str = None
    payer_name: str = None
    receiver_inn: str = None
    receiver_kpp: str = None
    receiver_name: str = None
    start_date: str = None
    stop_date: str = None
    vat_amount: float = None


class FinanceRealizationRowCommission(BaseEntity):
    """Комиссия."""
    amount: float = None
    bonus: float = None
    commission: float = None
    compensation: float = None
    price_per_instance: float = None
    quantity: int = None
    standard_fee: float = None
    stars: float = None
    total: float = None
    bank_coinvestment: float = None


class FinanceRealizationRowItem(BaseEntity):
    """Информация о товаре."""
    barcode: str = None
    name: str = None
    offer_id: str = None
    sku: int = None


class FinanceRealizationRow(BaseEntity):
    """Таблица отчёта."""
    commission_ratio: float = None
    delivery_commission: Optional[FinanceRealizationRowCommission] = None
    item: Optional[FinanceRealizationRowItem] = None
    return_commission: Optional[FinanceRealizationRowCommission] = None
    rowNumber: int = None
    seller_price_per_instance: float = None


class FinanceRealization(BaseEntity):
    """Отчёт о реализации товаров."""
    header: Optional[FinanceRealizationHeader] = None
    rows: Optional[list[FinanceRealizationRow]] = []
