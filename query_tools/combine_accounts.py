from config import *

def combine_accounts_byproductname(accounts):
	products = dict()
	for itr in accounts:
		keyid = str(int(itr[0]['unitId'] / 10000))
		products[keyid] = list()
	for item in accounts:
		keyid = str(int(item[0]['unitId'] / 10000))
		products[keyid].extend(item)
	print(products)
	return products



if __name__ == '__main__':
	combine_accounts_byproductname(stockaccounts)

