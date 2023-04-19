import requests
import pandas as pd
from sqlalchemy import create_engine
import mysql.connector
from time import sleep
import schedule

db_type = 'mysql'
host = '192.168.70.40'
port = '3305'
database = 'coin'
username = 'root'
password = '7610'

engine = create_engine(f'{db_type}://{username}:{password}@{host}:{port}/{database}')

# 현재가 API
def now_price(name):
    url = f"https://api.upbit.com/v1/ticker?markets={name}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
# 분봉 API
def minute_candle(code,count):
    url = f"https://api.upbit.com/v1/candles/minutes/1?market={code}&count={count}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    return response.json()
# 데이터베이스 연결 엔진 생성


# DB에서 이름 테이블 받아오기
def select_name():
    with mysql.connector.connect(
        host=host,
        user=username,
        password=password,
        database=database,
        port=port,
    ) as conn:
        cursor = conn.cursor()
        query = 'SELECT market FROM coin_name;'
        cursor.execute(query)
        result = cursor.fetchall()
        return [r[0] for r in result]

# 이름테이블 중 코인코드 데이터만 저장.

def load_new_data():
    codes = pd.DataFrame(select_name(),columns=['market'])
    for market in codes['market']:
        df = pd.DataFrame(now_price(market))
        df2 = pd.DataFrame(minute_candle(market,1))
        if not df.empty:
            df.to_sql(name='coin_volume', con=engine, if_exists='append', index=False)
        if not df2.empty:
            df2.to_sql(name='coin_data', con=engine, if_exists='append', index=False)
        sleep(0.1)

    schedule.every(48).seconds.do(load_new_data)

    while True:
        schedule.run_pending()
        sleep(1)

