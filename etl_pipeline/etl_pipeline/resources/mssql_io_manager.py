import pandas as pd
from dagster import IOManager, OutputContext, InputContext
from sqlalchemy import create_engine
from contextlib import contextmanager
from sqlalchemy import text
from datetime import datetime

# Thiết lập kết nối tới Microsoft SQL Server
@contextmanager
def connect_mssql(config):
    conn_info = (
        f"mssql+pyodbc://{config['user']}:{config['password']}@"
        f"{config['host']}:{config['port']}/{config['database']}?driver={config['driver']}"
    )
    db_conn = create_engine(conn_info)
    try:
        yield db_conn
    except Exception as e:
        raise e

# Lớp IOManager cho SQL Server
class MSSQLIOManager(IOManager):
    def __init__(self, config):
        self._config = config

    def handle_output(self, context: OutputContext, obj: pd.DataFrame):
        schema, table = context.asset_key.path[-2], context.asset_key.path[-1]
        with connect_mssql(self._config) as engine:
            # Ghi dữ liệu vào SQL Server
            obj.to_sql(table, con=engine, schema=schema, if_exists="append", index=False)

    def load_input(self, context: InputContext) -> pd.DataFrame:
        schema, table = context.asset_key.path[-2], context.asset_key.path[-1]
        sql = f"SELECT * FROM {schema}.{table}"
        return self.extract_data(sql)

    def extract_data(self, sql: str) -> pd.DataFrame:
        with connect_mssql(self._config) as db_conn:
            # Thực hiện truy vấn SQL và trả về DataFrame
            pd_data = pd.read_sql_query(sql, db_conn)
            return pd_data
