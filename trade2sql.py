import os
import sys
sys.path.append(os.getcwd())
import pandas as pd
from config.config import *
from utils import get_productids, get_date
from ato_client import ATOClient
from utils import keep_sql
from datetime import datetime

def get_trades():
	ato = ATOClient(userinfo)
	ato.login()
	accts = ato.get_stockaccountinfo()
	#unitIds = [itr['unitId'] for itr in accts]
	accounts = [itr['accountId'] for itr in accts]
	tradedf = ato.query_tradebyproduct(accounts)
	return tradedf

def combine_trades():
	tradedf = get_trades()
	productdf = get_productids()
	newdf = pd.merge(tradedf, productdf, on='unitId', how='left')	
	newdf = newdf[['dealId', 'fund_stra_id', 'dealDate', 'dealTime', 'symbol', 'side', 'dealPx', 'dealQty']]
	newdf['s_info_windcode'] = newdf['symbol'].apply(lambda x:f'{x}.SZ' if int(x) < 599999 else f'{x}.SH')
	newdf['direction'] = newdf['side'].apply(lambda x:'B' if int(x) == 1 else 'S')
	newdf['trade_dt'] = pd.to_datetime(newdf['dealDate'], format="%Y%m%d").dt.date
	newdf['trade_time'] = pd.to_datetime(newdf['dealTime'], format="%H%M%S%f").dt.floor('s')
	newdf['trade_time'] = newdf['trade_time'].dt.time
	newdf['trade_time'] = newdf.apply(lambda row: pd.Timestamp.combine(row['trade_dt'], row['trade_time']), axis=1)
	newdf = newdf.rename(columns={'fund_stra_id':'fund_id', 'dealId':'trade_id', 'dealPx':'price', 'dealQty':'qty'})
	newdf = newdf[['fund_id', 'trade_dt', 'trade_time', 's_info_windcode', 'direction', 'price', 'qty']]
	newdf.to_csv(f"trades/{get_date()}.csv")
	print(newdf)
	return newdf

def get_trades_local():
	cols = ['fund_id', 'trade_dt', 'trade_time', 's_info_windcode',
			'direction', 'price', 'qty'] 
	posdf = pd.read_csv(f'trades/2025-09-10.csv')
	return posdf[cols]

if __name__ == '__main__':
	posdf = combine_trades()
	#posdf = get_trades_local()
	keep_sql(db_config, posdf, 'fund_trades', fund_trades_mapping)
