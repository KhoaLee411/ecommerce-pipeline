from . import assets
from dagster import Definitions,load_assets_from_modules
from .resources.mssql_io_manager import MSQLIOManager
from .resources.minio_io_manager import MinIOIOManager
from dagster import Definitions, ScheduleDefinition,AssetSelection, define_asset_job,DailyPartitionsDefinition, build_schedule_from_partitioned_job


MSSQL_CONFIG = {
    "host": "localhost",  
    "port": 1433,
    "database": "WideWorldImporters",
    "user": "DESKTOP-HBH07UF\ADMIN",
    "password": "admin123",
}

MINIO_CONFIG = {
    "endpoint": "minio:9000", 
    "bucket_name": "warehouse",
    "access_key": "minio",
    "secret_key": "minio123",
    "secure": False
}
PSQL_CONFIG = {
    "host": "de_psql",
    "port": 5432,
    "database": "postgres",
    "user": "admin",
    "password": "admin123",
}

# Định nghĩa các tài nguyên
resources = {
    "mssql_io_manager": MSQLIOManager(MSSQL_CONFIG),
    "minio_io_manager": MinIOIOManager(MINIO_CONFIG)
}

assets = load_assets_from_modules([assets])  

definition = Definitions(
    assets=assets,  # Kết hợp assets
    resources=resources,
    #schedules=[etl_schedule]
)
