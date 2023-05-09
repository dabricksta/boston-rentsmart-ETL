from os import remove
from airflow import DAG 
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime

"""
DAG to extract Boston RentSmart data, load into AWS S3, and copy to AWS Redshift
"""

# Output name of extracted file. This be passed to each 
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")

# Run our DAG daily and ensures DAG run will kick off 
# once Airflow is started, as it will try to "catch up"
# TODO why are there 2 start_date
schedule_interval = '@daily' 
start_date = days_ago(1)

default_args = {"owner": "airflow"
                , "depends_on_past": False
                , 'start_date': today()
                , "retries": 1
                , 'retry_delay': timedelta(minutes = 5)
                }

with DAG(
    dag_id='boston_rentsmart_dag',
    description ='Boston RentSmart ELT',
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=True,
    max_active_runs=1,
    tags=['BostonRentSmartETL'],
) as dag:

    extract_data = PythonOperator(
        task_id = 'extract_data'
        , dag = dag
        , python_callable = extract_data
    )
    extract_data.doc_md = 'Extract Boston RentSmart data and store as CSV'
    
    # upload_to_s3 = BashOperator(
    #     task_id = 'upload_to_s3',
    #     bash_command = f'python /opt/airflow/extraction/upload_aws_s3_etl.py {output_name}',
    #     dag = dag,
    # )
    # upload_to_s3.doc_md = 'Upload Reddit CSV data to S3 bucket'
    
    # copy_to_redshift = BashOperator(
    #     task_id = 'copy_to_redshift',
    #     bash_command = f"python /opt/airflow/extraction/upload_aws_redshift_etl.py {output_name}",
    #     dag = dag,
    # )
    # copy_to_redshift.doc_md = 'Copy S3 CSV file to Redshift table'
    
    clean_data = PythonOperator(
        task_id = 'clean_data'
        , dag = dag
        , python_callable = clean_data
    )
    clean_data.doc_md = 'Clean data and store as CSV'


# extract_data >> upload_to_s3 >> copy_to_redshift
extract_data >> clean_data