from typing import Union

from .requests import *
from .response import *
from .core import YandexAsyncEngine
from .ya_endpoints_list import YandexAPIFactory


class YandexApi:

    def __init__(self, api_key: str):
        self._engine = YandexAsyncEngine(api_key=api_key)
        self._api_factory = YandexAPIFactory(self._engine)

        self._campaigns_api = self._api_factory.get_api(CampaignsResponse)
        self._campaigns_orders_api = self._api_factory.get_api(CampaignsOrdersResponse)
        self._campaigns_stats_orders_api = self._api_factory.get_api(CampaignsStatsOrdersResponse)
        self._reports_info_api = self._api_factory.get_api(ReportsInfoResponse)
        self._reports_united_marketplace_services_generate_api = self._api_factory.get_api(ReportsUnitedMarketplaceServicesGenerateResponse)

    async def get_campaigns(self, page: int = 1, page_size: int = None) -> CampaignsResponse:
        request = CampaignsRequest(page=page, pageSize=page_size)
        answer: CampaignsResponse = await self._campaigns_api.get(request)
        return answer

    async def get_campaigns_orders(self,
                                   campaign_id: Union[str, int],
                                   from_date: str = None,
                                   to_date: str = None,
                                   order_ids: list[int] = None,
                                   status: list[str] = None,
                                   substatus: list[str] = None,
                                   supplier_shipment_date_from: str = None,
                                   supplier_shipment_date_to: str = None,
                                   updated_at_from: str = None,
                                   updated_at_to: str = None,
                                   dispatch_type: str = None,
                                   fake: bool = False,
                                   has_cis: bool = False,
                                   only_waiting_for_cancellation_approve: bool = False,
                                   only_estimated_delivery: bool = False,
                                   buyer_type: str = None,
                                   page: int = 1,
                                   page_size: int = 50) -> CampaignsOrdersResponse:
        request = CampaignsOrdersRequest(orderIds=order_ids,
                                         status=status,
                                         substatus=substatus,
                                         fromDate=from_date,
                                         toDate=to_date,
                                         supplierShipmentDateFrom=supplier_shipment_date_from,
                                         supplierShipmentDateTo=supplier_shipment_date_to,
                                         updatedAtFrom=updated_at_from,
                                         updatedAtTo=updated_at_to,
                                         dispatchType=dispatch_type,
                                         fake=fake,
                                         hasCis=has_cis,
                                         onlyWaitingForCancellationApprove=only_waiting_for_cancellation_approve,
                                         onlyEstimatedDelivery=only_estimated_delivery,
                                         buyerType=buyer_type,
                                         page=page,
                                         pageSize=page_size)
        answer: CampaignsOrdersResponse = await self._campaigns_orders_api.get(request,
                                                                               format_dict={'campaignId': campaign_id})

        return answer

    async def get_campaigns_stats_orders(self,
                                         campaign_id: Union[str, int],
                                         page_token: str = None,
                                         limit: int = 20,
                                         date_from: str = None,
                                         date_to: str = None,
                                         update_from: str = None,
                                         update_to: str = None,
                                         orders: list[int] = None,
                                         statuses: list[str] = None,
                                         has_cis: bool = False) -> CampaignsStatsOrdersResponse:
        query = CampaignsStatsOrdersQueryRequest(page_token=page_token, limit=limit)
        body = CampaignsStatsOrdersBodyRequest(dateFrom=date_from,
                                               dateTo=date_to,
                                               updateFrom=update_from,
                                               updateTo=update_to,
                                               orders=orders,
                                               statuses=statuses,
                                               hasCis=has_cis)
        answer: CampaignsStatsOrdersResponse = await self._campaigns_stats_orders_api.post(body=body,
                                                                                           query=query,
                                                                                           format_dict={'campaignId': campaign_id})

        return answer

    async def get_reports_united_marketplace_services_generate(self,
                                                               business_id: int,
                                                               campaign_ids: list[int],
                                                               date_time_from: str = None,
                                                               date_time_to: str = None,
                                                               date_from: str = None,
                                                               date_to: str = None,
                                                               year_from: int = None,
                                                               month_from: int = None,
                                                               year_to: int = None,
                                                               month_to: int = None,
                                                               placement_programs: list[str] = None,
                                                               inns: list[str] = None,
                                                               format_field: str = 'FILE',
                                                               language: str = 'RU')\
            -> ReportsUnitedMarketplaceServicesGenerateResponse:
        if placement_programs is None:
            placement_programs = ["FBS", "FBY", "DBS"]
        query = ReportsUnitedMarketplaceServicesGenerateQueryRequest(format_field=format_field, language=language)
        body = ReportsUnitedMarketplaceServicesGenerateBodyRequest(businessId=business_id,
                                                                   dateTimeFrom=date_time_from,
                                                                   dateTimeTo=date_time_to,
                                                                   dateFrom=date_from,
                                                                   dateTo=date_to,
                                                                   yearFrom=year_from,
                                                                   monthFrom=month_from,
                                                                   yearTo=year_to,
                                                                   monthTo=month_to,
                                                                   placementPrograms=placement_programs,
                                                                   inns=inns,
                                                                   campaignIds=campaign_ids)
        answer: ReportsUnitedMarketplaceServicesGenerateResponse = \
            await self._reports_united_marketplace_services_generate_api.post(body=body,
                                                                              query=query)

        return answer

    async def get_reports_info(self, report_id: str) -> ReportsInfoResponse:
        request = ReportsInfoRequest()
        answer: ReportsInfoResponse = await self._reports_info_api.get(request, format_dict={'reportId': report_id})

        return answer
