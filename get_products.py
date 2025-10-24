import pandas as pd
from sqlalchemy import create_engine, types
from config.config import *


def get_products():
	try:
		engine = create_engine(
				f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}"
			)
		product_df = pd.read_sql(query_pp, engine)
		product_df.to_csv(f'pp.csv')
		print(product_df)
	except Exception as e:
		print(f'get_product error={e}')


if __name__ == '__main__':
	get_products()

