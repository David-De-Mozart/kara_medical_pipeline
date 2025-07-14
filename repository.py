from dagster import repository
from dagster_pipeline import full_data_pipeline  # adjust import if your file name differs

@repository
def kara_pipeline_repo():
    return [full_data_pipeline]