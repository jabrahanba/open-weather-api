from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.utils.email import send_email
import pandas as pd
import etl_functions as etl
#from dotenv import load_dotenv
#import os
from airflow.models import Variable


token = Variable.get("TOKEN")
email = Variable.get("EMAIL")
# Cargar variables de entorno
#load_dotenv("config.env")
#token = os.getenv("TOKEN")
#email = os.getenv("EMAIL")

def send_email_on_failure(context):
    subject = f"Airflow Alert: DAG {context['dag_run'].dag_id} Failed"
    message = (
        f"DAG execution failed on {context['execution_date']}. "
        "Please check the logs for more details."
    )
    send_email(
        to=[email],
        subject=subject,
        html_content=message
    )

def send_email_on_success(context):
    subject = f"Airflow Notification: DAG {context['dag_run'].dag_id} Succeeded"
    message = (
        f"DAG execution succeeded on {context['execution_date']}. "
        "The data was processed and loaded successfully."
    )
    send_email(
        to=[email],
        subject=subject,
        html_content=message
    )

# Definir el DAG
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 9, 8),
    'email_on_failure': True,
    'email': email,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': send_email_on_failure,
}

dag = DAG(
    'weather_etl_dag',
    default_args=default_args,
    schedule_interval='@daily', #'0 12 * * *',   Ejecutar todos los días a las 12:00 pm
    catchup=False
)

# Definir la tarea
#run_etl = BashOperator(
#    task_id='run_etl',
#    bash_command='dags/etl_functions.py', 
#    dag=dag,
#)

# Definir la tarea
run_etl = PythonOperator(
    task_id='run_etl',
    python_callable=etl.extract_transform_load,  # Llamar a la función ETL desde el archivo etl_functions.py
    provide_context=True,
    dag=dag,
)

# Agregar tarea para enviar correo en caso de éxito
send_success_email = PythonOperator(
    task_id='send_success_email',
    python_callable=send_email_on_success,
    provide_context=True,
    dag=dag,
)

# Definir dependencias entre tareas
run_etl >> send_success_email