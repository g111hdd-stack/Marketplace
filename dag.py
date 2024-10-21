from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

activate = 'source /home/Marketplace/venv/bin/activate && python /home/Marketplace/'

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 10, 18),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'scripts',
    default_args=default_args,
    description='scripts dag',
    schedule_interval='15 3 * * *',
    catchup=False,
)

check_updates = BashOperator(
    task_id='check_updates',
    bash_command='cd /home/Marketplace && git fetch && git status && git pull',
    dag=dag,
)

main_oz = BashOperator(
    task_id='main_oz',
    bash_command=f'{activate}main_oz.py',
    dag=dag,
)

oz_services = BashOperator(
    task_id='oz_services',
    bash_command=f'{activate}oz_services.py',
    dag=dag,
)

oz_advert_company = BashOperator(
    task_id='oz_advert_company',
    bash_command=f'{activate}oz_advert_company.py',
    dag=dag,
)

main_wb = BashOperator(
    task_id='main_wb',
    bash_command=f'{activate}main_wb.py',
    dag=dag,
)

wb_orders = BashOperator(
    task_id='wb_orders',
    bash_command=f'{activate}wb_orders.py',
    dag=dag,
)

wb_report = BashOperator(
    task_id='wb_report',
    bash_command=f'{activate}wb_report.py',
    dag=dag,
)

wb_storage = BashOperator(
    task_id='wb_storage',
    bash_command=f'{activate}wb_storage.py',
    dag=dag,
)

wb_acceptance = BashOperator(
    task_id='wb_acceptance',
    bash_command=f'{activate}wb_acceptance.py',
    dag=dag,
)

wb_advert_company = BashOperator(
    task_id='wb_advert_company',
    bash_command=f'{activate}wb_advert_company.py',
    dag=dag,
)

google_sheet_report = BashOperator(
    task_id='google_sheet_report',
    bash_command=f'{activate}google_sheet_report.py',
    dag=dag,
)

main_ya = BashOperator(
    task_id='main_ya',
    bash_command=f'{activate}main_ya.py',
    dag=dag,
)

ya_report = BashOperator(
    task_id='ya_report',
    bash_command=f'{activate}ya_report.py',
    dag=dag,
)

check_updates >> main_oz >> oz_services >> oz_advert_company

check_updates >> main_wb >> wb_orders >> wb_report >> wb_storage >> wb_acceptance >> wb_advert_company >> google_sheet_report

check_updates >> main_ya >> ya_report
