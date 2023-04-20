from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.github.sensors.github import BaseGithubRepositorySensor
from datetime import datetime, timedelta
import subprocess

# Define default_args and DAG settings
default_args = {
    'owner': 'my_owner',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1,0,0,30),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'github_commits_dag_new',
    default_args=default_args,
    schedule_interval=timedelta(minutes=30),  # polling interval for checking commits
)

# Callback function to process the new commits
def process_commits(**kwargs):
    # Retrieve the commit information using GitHub API
    owner = 'kaushal-faclon'
    repo = 'airflow-github'
    branch = 'master'  # specify the branch to monitor
    url = f'https://api.github.com/repos/{owner}/{repo}/commits?sha={branch}'
    # ... rest of the code ...

    # Pull the latest changes from the remote repository
    local_repo_path = './'
    subprocess.run(['git', '-C', local_repo_path, 'pull'])

    # ... rest of the code ...

# Define the GitHub Repository Sensor
github_sensor = BaseGithubRepositorySensor(
    task_id='github_sensor',
    github_conn_id='github_connection',  # specify the GitHub connection configured in step 2
    # repo='kaushal-faclon/airflow-github',  # specify the repository in the format owner/repo
    result_processor=process_commits,  # specify the callback function to process the commits
    mode='poke',  # use poke mode for periodic polling
    timeout=600,  # specify the timeout for polling in seconds
    # branch='master',  # specify the branch to monitor
    dag=dag,
)

# Set up the task dependencies
github_sensor
