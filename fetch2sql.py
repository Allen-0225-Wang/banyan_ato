import sys
sys.path.insert(0, '/home/gaoeng/mwang/workplace/new_banyan_ato/banyan_ato')
import pandas as pd
from ato_client import ATOClient
from fetch_preclose import get_stock_close_local
from config.config import *
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, types
from utils import keep_sql, get_productids


def combine_cols(posdf):
	price_df = get_stock_close_local()
	print(price_df)
	fundid_df = get_productids()
	tradetime = datetime.now()
	tradedate = tradetime.date()
	newdf = pd.merge(posdf, price_df, on='symbol', how='left')
	newdf = pd.merge(newdf, fundid_df, on='unitId', how='left')
	newdf['symbol'] = newdf['symbol'].apply(lambda x : f'{x}.SH' if int(x) > 599999 else f'{x}.SZ')
	newdf['trade_dt'] = tradedate
	newdf['opdate'] = tradetime.strftime('%Y-%m-%d %H:%M:%S')
	print(newdf)
	newdf = newdf[['trade_dt', 'fund_stra_id', 'symbol', 'holdQty', 'preclose', 'opdate']]
	newdf = newdf.rename(columns={'symbol':'s_info_windcode', 'fund_stra_id':'fund_id', 
								  'holdQty':'shares', 'preclose':'s_dq_close'})
	newdf.to_csv(f'positions/{tradedate}.csv')
	return newdf

def get_posinfo():
	ato = ATOClient(userinfo)
	ato.login()
	accts = ato.get_stockaccountinfo()
	pdf = ato.query_positionbyproduct(accts, "test")
	pdict = pdf[['unitId', 'symbol', 'holdQty']]
	pdict.to_csv(f'positions/unitId.csv')
	pdf = combine_cols(pdict)
	return pdf

def get_posinfo_local(date):
	return pd.read_csv(f'positions/{date}.csv')

def main():
	pdf = get_posinfo()
	#pdf = get_posinfo_local('2025-09-23')[['trade_dt','fund_id','s_info_windcode','shares','s_dq_close','opdate']]
	hnow = datetime.now().hour
	print(pdf)
	#sqlname = 'fund_position' if hnow >= 15 else 'fund_initial_position'
	# keep_sql(db_config, pdf, sqlname, fund_position_mapping)


if __name__ == '__main__':
	main()
