from .base import BaseRequest
from pydantic import Field
from enum import Enum


class FinanceTransactionListDate(BaseRequest):
    """
        Фильтр по дате.

        Аргументы:
            from_field (str): Начало периода.
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ. \n
                Пример: 2019-11-25T10:43:06.51Z.
            to (str): Конец периода.
                Формат: YYYY-MM-DDTHH:mm:ss.sssZ. \n
                Пример: 2019-11-25T10:43:06.51Z.
    """
    from_field: str = Field(serialization_alias='from')
    to: str


class OperationTypeEnum(str, Enum):
    """
        Тип операции:
            ClientReturnAgentOperation — получение возврата, отмены, невыкупа от покупателя; \n
            MarketplaceMarketingActionCostOperation — услуги продвижения товаров; \n
            MarketplaceSaleReviewsOperation — приобретение отзывов на платформе; \n
            MarketplaceSellerCompensationOperation — прочие компенсации; \n
            OperationAgentDeliveredToCustomer — доставка покупателю; \n
            OperationAgentDeliveredToCustomerCanceled — доставка покупателю — исправленное начисление; \n
            OperationAgentStornoDeliveredToCustomer — доставка покупателю — отмена начисления; \n
            OperationClaim — начисление по претензии; \n
            OperationCorrectionSeller — инвентаризация взаиморасчетов; \n
            OperationDefectiveWriteOff — компенсация за повреждённый на складе товар; \n
            OperationItemReturn — доставка и обработка возврата, отмены, невыкупа; \n
            OperationLackWriteOff — компенсация за утерянный на складе товар; \n
            OperationMarketplaceCrossDockServiceWriteOff — доставка товаров на склад Ozon (кросс-докинг); \n
            OperationMarketplaceServiceStorage — услуга размещения товаров на складе; \n
            OperationSetOff — взаимозачёт с другими договорами контрагента; \n
            MarketplaceSellerReexposureDeliveryReturnOperation — перечисление за доставку от покупателя; \n
            OperationReturnGoodsFBSofRMS — доставка и обработка возврата, отмены, невыкупа; \n
            ReturnAgentOperationRFBS — возврат перечисления за доставку покупателю; \n
            MarketplaceSellerShippingCompensationReturnOperation — компенсация перечисления за доставку; \n
            OperationMarketplaceServicePremiumCashback — услуга продвижения Premium; \n
            MarketplaceServicePremiumPromotion — услуга продвижения Premium, фиксированная комиссия; \n
            MarketplaceRedistributionOfAcquiringOperation — оплата эквайринга; \n
            MarketplaceReturnStorageServiceAtThePickupPointFbsItem — краткосрочное размещение возврата FBS; \n
            MarketplaceReturnStorageServiceInTheWarehouseFbsItem — долгосрочное размещение возврата FBS; \n
            MarketplaceServiceItemDeliveryKGT — доставка КГТ; \n
            MarketplaceServiceItemDirectFlowLogistic — логистика; \n
            MarketplaceServiceItemReturnFlowLogistic — обратная логистика; \n
            MarketplaceServicePremiumCashbackIndividualPoints — услуга продвижения «Бонусы продавца»; \n
            OperationMarketplaceWithHoldingForUndeliverableGoods — удержание за недовложение товара; \n
            MarketplaceServiceItemDirectFlowLogisticVDC — логистика вРЦ; \n
            MarketplaceServiceItemDropoffPPZ — услуга drop-off в пункте приёма заказов; \n
            MarketplaceServicePremiumCashback — услуга продвижения Premium; \n
            MarketplaceServiceItemRedistributionReturnsPVZ — перевыставление возвратов на пункте выдачи.
    """
    client_return_agent_operation = 'ClientReturnAgentOperation'
    marketplace_marketing_action_cost_operation = 'MarketplaceMarketingActionCostOperation'
    marketplace_sale_reviews_operation = 'MarketplaceSaleReviewsOperation'
    marketplace_seller_compensation_operation = 'MarketplaceSellerCompensationOperation'
    operation_agent_delivered_to_customer = 'OperationAgentDeliveredToCustomer'
    operation_agent_delivered_to_customer_canceled = 'OperationAgentDeliveredToCustomerCanceled'
    operation_agent_storno_delivered_to_customer = 'OperationAgentStornoDeliveredToCustomer'
    operation_claim = 'OperationClaim'
    operation_correction_seller = 'OperationCorrectionSeller'
    operation_defective_write_off = 'OperationDefectiveWriteOff'
    operation_lack_write_off = 'OperationLackWriteOff'
    operation_item_return = 'OperationItemReturn'
    operation_marketplace_cross_dock_service_write_off = 'OperationMarketplaceCrossDockServiceWriteOff'
    operation_marketplace_service_storage = 'OperationMarketplaceServiceStorage'
    operation_set_off = 'OperationSetOff'
    marketplace_seller_reexposure_delivery_return_operation = 'MarketplaceSellerReexposureDeliveryReturnOperation'
    operation_return_goods_fbs_of_rms = 'OperationReturnGoodsFBSofRMS'
    return_agent_operation_rfbs = 'ReturnAgentOperationRFBS'
    marketplace_seller_shipping_compensation_return_operation = 'MarketplaceSellerShippingCompensationReturnOperation'
    operation_marketplace_service_premium_cashback = 'OperationMarketplaceServicePremiumCashback'
    marketplace_service_premium_promotion = 'MarketplaceServicePremiumPromotion'
    marketplace_redistribution_of_acquiring_operation = 'MarketplaceRedistributionOfAcquiringOperation'
    marketplace_return_storage_service_at_the_pickup_point_fbs_item = 'MarketplaceReturnStorageServiceAtThePickupPointFbsItem'
    marketplace_return_storage_service_in_the_warehouse_fbs_item = 'MarketplaceReturnStorageServiceInTheWarehouseFbsItem'
    marketplace_service_item_delivery_kgt = 'MarketplaceServiceItemDeliveryKGT'
    marketplace_service_item_direct_flow_logistic = 'MarketplaceServiceItemDirectFlowLogistic'
    marketplace_service_item_return_flow_logistic = 'MarketplaceServiceItemReturnFlowLogistic'
    marketplace_service_premium_cashback_individual_points = 'MarketplaceServicePremiumCashbackIndividualPoints'
    operation_marketplace_with_holding_for_undeliverable_goods = 'OperationMarketplaceWithHoldingForUndeliverableGoods'
    marketplace_service_item_direct_flow_logistic_vdc = 'MarketplaceServiceItemDirectFlowLogisticVDC'
    marketplace_service_item_drop_off_ppz = 'MarketplaceServiceItemDropoffPPZ'
    marketplace_service_premium_cashback = 'MarketplaceServicePremiumCashback'
    marketplace_service_item_redistribution_returns_pvz = 'MarketplaceServiceItemRedistributionReturnsPVZ'


