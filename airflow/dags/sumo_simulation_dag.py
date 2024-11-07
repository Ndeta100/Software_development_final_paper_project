from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta
import os

# Function to parse TomTom data
def parse_tomtom_data():
    os.system('python3 /opt/airflow/sumo_work/parse_tom_tom.py')

# Function to run the SUMO simulation
def run_sumo_simulation(file_name):
    os.system(f'python3 /opt/airflow/sumo_work/run_traci_local.py {file_name}')

# Function to output results to summary.csv
def output_results():
    os.system('python3 /opt/airflow/sumo_work/extract_from_summary.py > /opt/airflow/sumo_work/summary.csv')

# Function to extract data from the summary
def extract_data():
    os.system('python3 /opt/airflow/sumo_work/extract_from_summary.py')

# Define DAG arguments
default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 10, 30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Define DAG
with DAG(
    'sumo_simulation_dag_v3',
    default_args=default_args,
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Task 1: Parse TomTom data
    parse_tomtom_task = PythonOperator(
        task_id='parse_tomtom_data',
        python_callable=parse_tomtom_data,
    )

    # Task 2: Run the SUMO simulation for different scenarios
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

    # Task 3: Output results to summary.csv
    output_results_task = PythonOperator(
        task_id='output_results',
        python_callable=output_results,
    )

    # Task 4: Extract data from the summary
    extract_data_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    # Define task dependencies
    parse_tomtom_task >> run_morning_peak_simulation >> run_evening_peak_simulation >> run_off_peak_simulation >> output_results_task >> extract_data_task
