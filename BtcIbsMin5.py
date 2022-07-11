# 변동성 돌파 전략 비트코인 자동매매 코드 (2강)

import time
import pyupbit
import datetime

def get_target_price(ticker, k):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_ibs_index(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    ibs_index = (df.iloc[0]['close']-df.iloc[0]['low']) / (df.iloc[0]['high'] - df.iloc[0]['low']) 
    return ibs_index

def get_stop_price(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=2)
    stop_price = df.iloc[0]['close'] - (df.iloc[0]['high'] - df.iloc[0]['low']) * 0.5
    return stop_price

def get_start_time(ticker):
    df = pyupbit.get_ohlcv(ticker, interval="minute5", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

  
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-BTC") 
        end_time = start_time + datetime.timedelta(minutes=5)
        if start_time < now < end_time - datetime.timedelta(seconds=10):
            target_price = get_target_price("KRW-BTC", 0.1)
            current_price = get_current_price("KRW-BTC")
            stop_price = get_stop_price("KRW-BTC")
            ibs_index = get_ibs_index("KRW-BTC")
            if (target_price < current_price) and(ibs_index > 0.8):
                krw = get_balance("KRW")
                if krw  > 5000:
                    upbit.buy_market_order("KRW-BTC", krw*0.9995)
                    print(krw)
            if current_price < stop_price:       
                btc = get_balance("BTC")
                if btc > 1000/current_price:
                    upbit.sell_market_order("KRW-BTC", btc*0.9995)   
            print(now, target_price,current_price,ibs_index )
            
                    
        # 9시 300초전일때 전량 매도            
        else:
            current_price = get_current_price("KRW-BTC")
            btc = get_balance("BTC")
            if btc > 1000/current_price:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)    
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
        