class TransactionTypeEnum(str, Enum):
    """
        Тип начисления:
            all — все, \n
            orders — заказы, \n
            returns — возвраты и отмены, \n
            services — сервисные сборы, \n
            compensation — компенсация, \n
            transferDelivery — стоимость доставки, \n
            other — прочее.

        Некоторые операции могут быть разделены во времени.
        Например, при приёме возврата от покупателя списывается стоимость товара и возвращается комиссия, а когда товар
        возвращается на склад, взимается стоимость услуга по обработке возврата.
    """
    all = 'all'
    services = 'services'
    compensation = 'compensation'
    transfer_delivery = 'transferDelivery'
    other = 'other'


class FinanceTransactionListFilter(BaseRequest):
    """
        Фильтр. \n
        Если в запросе не указывать posting_number, то в ответе будут все отправления за указанный период или отправления определённого типа.

        Аргументы:
            date (FinanceTransactionListFilter): Фильтр по дате. \n
            operation_type (list[OperationTypeEnum], optional): Список типов операций.Default to []. \n
            posting_number (str, optional): Количество элементов на странице.. Default to ''. \n
            transaction_type (TransactionTypeEnum, optional): Тип начисления.. Default to 'all'.
    """
    date: FinanceTransactionListDate
    operation_type: list[OperationTypeEnum] = []
    posting_number: str = ''
    transaction_type: TransactionTypeEnum = TransactionTypeEnum.all


class FinanceTransactionListRequest(BaseRequest):
    """
        Возвращает подробную информацию по всем начислениям. Максимальный период, за который можно получить информацию в одном запросе — 1 месяц.

        Аргументы:
            filter (FinanceTransactionListFilter): Фильтр. \n
            page (int, optional): Номер страницы, возвращаемой в запросе.. Default to 1. \n
            page_size (int, optional): Количество элементов на странице.. Default to 1000.
    """
    filter: FinanceTransactionListFilter
    page: int = 1
    page_size: int = 1000
