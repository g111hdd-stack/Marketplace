from typing import Optional

from pydantic import Field

from .base import BaseEntity


class GetMappingDTO(BaseEntity):
    """Информация о товарах в каталоге."""
    marketCategoryId: Optional[int] = None
    marketCategoryName: Optional[str] = None
    marketSku: Optional[int] = None
    marketSkuName: Optional[str] = None


class AgeDTO(BaseEntity):
    """Возраст в заданных единицах измерения."""
    ageUnit: Optional[str] = None
    value: Optional[float] = None


class GetPriceWithDiscountDTO(BaseEntity):
    """Цена с указанием скидки и времени последнего обновления."""
    updatedAt: Optional[str] = None
    currencyId: Optional[str] = None
    discountBase: Optional[float] = None
    value: Optional[float] = None


class OfferCampaignStatusDTO(BaseEntity):
    """Статус товара в магазине."""
    campaignId: Optional[int] = None
    status: Optional[str] = None


class CommodityCodeDTO(BaseEntity):
    """Товарный код."""
    code: Optional[str] = None
    type_field: str = Field(None, alias='type')


class OfferConditionDTO(BaseEntity):
    """Состояние уцененного товара."""
    quality: Optional[str] = None
    reason: Optional[str] = None
    type_field: str = Field(None, alias='type')


class OfferManualDTO(BaseEntity):
    """Инструкция по использованию товара."""
    url: Optional[str] = None
    title: Optional[str] = None


class OfferMediaFileDTO(BaseEntity):
    """Информация о медиафайле товара."""
    title: Optional[str] = None
    uploadState: Optional[str] = None
    url: Optional[str] = None


class OfferMediaFilesDTO(BaseEntity):
    """Информация о медиафайлах товара."""
    firstVideoAsCover: Optional[bool] = None
    manuals: Optional[list[OfferMediaFileDTO]] = []
    pictures: Optional[list[OfferMediaFileDTO]] = []
    videos: Optional[list[OfferMediaFileDTO]] = []


class GetPriceDTO(BaseEntity):
    """Цена с указанием времени последнего обновления."""
    currencyId: Optional[str] = None
    updatedAt: Optional[str] = None
    value: Optional[float] = None


class OfferSellingProgramDTO(BaseEntity):
    """Информация о том, по каким моделям можно продавать товар, а по каким нельзя."""
    sellingProgram: Optional[str] = None
    status: Optional[str] = None


class TimePeriodDTO(BaseEntity):
    """Временной отрезок с комментарием."""
    timePeriod: Optional[int] = None
    timeUnit: Optional[str] = None
    comment: Optional[str] = None


class OfferWeightDimensionsDTO(BaseEntity):
    """Габариты упаковки и вес товара."""
    height: Optional[float] = None
    length: Optional[float] = None
    weight: Optional[float] = None
    width: Optional[float] = None


class GetOfferDTO(BaseEntity):
    """Параметры товара."""
    offerId: str
    additionalExpenses: Optional[GetPriceDTO] = None
    adult: Optional[bool] = None
    age: Optional[AgeDTO] = None
    archived: Optional[bool] = None
    barcodes: Optional[list] = []
    basicPrice: Optional[GetPriceWithDiscountDTO] = None
    boxCount: Optional[int] = None
    campaigns: Optional[list[OfferCampaignStatusDTO]] = []
    cardStatus: Optional[str] = None
    certificates: Optional[list[str]] = []
    cofinancePrice: Optional[GetPriceDTO] = None
    commodityCodes: Optional[list[CommodityCodeDTO]] = []
    condition: Optional[OfferConditionDTO] = None
    description: Optional[str] = None
    downloadable: Optional[bool] = None
    guaranteePeriod: Optional[TimePeriodDTO] = None
    lifeTime: Optional[TimePeriodDTO] = None
    manuals: Optional[list[OfferManualDTO]] = []
    OfferManualDTO: Optional[list[str]] = []
    marketCategoryId: Optional[int] = None
    mediaFiles: Optional[OfferMediaFilesDTO] = None
    name: Optional[str] = None
    pictures: Optional[list[str]] = []
    purchasePrice: Optional[GetPriceDTO] = None
    sellingPrograms: Optional[list[OfferSellingProgramDTO]] = []
    shelfLife: Optional[TimePeriodDTO] = None
    tags: Optional[list[str]] = []
    type_field: str = Field(None, alias='type')
    vendor: Optional[str] = None
    vendorCode: Optional[str] = None
    videos: Optional[list[str]] = []
    weightDimensions: Optional[OfferWeightDimensionsDTO] = None


class GetOfferMappingDTO(BaseEntity):
    """Информация о товаре."""
    mapping: Optional[GetMappingDTO] = None
    offer: Optional[GetOfferDTO] = None


class ScrollingPagerDTO(BaseEntity):
    """Информация о страницах результатов."""
    nextPageToken: Optional[str] = None
    prevPageToken: Optional[str] = None


class GetOfferMappingsResultDTO(BaseEntity):
    """Информация о товарах."""
    offerMappings: Optional[list[GetOfferMappingDTO]] = []
    paging: Optional[ScrollingPagerDTO] = None
