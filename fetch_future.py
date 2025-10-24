import os
import sys
sys.path.insert(0, '/home/gaoeng/mwang/workplace/new_banyan_ato/banyan_ato')
import pandas as pd
from config.config import *
from ato_client import ATOClient
from utils import get_productids, get_date, keep_sql
from datetime import datetime

def fetch_futuinfo(client: ATOClient):
	_futu = ato.get_futureaccountinfo()
	_futuinfo = ato.query_futureinfo(_futu)
	_prodf = get_productids()
	_ftdf = pd.DataFrame(_futuinfo['pageData'])
	_futudf = pd.merge(_ftdf, _prodf, on='unitId', how='left')
	_futudf = _futudf.rename(
							 columns={'symbol':'s_info_windcode', 
									  'holdQty':'shares', 
									  'preSettPx':'s_dq_close', 
									  'fund_stra_id':'fund_id'}
						    )
	_cols = ['fund_id', 'trade_dt', 's_info_windcode', 'shares', 's_dq_close', 'opdate']
	_futudf['trade_dt'] = get_date()
	_futudf['opdate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
	return _futudf[_cols]

def run(client: ATOClient):
	_fdf = fetch_futuinfo(client)
	_sqlname = 'fund_position'
	keep_sql(qa_db_config, _fdf, _sqlname, fund_position_mapping)
	print(_fdf)
	

if __name__ == '__main__':
	userinfo = {'operatorNo':20380003, 'password':'Jt731229', 'mac':'', 'operInfo':''}
	ato = ATOClient(userinfo)
	ato.login()
	run(ato)


