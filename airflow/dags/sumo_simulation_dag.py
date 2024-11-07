from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

# Function to run the SUMO simulation
def run_sumo_simulation(file_name):
    os.system(f'python3 /opt/airflow/sumo_work/run_traci1.py {file_name}')

# Define DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    'sumo_simulation_dag_v2',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Run the SUMO simulation for different scenarios
    run_morning_peak_simulation = PythonOperator(
        task_id='run_morning_peak_simulation',
        python_callable=run_sumo_simulation,
        op_args=['morning_peak_8AM.rou.xml'],
    )

    run_evening_peak_simulation = PythonOperator(
        task_id='run_evening_peak_simulation',
        python_callable=run_sumo_simulation,
        op_args=['evening_peak_6PM.rou.xml'],
    )

    run_off_peak_simulation = PythonOperator(
        task_id='run_off_peak_simulation',
        python_callable=run_sumo_simulation,
        op_args=['off_peak_2AM.rou.xml'],
    )

    run_morning_peak_simulation >> run_evening_peak_simulation >> run_off_peak_simulation
