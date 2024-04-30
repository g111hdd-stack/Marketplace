from .requests import SupplierSalesRequest
from .response import SupplierSalesResponse
from .core import WBAsyncEngine
from .wb_endpoints_list import WBAPIFactory


class WBApi:

    def __init__(self, api_key: str):
        self._engine = WBAsyncEngine(api_key=api_key)
        self._api_factory = WBAPIFactory(self._engine)

        self._supplier_sales_api = self._api_factory.get_api(SupplierSalesResponse)

    async def get_supplier_sales_response(self, date_from: str, flag: int = 0) -> SupplierSalesResponse:
        """
            Продажи

            Args:
                date_from (datetime): Начальная дата отчета.
                flag (int, option): Если параметр flag=0 (или не указан в строке запроса),
                    при вызове API возвращаются данные, у которых значение поля lastChangeDate
                    (дата время обновления информации в сервисе) больше или равно переданному значению параметра dateFrom.
                    При этом количество возвращенных строк данных варьируется в интервале от 0 до примерно 100 000.
                    Если параметр flag=1, то будет выгружена информация обо всех заказах или продажах с датой,
                    равной переданному параметру dateFrom (в данном случае время в дате значения не имеет).
                    При этом количество возвращенных строк данных будет равно количеству всех заказов или продаж,
                    сделанных в указанную дату, переданную в параметре dateFrom. Default to 0.
        """
        request = SupplierSalesRequest(dateFrom=date_from, flag=flag)
        answer: SupplierSalesResponse = await self._supplier_sales_api.get(request)

        return answer
