import logging
import requests
import datetime

from database import DbConnection
from data_classes import DataRate
from requests.exceptions import RequestException, JSONDecodeError

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)-8s %(message)s')
logger = logging.getLogger(__name__)

db_conn = DbConnection()

list_rate = []
valutes = ['USD', 'CNY']
url = 'https://www.cbr-xml-daily.ru/daily_json.js'

proxies = {
    'http': 'http://spare:kB3wia9z@176.113.83.95:7657',
    'https': 'http://spare:kB3wia9z@176.113.83.95:7657'
}

try:
    response = requests.get(url, timeout=10, proxies=proxies)
    response.raise_for_status()
    data = response.json()

    for valute in valutes:
        try:
            rate_value = round(float(data['Valute'][valute]['Value']), 4)
            list_rate.append(DataRate(date=datetime.date.today(), currency=valute, rate=rate_value))
        except KeyError:
            logger.error(f"Ошибка: Валюта {valute} не найдена в данных")
        except (ValueError, TypeError):
            logger.error(f"Ошибка: Некорректное значение курса для {valute}")
    db_conn.add_exchange_rate(list_rate=list_rate)
except RequestException as e:
    logger.error(f"Ошибка при выполнении запроса: {e}")
except JSONDecodeError:
    logger.error("Ошибка: Не удалось декодировать JSON")
except Exception as e:
    logger.error(f"Неизвестная ошибка: {e}")
