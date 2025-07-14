from dagster import job, op
import subprocess

@op
def scrape_telegram_data():
    subprocess.run(["python", "scraper/scrape_telegram.py"], check=True)

@op
def load_raw_to_postgres():
    subprocess.run(["python", "src/load_raw_to_postgres.py"], check=True)

@op
def run_dbt_transformations():
    subprocess.run(["dbt", "run"], check=True)

@op
def run_yolo_enrichment():
    subprocess.run(["python", "src/run_yolo_detection.py"], check=True)

@job
def full_data_pipeline():
    scrape_telegram_data()
    load_raw_to_postgres()
    run_dbt_transformations()
    run_yolo_enrichment()
