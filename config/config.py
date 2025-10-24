from sqlalchemy import create_engine, types

## Test
db_config = {
			 'user': 'shenzhen', 
			 'password': 'dvXGXNc32Q0r7t5db6GzaPGCnYs=',
			 'host': '44.241.205.126',
			 'port': 3306,
			 #'database': 'gbops_qa' #test
			 'database': 'gbops' #prod
			}

qa_db_config = {
			 'user': 'shenzhen', 
			 'password': 'dvXGXNc32Q0r7t5db6GzaPGCnYs=',
			 'host': '44.241.205.126',
			 'port': 3306,
			 'database': 'gbops_qa' #test
			}

fund_position_mapping = {
			        'fund_id': types.INTEGER(),
					    'trade_dt': types.DATE(),
					    's_info_wincode': types.String(length=50),
					    'shares': types.INTEGER(),
					    's_dq_close': types.FLOAT(precision=2),
					    'opdate': types.DATE()
					   }

fund_trades_mapping = {
						'trade_id': types.String(length=64),
						'fund_id': types.INTEGER(),
						'trade_dt': types.DATE(),
						'trade_time': types.DATE(),
						's_info_windcode': types.String(length=32),
						'direction': types.String(length=8),
						'price': types.FLOAT(precision=2),
						'qty': types.INTEGER()
					  }

userinfo = {
			'operatorNo':20380003,
	        'password':'Jt731229', 
			'mac':'',
			'operInfo':''
			}

#从数据库中抓取products.csv的sql语句
query_pp = 'select * from trading.kafang_fund_stra_id_map a inner join trading.kafang_account_map b ON a.productId=b.productId AND a.unitId=b.unitId'

