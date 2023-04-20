FROM apache/airflow:latest-python3.9
RUN pip install --user --upgrade pip
RUN pip install apache-airflow-providers-github
