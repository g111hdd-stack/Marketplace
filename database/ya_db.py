import logging

from sqlalchemy.dialects.postgresql import insert

from .db import DbConnection, retry_on_exception
from data_classes import DataOperation, DataYaCampaigns, DataYaReport
from .models import Client, YaMain, YaCampaigns, YaReport, YaTypeReport

logger = logging.getLogger(__name__)


class YaDbConnection(DbConnection):

    @retry_on_exception()
    def add_ya_campaigns(self, list_campaigns: list[DataYaCampaigns]) -> None:
        for campaign in list_campaigns:
            existing_client = self.session.query(Client).filter_by(client_id=campaign.client_id).first()
            if existing_client:
                new_campaign = YaCampaigns(campaign_id=campaign.campaign_id,
                                           client_id=campaign.client_id,
                                           name=campaign.name,
                                           placement_type=campaign.placement_type)
                self.session.merge(new_campaign)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_operation(self, list_operations: list[DataOperation]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_operations (list[DataOperation]): Список данных об операциях.
        """
        for row in list_operations:
            stmt = insert(YaMain).values(
                client_id=row.client_id,
                accrual_date=row.accrual_date,
                type_of_transaction=row.type_of_transaction,
                vendor_code=row.vendor_code,
                posting_number=row.posting_number,
                delivery_schema=row.delivery_schema,
                sku=row.sku,
                sale=row.sale,
                quantities=row.quantities
            ).on_conflict_do_update(
                index_elements=['accrual_date', 'client_id', 'type_of_transaction', 'posting_number', 'sku'],
                set_={'sale': row.sale,
                      'quantities': row.quantities}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")

    @retry_on_exception()
    def add_ya_report(self, list_reports: list[DataYaReport]) -> None:
        """
            Добавление в базу данных записи об операциях с товарами.

            Args:
                list_reports (list[DataYaReport]): Список данных об операциях.
        """
        type_services = set(self.session.query(YaTypeReport.operation_type,
                                               YaTypeReport.service).all())
        for row in list_reports:
            if (row.operation_type, row.service or '') not in type_services:
                new_type = YaTypeReport(operation_type=row.operation_type,
                                        service=row.service or '',
                                        type_name='new')
                self.session.add(new_type)
                type_services.add((row.operation_type, row.service or ''))
            stmt = insert(YaReport).values(
                client_id=row.client_id,
                campaign_id=row.campaign_id,
                posting_number=row.posting_number or '',
                operation_type=row.operation_type,
                vendor_code=row.vendor_code or '',
                service=row.service or '',
                date=row.date,
                cost=row.cost
            ).on_conflict_do_update(
                index_elements=['client_id', 'campaign_id', 'date', 'posting_number', 'vendor_code', 'operation_type', 'service'],
                set_={'cost': row.cost}
            )
            self.session.execute(stmt)
        self.session.commit()
        logger.info(f"Успешное добавление в базу")
