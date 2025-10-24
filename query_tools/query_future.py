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

def get_future_position_byproduct():
	user = login_ato()
	products = combine_accounts_byproductname(futureaccounts)
	for productname in products.keys():
		query_future_position(user, products[productname], productname)


def query_future_position(user, account, product):
	marketTypes = [1, 2]
	symbol = ""
	pageNo = 1
	pageSize = 1000
	entityList = []
	entity = user.queryUnitPosition(account, marketTypes, symbol, pageNo, pageSize)
	entityList.append(entity)
	while pageNo < entity["pageCount"]:
		pageNo += 1
		entity = user.queryUnitPosition(account, marketTypes, symbol, pageNo, pageSize)
		entityList.append(entity)
	print(entityList)

if __name__ == '__main__':
	get_future_position_byproduct()
