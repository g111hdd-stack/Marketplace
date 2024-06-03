import asyncio
import nest_asyncio
import logging

from datetime import datetime, timedelta
from sqlalchemy.exc import OperationalError

from data_classes import DataWBReport
from wb_sdk.wb_api import WBApi
from database import WBDbConnection

nest_asyncio.apply()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)


async def get_report(db_conn: WBDbConnection, client_id: str, api_key: str, date_from: datetime,
                     date_to: datetime) -> bool:
    list_report = []
    api_user = WBApi(api_key=api_key)
    answer = await api_user.get_supplier_report_detail_by_period(date_from=date_from.isoformat(),
                                                                 date_to=date_to.isoformat())
    if answer:
        if answer.result:
            for report in answer.result:
                if report.sale_dt.date() > date_to.date():
                    continue
                list_report.append(DataWBReport(realizationreport_id=str(report.realizationreport_id),
                                                gi_id=str(report.gi_id),
                                                sku=str(report.nm_id),
                                                brand=report.brand_name,
                                                vendor_code=report.sa_name,
                                                size=report.ts_name,
                                                barcode=report.barcode,
                                                doc_type_name=report.doc_type_name,
                                                quantity=report.quantity,
                                                retail_price=report.retail_price,
                                                retail_amount=report.retail_amount,
                                                sale_percent=report.sale_percent,
                                                commission_percent=report.commission_percent,
                                                office_name=report.office_name,
                                                supplier_oper_name=report.supplier_oper_name,
                                                order_date=report.order_dt.date(),
                                                sale_date=report.sale_dt.date(),
                                                operation_date=report.rr_dt.date(),
                                                shk_id=str(report.shk_id),
                                                retail_price_withdisc_rub=round(report.retail_price_withdisc_rub, 2),
                                                delivery_amount=report.delivery_amount,
                                                return_amount=report.return_amount,
                                                delivery_rub=round(report.delivery_rub, 2),
                                                gi_box_type_name=report.gi_box_type_name,
                                                product_discount_for_report=round(report.product_discount_for_report, 2),
                                                supplier_promo=round(report.supplier_promo, 2),
                                                order_id=str(report.rid),
                                                ppvz_spp_prc=round(report.ppvz_spp_prc, 2),
                                                ppvz_kvw_prc_base=round(report.ppvz_kvw_prc_base, 2),
                                                ppvz_kvw_prc=round(report.ppvz_kvw_prc, 2),
                                                sup_rating_prc_up=round(report.sup_rating_prc_up, 2),
                                                is_kgvp_v2=round(report.is_kgvp_v2, 2),
                                                ppvz_sales_commission=round(report.ppvz_sales_commission, 2),
                                                ppvz_for_pay=round(report.ppvz_for_pay, 2),
                                                ppvz_reward=round(report.ppvz_reward, 2),
                                                acquiring_fee=round(report.acquiring_fee, 2),
                                                acquiring_bank=report.acquiring_bank,
                                                ppvz_vw=round(report.ppvz_vw, 2),
                                                ppvz_vw_nds=round(report.ppvz_vw_nds, 2),
                                                ppvz_office_id=str(report.ppvz_office_id),
                                                ppvz_office_name=report.ppvz_office_name,
                                                ppvz_supplier_id=str(report.ppvz_supplier_id),
                                                ppvz_supplier_name=report.ppvz_supplier_name,
                                                ppvz_inn=report.ppvz_inn,
                                                declaration_number=report.declaration_number,
                                                bonus_type_name=report.bonus_type_name,
                                                sticker_id=report.sticker_id,
                                                site_country=report.site_country,
                                                penalty=round(report.penalty, 2),
                                                additional_payment=round(report.additional_payment, 2),
                                                rebill_logistic_cost=round(report.rebill_logistic_cost, 2),
                                                rebill_logistic_org=report.rebill_logistic_org,
                                                kiz=report.kiz,
                                                storage_fee=round(report.storage_fee, 2),
                                                deduction=round(report.deduction, 2),
                                                acceptance=round(report.acceptance, 2),
                                                posting_number=report.srid))

    logger.info(f"Количество записей: {len(list_report)}")
    db_conn.add_wb_report_entry(client_id=client_id, list_report=list_report)

    if len(list_report) > 0:
        return True
    return False


async def main_wb_report(retries: int = 6) -> None:
    try:
        db_conn = WBDbConnection()
        db_conn.start_db()
        clients = db_conn.get_clients(marketplace="WB")

        now_date = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)

        for client in clients:
            last_date = db_conn.get_last_sale_date_wb_report(client_id=client.client_id)
            date_from = datetime(year=last_date.year, month=last_date.month, day=last_date.day,
                                 hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)

            current_weekday = date_from.weekday()
            days_to_last_monday = 7 - (current_weekday + 1) % 7
            date_to = date_from + timedelta(days=days_to_last_monday + 1) - timedelta(microseconds=1)

            if date_to.date() < now_date.date():
                logger.info(f"Получение отчёта для {client.name_company} за период от {date_from.date().isoformat()} до {date_to.date().isoformat()}")
                check = await get_report(db_conn=db_conn,
                                         client_id=client.client_id,
                                         api_key=client.api_key,
                                         date_from=date_from,
                                         date_to=date_to)
            else:
                check = False

            if check:
                last_date_report = db_conn.get_last_sale_date_wb_report(client_id=client.client_id)
                db_conn.add_wb_operation_for_not_report(client_id=client.client_id, date_to=last_date_report)

        db_conn.add_wb_operation_for_report()

    except OperationalError:
        logger.error(f'Не доступна база данных. Осталось попыток подключения: {retries - 1}')
        if retries > 0:
            await asyncio.sleep(10)
            await main_wb_report(retries=retries - 1)
    except Exception as e:
        logger.error(f'{e}')

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_wb_report())
    loop.stop()
