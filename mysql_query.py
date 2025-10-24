from sqlalchemy import create_engine, text, MetaData, Table, select, func
from sqlalchemy.orm import sessionmaker
from typing import Optional, List, Dict, Tuple, Any, Union
import pandas as pd

class MySQLAlchemyQuery:
    def __init__(self, host: str, user: str, password: str, database: str, port: int = 3306):
        """
        使用SQLAlchemy初始化MySQL连接
        
        Args:
            host: 数据库主机地址
            user: 用户名
            password: 密码
            database: 数据库名
            port: 端口号
        """
        # 创建连接字符串
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        
        # 创建引擎
        self.engine = create_engine(
            connection_string,
            echo=False,  # 设置为True可以看到生成的SQL
            pool_size=5,
            max_overflow=10,
            pool_pre_ping=True  # 连接前检查连接是否有效
        )
        
        # 创建会话工厂
        self.Session = sessionmaker(bind=self.engine)
        
        # 元数据
        self.metadata = MetaData()
    
    def query_to_dataframe(self, query: str, params: Optional[Dict] = None) -> pd.DataFrame:
        """
        执行查询并返回DataFrame
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            pandas DataFrame
        """
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
        """
        执行原始SQL查询
        
        Args:
            query: SQL查询语句
            params: 查询参数
            
        Returns:
            结果列表
        """
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
        """
        获取表结构信息
        
        Args:
            table_name: 表名
            
        Returns:
            表结构DataFrame
        """
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
def sqlalchemy_usage():
    # 创建连接
    db = MySQLAlchemyQuery(
        host='44.241.205.126',
        user='shenzhen',
        password='dvXGXNc32Q0r7t5db6GzaPGCnYs',
        database='gbops'
    )
    
    # 查询数据到DataFrame
    df = db.query_to_dataframe("SELECT * FROM ASHAREEODPRICES WHERE TRADE_DT = %s", {'TRADE_DT': "20251023"})
    print(df.head(5))

if __name__ == "__main__":
    sqlalchemy_usage()