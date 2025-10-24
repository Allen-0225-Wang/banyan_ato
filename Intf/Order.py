import requests
import json
import ast
from requests_toolbelt import MultipartEncoder
from pathlib import Path
from Intf.Config import Config


class Order(object):
    """
    订单操作类
    """
    token = ""
    hosts = ""

    def __init__(self, token):
        self.token = token
        self.hosts = Config.getHosts()

    def __savefile__(self, fileType, text):
        """
        文件单模板保存接口
        """
        if 1 == fileType:
            with open("template.csv", "a", encoding="GBK") as f:
                f.write(text)
                f.closed
        elif 2 == fileType:
            with open("template.xslx", "a", encoding="GBK") as f:
                f.write(text)
                f.closed
        else:
            return False

        return True

    def fileTemplateDownLoad(self, fileType):
        """
        文件单模板下载接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/fileTemplateDownLoad" % self.hosts
        queryParam = {"fileType": fileType}
        data = json.loads(json.dumps(queryParam))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        if 200 != res.status_code:
            print("[ERROR]HTTP request failed:%s" % res.status_code)
            return False

        return self.__savefile__(fileType, res.text)

    def fileOrderUpload(self, file):
        """
        文件单上传接口
        """
        orderFile = Path(file)
        if False == orderFile.exists():
            return False

        url = "https://%s/ato/order/fileOrderUpload" % self.hosts
        multipart_encoder = MultipartEncoder(fields={"Content-Type": "application/octet-stream",
                                                     "file": (file, open(file, 'rb'), 'application/octet-stream')})

        res = requests.post(url, data=multipart_encoder, headers={"Accept": "*/*", "Authorization": self.token,
                                                                  'Content-Type': multipart_encoder.content_type},
                            verify=False)

        # handle error
        resJson = res.json()
        if 1 != resJson.get("code"):
            # you can do something when upload fails
            print("==Response:%s" % res.text)
            return False

        responseEntity = resJson.get("responseEntity")
        if 0 != responseEntity.get("failNum"):
            print("file %s" % responseEntity.get("failReason"))
            return False

        return True

    def fileOrderSubmit(self, errorContinue):
        """
        文件单提交接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/fileOrderSubmit" % self.hosts
        data = json.loads(json.dumps(errorContinue))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)

        resJson = res.json()
        if 1 != resJson.get("code"):
            # you can do something when submit fails
            print("==Response:%s" % res.text)
            return False

        responseEntity = resJson.get("responseEntity")
        print("%s" % responseEntity)
        return True

    def algoOrderCreate(self, algoOrder):
        """
        算法单委托接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/algoOrderCreate" % self.hosts
        data = json.loads(json.dumps(algoOrder))
        params = json.dumps(data, ensure_ascii=False)
        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        res_json = res.json()
        responseEntity = res_json["responseEntity"]
        has_error = False
        print("==status_code:%s" % res.status_code)
        print("==Response:%s" % res.text)
        if 1 != res_json.get("code"):
            print("==Response:%s" % res.text)
            has_error = True
        else:
            for value in responseEntity:
                if value["errCode"] != 0:
                    print("==母单存在异常:%s!!" % value.text)
                    has_error = True
        return not has_error

    def algoOrderOperation(self, algoOrder):
        """
        算法单操作接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/algoOrderOperation" % self.hosts
        data = json.loads(json.dumps(algoOrder))
        params = json.dumps(data, ensure_ascii=False)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        print("==status_code:%s" % res.status_code)
        print("==Response:%s" % res.text)

    def algoOrderModify(self, modifyList):
        """
        算法单修改接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/algoOrderModify" % self.hosts
        data = json.loads(json.dumps(modifyList))
        params = json.dumps(data, ensure_ascii=False)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        print("==status_code:%s" % res.status_code)
        print("==Response:%s" % res.text)

    def queryAlgoOrderInfo(self, algoOrderCondition):
        """
        算法单查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/queryAlgoOrderInfo" % self.hosts
        data = json.loads(json.dumps(algoOrderCondition))
        params = json.dumps(data, ensure_ascii=False)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)
        print("==status_code:%s" % res.status_code)
        print("==Response:%s" % res.text)
        return res.json().get("responseEntity")

    def queryOrderInfo(self, orderCondition):
        """
        订单查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/queryOrderInfo" % self.hosts
        data = json.loads(json.dumps(orderCondition))
        params = json.dumps(data, ensure_ascii=False)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)

        return res.json().get("responseEntity")

    def queryDealInfo(self, dealCondition):
        """
        成交查询接口
        """
        header = {"Accept": "*/*", "Content-Type": "application/json;charset=utf-8", "Authorization": self.token}
        url = "https://%s/ato/order/queryDealInfo" % self.hosts
        data = json.loads(json.dumps(dealCondition))
        params = json.dumps(data, ensure_ascii=False)

        res = requests.post(url, data=json.dumps(ast.literal_eval(params)), headers=header, verify=False)

        return res.json().get("responseEntity")
