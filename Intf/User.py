import requests
import json
import ast
from Intf.Config import Config


class User(object):
    """
    用户操作类
    """
    token = ""
    hosts = ""

    def __init__(self):
        self.hosts = Config.getHosts()
        requests.packages.urllib3.disable_warnings()

    def operatorLogin(self, operatorNo, password, mac, operInfo):
        """
        登录接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8"}
        url = "https://%s/ato/user/operatorLogin" % self.hosts
        params = "{\"operatorNo\":%d,\"password\":\"%s\",\"mac\":\"%s\",\"operInfo\":\"%s\"}" % (
            operatorNo, password, mac, operInfo)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        resMsg = res.json()
        if 1 != resMsg.get("code"):
            # you can do something when login fails
            print("==Response:%s" % res.text)
            return

        self.token = resMsg.get("responseEntity").get("token")
        return self.token

    def getAcctInfo(self):
        """
        账户信息查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/user/getAcctInfo" % self.hosts

        params = "{}"
        res = requests.get(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        return res.json().get("responseEntity")

    def queryUnitPosition(self, unitAccount, marketTypes, symbol, pageNo, pageSize):
        """
        账户持仓查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/user/queryUnitPositionInfo" % self.hosts

        queryParam = {"unitAccount": unitAccount,
                      "marketTypes": marketTypes,
                      "symbol": symbol,
                      "pageNo": pageNo,
                      "pageSize": pageSize}
        data = json.loads(json.dumps(queryParam))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        res_json = res.json()
        if res_json["code"] == -1:
            print("==Response Error %s" % res_json["errorMsg"])
        return res_json["responseEntity"]

    def queryUnitTrades(self, accountIds, pageNo, pageSize):
        """
        账户成交查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/queryDealInfo" % self.hosts
        params = {"productIds" : [],
				  "unitIds" : [],
				  "accountIds" : accountIds,
				  "selfData" : 0,
				  "sides" : [],
				  "marketTypes" : [],
				  "symbol" : "",
				  "algoTypeIds" : [],
				  "sysQuoteIds" : [],
				  "sysOrderIds" : [],
				  "brokerOrderId" : [],
				  "sysDealIds" : [],
				  "dealIds" : [],
				  "dealProp" : [],
				  "orderProp" : [],
				  "pageNo" : pageNo,
				  "pageSize" : pageSize
				}
        data = json.loads(json.dumps(params))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        res_json = res.json()
        if res_json["code"] == -1:
            print("==Response Error %s" % res_json("errorMsg"))
        return res_json["responseEntity"]

    def queryUnitFund(self, unitIds:list, accountIds:list):
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/user/queryUnitFundInfo" % self.hosts
        queryParam = {"unitIds": unitIds, "accountIds": accountIds}
        data = json.loads(json.dumps(queryParam))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        return res.json().get("responseEntity")

    def queryCreditAssetInfo(self, pageNo, pageSize):
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/user/queryCreditAssetInfo" % self.hosts
        queryParam = {
					  "productIds" : [],
					  "unitIds" : [],
					  "accountIds" : [],
					  "pageNo" : pageNo,
					  "pageSize" : pageSize
					 }
        data = json.loads(json.dumps(queryParam))
        res = requests.post(url, data=json.dumps(data), headers=header, verify=False)
        print(res.json())
        return res.json().get("responseEntity")

    def queryFutureUnitPositionInfo(self, unitAccounts:list):
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/user/queryFutuUnitPositionInfo" % self.hosts
       	queryParam = {
				       "unitAccount": unitAccounts,
                       "pageNo": 1,
                       "pageSize": 100
					 }
       	data = json.loads(json.dumps(queryParam))
       	params = json.dumps(data, ensure_ascii=False)
       	res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
       	return res.json().get("responseEntity")
		







