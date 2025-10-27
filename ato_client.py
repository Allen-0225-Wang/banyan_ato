import sys
import pandas as pd
from Intf.User import User
from Intf.Order import Order
from Intf.Config import Config
from datetime import datetime


class ATOClient:

	def __init__(self, userinfo:dict):
		Config.getCfg()
		self.user = User()
		self.userinfo = userinfo
		self.date = datetime.now().date()
		self.accountinfo = None
		self.positioninfo = None
		self.stockaccountinfo = None
		self.marginaccountinfo = None
		self.futureaccountinfo = None

	def login(self):
		operatorNo = self.userinfo['operatorNo']
		password = self.userinfo['password']
		operInfo = self.userinfo['operInfo']
		mac = self.userinfo['mac']
		token = self.user.operatorLogin(operatorNo, password, mac, operInfo)
		if None == token:
			sys.exit()

	def query_account(self):
		self.accountinfo = self.user.getAcctInfo();

	def query_positionbyproduct(self, account:dict, productname:str, query_types=[1, 2]):
		symbol = ""
		pageNo = 1
		pageSize = 1000
		entity = self.user.queryUnitPosition(account, query_types, symbol, pageNo, pageSize)
		entityList = entity['pageData']
		while pageNo < entity['pageCount']:
			pageNo += 1
			entity = self.user.queryUnitPosition(account, query_types, symbol, pageNo, pageSize)
			entityList.extend(entity['pageData'])
		prodf = pd.DataFrame(entityList)
		return prodf

	def query_tradebyproduct(self, unitIds):
		pageNo = 1
		pageSize = 1000
		entity = self.user.queryUnitTrades(unitIds, pageNo, pageSize)
		entityList = entity['pageData']
		while pageNo < entity['pageCount']:
			pageNo += 1
			entity = self.user.queryUnitTrades(unitIds, pageNo, pageSize)
			entityList.extend(entity['pageData'])
		tradedf = pd.DataFrame(entityList)
		tradedf.to_csv(f'trades/{self.date}.csv')
		return tradedf

	def query_cashbyproduct(self, unitIds, acctIds):
		fundinfo = self.user.queryUnitFund(unitIds, acctIds)
		return fundinfo

	def query_futureinfo(self, unitAccounts):
		futuinfo = self.user.queryFutureUnitPositionInfo(unitAccounts)
		return futuinfo

	def query_creditinfo(self, pageNo, pageSize):
		creditasset = self.user.queryCreditAssetInfo(1, 10)
		return creditasset
			
	def get_stockaccountinfo(self):
		self.query_account()
		self.stockaccountinfo = [{'unitId':itr['unitId'], 'accountId':itr['accountId']} for itr in self.accountinfo if itr['accountType']==1 or itr['accountType']==2]
		return self.stockaccountinfo

	def get_marginaccountinfo(self):
		self.query_account()
		self.marginaccountinfo = [{'unitId':itr['unitId'], 'accountId':itr['accountId']} for itr in self.accountinfo if itr['accountType']==2]
		return self.marginaccountinfo

	def get_futureaccountinfo(self):
		self.query_account()
		self.futureaccountinfo = [{'unitId':itr['unitId'], 'accountId':itr['accountId']} for itr in self.accountinfo if itr['accountType']==3]
		return self.futureaccountinfo

if __name__ == '__main__':
	userinfo = {'operatorNo':20380003, 'password':'Jt731229', 'mac':'', 'operInfo':''}
	ato = ATOClient(userinfo)
	ato.login()
	##@query fund cash
	accts = ato.get_stockaccountinfo()
	#unitIds = [itr['unitId'] for itr in accts]
	#accounts = [itr['accountId'] for itr in accts]
	
	##@query future
	futu = ato.get_futureaccountinfo()
	futuinfo = ato.query_futureinfo(futu)

	credit = ato.query_creditinfo(1, 10)
	print(credit)

	#acctdf = ato.query_cashbyproduct(unitIds, accounts)
	#print(acctdf)

	#tradedf = ato.query_tradebyproduct(accounts)
	#print(tradedf)

	#creditdf = ato.query_creditinfo(1, 10)

	##@query fund position
	#pdf = ato.query_positionbyproduct(accts, "test")
	#pdict = pdf.set_index('unitId')[['symbol', 'holdQty']]
	#print(pdict)
