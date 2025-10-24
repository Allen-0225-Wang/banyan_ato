import os
import sys
sys.path.insert(0, '/home/gaoeng/mwang/workplace/new_banyan_ato/banyan_ato')
import pandas as pd
import akshare as ak
from datetime import datetime
from mysql_query import fetch_eod_wind2local


def stats_file():
	if not os.path.exists('pre_closeprice'):
		os.mkdir('pre_closeprice')

def get_stock_close_prices():
	stock_spot = ak.stock_zh_a_spot_em()
	hnow = datetime.now().hour
	if hnow >= 15:
		close_price_df = stock_spot[['代码', '最新价']]
		close_price_df = close_price_df.rename(index={'代码':'symbol', '最新价':'preclose'})
		print(f'houroftime={hnow} fetch prelast')
	else:
		close_price_df = stock_spot[['代码', '昨收']]
		close_price_df = close_price_df.rename(index={'代码':'symbol', '昨收':'preclose'})
		print(f'houroftime={hnow} fetch preclose')
	ddate = datetime.now().date()
	stats_file()
	close_price_df.to_csv(f'pre_closeprice/{ddate}.csv')
	return close_price_df

def get_stock_close_prices_wind():
	fetch_eod_wind2local()
	ddate = datetime.now().strftime('%Y%m%d')
	file_path = f'eod/ashare_eodprices_{ddate}.csv'
	eod_df = pd.read_csv(file_path, dtype={'S_INFO_WINDCODE':str, 'S_DQ_PRECLOSE':float})
	close_price_df = eod_df[['S_INFO_WINDCODE', 'S_DQ_PRECLOSE']]
	close_price_df = close_price_df.rename(columns={'S_INFO_WINDCODE':'symbol', 'S_DQ_PRECLOSE':'preclose'})
	return close_price_df

def get_stock_close_local():
	ddate = datetime.now().date()
	file_path = f'pre_closeprice/{ddate}.csv'
	if not os.path.exists(file_path):
		get_stock_close_prices()
	predf = pd.read_csv(file_path, names=['symbol', 'preclose'], skiprows=1, dtype={'symbol':str, 'preclose':float})
	return predf

def get_productids():
	pdf = pd.read_csv(f'config/products.csv')[['unitId', 'fund_stra_id']]
	return pdf

if __name__ == "__main__":
	# pdf = get_stock_close_local()
	#pdf = get_stock_close_prices()
	pdf = get_stock_close_prices_wind
	print(pdf)
