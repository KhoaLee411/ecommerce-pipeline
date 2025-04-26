from dagster_dbt import  load_assets_from_dbt_project, DbtCliClientResource
from dagster import file_relative_path, Definitions

DBT_PROJECT_PATH = file_relative_path(__file__, "../dbt")

dbt_assets = load_assets_from_dbt_project(
    project_dir="shopee_etl_pipeline/dbt",
    profiles_dir="shopee_etl_pipeline/dbt",
    project_name="shopee_etl_pipeline",
    
)

resources = {
    "dbt": DbtCliClientResource(
        project_dir=DBT_PROJECT_PATH,
        profiles_dir=DBT_PROFILE_PATH,
    )
}

defs = Definitions(
    assets=dbt_assets,
    resources=resources,
)
