from airflow.decorators import dag, task
from airflow.operators.bash_operator import BashOperator
import os
import shutil
import datetime

@dag(schedule_interval=None, start_date=datetime.datetime(2024, 1, 1), catchup=False, tags=['room_rental_market'])
def room_rental_market():
    # This task will run the spider
    project_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src', 'pisocompartido')
    project_dir = project_dir.replace('dags/', '')
    output_dir = os.path.join(os.getcwd(), 'include', 'pisocompartido', 'raw')
    #os.makedirs(output_dir, exist_ok=True)
    output_dir = output_dir.replace('src/pisocompartido','')
    print(output_dir)
    date = datetime.datetime.now().strftime('%Y%m%d')

    output_file = os.path.join(output_dir, f'pisocompartido_{date}_raw.json')

    extract = BashOperator(
        task_id='extract',
        bash_command=f'cd {project_dir} && scrapy crawl barcelona -o {output_file} -t json',
    )

    @task()
    def transform_and_structure():
        pass
    extract >> transform_and_structure() # Define the order of the tasks


# Instantiate the DAG
room_rental_market()