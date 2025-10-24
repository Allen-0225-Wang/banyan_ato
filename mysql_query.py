from sqlalchemy import create_engine, text, MetaData, Table, select, func
from sqlalchemy.orm import sessionmaker
from typing import Optional, List, Dict
from datetime import datetime
import pandas as pd

class MySQLAlchemyQuery:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        # 创建连接字符串
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        
        # 创建引擎
        self.engine = create_engine(
            connection_string,
        )

        self.Session = sessionmaker(bind=self.engine)
        self.metadata = MetaData()
    
    def query_to_dataframe(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        try:
            if params:
                df = pd.read_sql(query, self.engine, params=params)
            else:
                df = pd.read_sql(query, self.engine)
            return df
        except Exception as e:
            print(f"查询失败: {e}")
            return pd.DataFrame()
    
    def execute_raw_query(self, query: str, params: Optional[Dict] = None) -> List[Dict]:
        session = self.Session()
        try:
            if params:
                result = session.execute(text(query), params)
            else:
                result = session.execute(text(query))
            
            # 转换为字典列表
            columns = result.keys()
            rows = [dict(zip(columns, row)) for row in result.fetchall()]
            return rows
        except Exception as e:
            print(f"查询执行失败: {e}")
            return []
        finally:
            session.close()
    
    def get_table_info(self, table_name: str) -> pd.DataFrame:
        query = """
        SELECT 
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY,
            EXTRA
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_NAME = %s AND TABLE_SCHEMA = DATABASE()
        """
        return self.query_to_dataframe(query, (table_name,))

# 使用示例
def fetch_eod_wind2local():
    db = MySQLAlchemyQuery(
        host='44.241.205.126',
        user='shenzhen',
        password='dvXGXNc32Q0r7t5db6GzaPGCnYs=',
        database='wind'
    )
    now = datetime.now().strftime('%Y%m%d')
    df = db.query_to_dataframe(f"SELECT * FROM ASHAREEODPRICES WHERE TRADE_DT={now}")
    df.to_csv(f'eod/ashare_eodprices_{now}.csv', index=False)
    print(f'查询结果已保存到 eod/ashare_eodprices_{now}.csv')

if __name__ == "__main__":
    fetch_eod_wind2local()