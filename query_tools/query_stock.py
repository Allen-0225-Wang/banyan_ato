import sys
import pandas as pd
from combine_accounts import combine_accounts_byproductname
from Intf.User import User
from Intf.Order import Order
from Intf.Config import Config
from config import *


def login_ato():
	Config.getCfg()
	user = User()
	operatorNo = 20380003
	password = "Jt731229"
	#mac = "00:50:56:83:17:58"
	#operInfo = "内网IP:,外网IP:,MAC:00:50:56:83:17:58,设备名称:WIN10PRO-249"
	token = user.operatorLogin(operatorNo, password, '', '')
	if None == token:
		print("login fail")
		sys.exit()
	return user

## 获取产品列表
def get_account_info():
	ato_user = login_ato()
	entity = ato_user.getAcctInfo()
	stock_account_lis = list()
	future_account_lis = list()
	account_lis = list()
	for itr in entity:
		actlis = list()
		actdic = dict()
		actdic['unitId'] = itr['unitId']
		actdic['accountId'] = itr['accountId']
		actlis.append(actdic)
		if itr['accountType'] == 1:
			stock_account_lis.append(actlis)
		elif itr['accountType'] == 3:
			future_account_lis.append(actlis)
		account_lis.append(actlis)
	print(stock_account_lis)
	print(future_account_lis)
	print(account_lis)
	return ato_user, stock_account_lis, future_account_lis

def get_position_info_all():
	ato_user, stkaccounts, futureaccounts = get_account_info()
	for acct in stkaccounts:
		positions = get_position_info(ato_user, acct, [])

## 根据产品名查询持仓
def get_position_byproduct():
	ato_user, stkaccounts, futureaccounts = get_account_info()
	products = combine_accounts_byproductname(stockaccounts) 
	for product in products:
		print(products[product])
		get_position_info(ato_user, products[product], [], product)

def get_position_info(ato_user, account, query_markettypes, productname):
	#marketTypes = [1, 2]
	symbol = ""
	pageNo = 1
	pageSize = 1000
	entity = ato_user.queryUnitPosition(account, query_markettypes, symbol, pageNo, pageSize)
	entityList = entity['pageData']
	while pageNo < entity["pageCount"]:
		pageNo += 1
		entity = ato_user.queryUnitPosition(account, query_markettypes, symbol, pageNo, pageSize)
		entityList.extend(entity['pageData'])
	posdf = pd.DataFrame(entityList)
	posdf.to_csv(f'positions/{productname}.csv')
	return entityList


if __name__ == '__main__':
	#get_position_byproduct()
	get_account_info()
