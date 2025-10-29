import sys
sys.path.insert(0, '/home/gaoeng/mwang/workplace/new_banyan_ato/banyan_ato')
import pandas as pd
from ato_client import ATOClient
from fetch_preclose import get_stock_close_local
from config.config import *
from datetime import datetime, date, timedelta
from sqlalchemy import create_engine, types
from utils import keep_sql, get_productids
from fetch_future import fetch_futuinfo


def combine_cols(posdf, account_type):
	price_df = get_stock_close_local()
	fundid_df = get_productids()
	tradetime = datetime.now()
	tradedate = tradetime.date()
	newdf = pd.merge(posdf, price_df, on='symbol', how='left')
	newdf = pd.merge(newdf, fundid_df, on='unitId', how='left')
	newdf['trade_dt'] = tradedate
	newdf['opdate'] = tradetime.strftime('%Y-%m-%d %H:%M:%S')
	newdf = newdf[['trade_dt', 'fund_stra_id', 'symbol', 'holdQty', 'preclose', 'opdate']]
	newdf = newdf.rename(columns={'symbol':'s_info_windcode', 'fund_stra_id':'fund_id', 
								  'holdQty':'shares', 'preclose':'s_dq_close'})
	newdf.to_csv(f'positions/{tradedate}_{account_type}.csv')
	return newdf if account_type < 3 else newdf.query('fund_id<0')

def get_posinfo(account_type=1):
	ato = ATOClient(userinfo)
	ato.login()
	if account_type == 1:
		accts = ato.get_stockaccountinfo()
		pdf = ato.query_positionbyproduct(accts, "test")
	elif account_type == 2:
		acctsinfo = ato.get_marginaccountinfo()
		accts = [itr['accountId'] for itr in acctsinfo]
		pdf = ato.query_credictdebtdetail_byaccounts(accts)
	elif account_type == 3:
		accts = ato.get_futureaccountinfo()
		pdf = ato.query_futureinfo(accts)
		pdf = pdf.groupby(['unitId', 'symbol']).agg({'holdQty' : 'sum'}).reset_index()
	else:
		pdf = pd.DataFrame()
	
	pdict = pdf[['unitId', 'symbol', 'holdQty']]
	pdict['symbol'] = pdict['symbol'].apply(lambda x : f'{x}.SH' if int(x) > 599999 else f'{x}.SZ') if account_type < 3 else pdict['symbol']
	pdf = combine_cols(pdict, account_type)
	return pdf

def get_cashinfo(account_type=1):
	ato = ATOClient(userinfo)
	ato.login()
	accts = ato.get_stockaccountinfo()
	cash_df = ato.query_cashbyproduct(accts)
	print(cash_df)


def get_posinfo_local(date):
	return pd.read_csv(f'positions/{date}.csv')

def main():
	#pdf = get_posinfo(account_type=1)
	#hnow = datetime.now().hour
	#sqlname = 'fund_position' if hnow >= 15 else 'fund_initial_position'
	#keep_sql(db_config, pdf, sqlname, fund_position_mapping)

	## special handle margin account
	#pdf = get_posinfo(account_type=3)
	#sqlname = 'fund_margin_position'
	#print(pdf)
	# keep_sql(db_config, pdf, sqlname, fund_position_mapping)
	#account_types = {1 : 'fund_position', 2 : 'fund_margin_position', 3 : 'fund_margin_position'}
	#for _k, _v in account_types.items():
		#pdf = get_posinfo(_k)
		#keep_sql(db_config, pdf, _v, fund_position_mapping)
	get_cashinfo()

if __name__ == '__main__':
	main()
