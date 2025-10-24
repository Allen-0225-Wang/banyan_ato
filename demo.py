import sys
from Intf.User import User
from Intf.Order import Order
from Intf.Config import Config

if __name__ == '__main__':
    # get http server config
    Config.getCfg()

    # the demo shows you how to use the API
    # how to assign the function parameters can be found in the documentation ATO-http接口说明

    # user operation
    # make an instance
    user = User()

    operatorNo = 11110001
    password = "123456"
    mac = "00:50:56:83:17:58"
    operInfo = "内网IP:,外网IP:,MAC:00:50:56:83:17:58,设备名称:WIN10PRO-249"
    print("operatorLogin")
    token = user.operatorLogin(operatorNo, password, mac, operInfo)
    if None == token:
        print("login fail")
        sys.exit()
    print("\n")

    print("getAcctInfo")
    entity = user.getAcctInfo()
    print(entity)
    print("\n")

	'''
    unitAccount = [{"unitId": "111100010001", "accountId": "111100001"},
                   {"unitId": "111100020001", "accountId": "111100002"}]
    marketTypes = [1, 2]
    symbol = ""
    pageNo = 1
    pageSize = 1000
    entityList = []
    print("queryUnitPosition")
    entity = user.queryUnitPosition(unitAccount, marketTypes, symbol, pageNo, pageSize)
    entityList.append(entity)
    while pageNo < entity["pageCount"]:
        pageNo += 1
        entity = user.queryUnitPosition(unitAccount, marketTypes, symbol, pageNo, pageSize)
        entityList.append(entity)
    print(entityList)
    print("\n")

    unitIds = [111100010001, 111100020001, 111100030001]
    accountIds = [111100001, 111100002, 111100003, 111100004, 111100005]
    print("queryUnitFund")
    entity = user.queryUnitFund(unitIds, accountIds)
    print(entity)
    print("\n")

    # order operation
    order = Order(token)
    fileType = 1
    print("fileTemplateDownLoad")
    bRes = order.fileTemplateDownLoad(fileType)
    if False == bRes:
        print("文件单模板下载失败")
    print("\n")

    print("fileOrderUpload")
    bRes = order.fileOrderUpload("template.csv")
    if False == bRes:
        print("文件单上传失败")
    print("\n")

    print("fileOrderSubmit")

    # errorContinue:true出现失败继续下单 false一笔失败全失败 默认true
    errorContinue = {
        "errorContinue": "true"
    }
    order.fileOrderSubmit(errorContinue)
    print("\n")

    algoOrder = {
        "algoOrderList": [{
            "productId": 11110001,
            "unitId": 111100010001,
            "accountId": 111100001,
            "stkAcctCode": "111",
            "basketId": "",
            "marketType": 1,
            "symbol": "000001",
            "side": 1,
            "algoTypeId": 1,
            "orderQty": 10000,
            "effectiveTime": 93000,
            "expireTime": 140000,
            "limitAction": 1,
            "afterAction": 1,
            "algoParam": "price=9.23;down_limit=5"
        },
            {
                "productId": 11110001,
                "unitId": 111100010001,
                "accountId": 111100001,
                "stkAcctCode": "222",
                "basketId": "",
                "marketType": 2,
                "symbol": "600338",
                "side": 2,
                "algoTypeId": 2,
                "orderQty": 10000,
                "effectiveTime": 93000,
                "expireTime": 140000,
                "limitAction": 1,
                "afterAction": 1,
                "algoParam": "price=21.64;up_limit=10"
            }
        ],
        "errorContinue": "false"
    }

    print("algoOrderCreate")
    order.algoOrderCreate(algoOrder)
    print("\n")

    algoOrder = {
        "operationList": [{
            "sysQuoteId": 6880850335743000001,
            "operationType": 1
        },
            {
                "sysQuoteId": 6880850335965000001,
                "operationType": 4
            }
        ]
    }
    print("algoOrderOperation")
    order.algoOrderOperation(algoOrder)
    print("\n")

    modifyList = {
        "modifyList": [{
            "sysQuoteId": 6800838147627000001,
            "effectiveTime": 0,
            "expireTime": 0,
            "algoParam": "",
            "isOrderCancel": 0
        },
            {
                "sysQuoteId": 6800838147627000002,
                "effectiveTime": 93000,
                "expireTime": "143000",
                "algoParam": "price=9.23;down_limit=5",
                "isOrderCancel": 1
            }
        ]
    }

    print("algoOrderModify")
    order.algoOrderModify(modifyList)
    print("\n")

    algoOrderCondition = {
        "productIds": [11110001],
        "unitIds": [111100010001, 111100020001],
        "accountIds": [11110001],
        "selfData": 1,
        "sides": [1, 2],
        "marketTypes": [1, 2],
        "symbol": "",
        "algoTypeIds": [],
        "algoStatus": [],
        "sysQuoteIds": [],
        "basketIds": [],
        "pageNo": 1,
        "pageSize": 100,
        "sortField": "algoStatus",
        "sortMode": "1"
    }
    print("queryAlgoOrderInfo")
    entityList = []
    entity = order.queryAlgoOrderInfo(algoOrderCondition)
    entityList.append(entity)
    while algoOrderCondition["pageNo"] < entity["pageCount"]:
        algoOrderCondition["pageNo"] += 1
        entity = order.queryAlgoOrderInfo(algoOrderCondition)
        entityList.append(entity)
    print("==Response entity:%s" % entityList)
    print("\n")


    orderCondition = {
        "unitIds": [111100010001, 111100020001],
        "selfData": 1,
        "sides": [1, 2],
        "marketTypes": [1, 2],
        "symbol": "",
        "orderStatus": [],
        "sysQuoteIds": [],
        "sysOrderIds": [],
        "brokerOrderId": [],
        "orderProp": [2, 3],
        "pageNo": 1,
        "pageSize": 100,
        "sortField": "orderStatus",
        "sortMode": "1"
    }
    print("queryOrderInfo")
    entityList = []
    entity = order.queryOrderInfo(orderCondition)
    entityList.append(entity)
    while orderCondition["pageNo"] < entity["pageCount"]:
        orderCondition["pageNo"] += 1
        entity = order.queryOrderInfo(orderCondition)
        entityList.append(entity)
    print("==Response entity:%s" % entityList)
    print("\n")

    dealCondition = {
        "productIds": [],
        "unitIds": [111100010001, 111100020001],
        "acountIds": [],
        "selfData": 1,
        "sides": [1, 2],
        "marketTypes": [1, 2],
        "symbol": "",
        "sysOrderIds": [],
        "brokerOrderId": [],
        "sysDealIds": [],
        "dealIds": [],
        "dealProp": [],
        "pageNo": 1,
        "pageSize": 100,
        "sortField": "side",
        "sortMode": "1"
    }
    print("queryDealInfo")
    entityList = []
    entity = order.queryDealInfo(dealCondition)
    entityList.append(entity)
    while dealCondition["pageNo"] < entity["pageCount"]:
        dealCondition["pageNo"] += 1
        entity = order.queryDealInfo(dealCondition)
        entityList.append(entity)
    print("==Response entity:%s" % entityList)
    print("\n")
	'''
