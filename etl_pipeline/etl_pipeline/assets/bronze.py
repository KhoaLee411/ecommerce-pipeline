from dagster import Definitions, asset, Output, DailyPartitionsDefinition
from dagster import AssetIn, AssetOut, Output, multi_asset
from dagster import DailyPartitionsDefinition, build_schedule_from_partitioned_job
import pandas as pd
  

@asset(
    description= 'Extract data from Microsoft SQL Server',
    io_manager_key= "minio_io_manager",
    required_resource_keys={'mssql_io_manager'},
    key_prefix=['bronze','sales'],
    compute_kind = 'MinIO',
)
def bronze_customers(context)->Output:
    table  = 'Sales.Customers'
    sql = f'Select * from {table}'
    context.log.info(f"Extract data from {table}")
    
    try:
        pd_data = context.resources.mssql_io_manager.extract_data(sql)
        context.log.info(f"Extract successfully from {table}")
        
    except Exception as e:
        context.log.error(f"Error while extracting data from MySQL: {e}")
    
    return Output(
        pd_data, 
        metadata={
            "table": table, 
            "column_count": len(pd_data.columns),
            "records": len(pd_data)
            }
        )