import os
import json
import pandas as pd
import akshare as ak
from datetime import datetime
from sqlalchemy import create_engine, types


def get_date():
	return datetime.now().date()

def get_productids():
	pdf = pd.read_csv(f'config/products.csv')[['unitId', 'fund_stra_id']]
	return pdf

def keep_sql(db_config:json, table:pd.DataFrame, tablename:str, tablemap:json, if_exists='append'):
	try:
		engine = create_engine(
				f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
			)
		table.to_sql(
					 name=tablename,
					 con=engine,
					 if_exists=if_exists,
					 index=False,
					 dtype=tablemap,
					 chunksize=1000,
					 method='multi'
					)
	except Exception as e:
		print(f'{tablename} keep sql failed. Exception={e}')
	print(f'{tablename} keep sql success')

if __name__ == '__main__':
	get_productids()


