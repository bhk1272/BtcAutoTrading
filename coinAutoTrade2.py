# 변동성 돌파 전략 비트코인 자동매매 코드 (2강)

import time
import pyupbit
import datetime

access = ""
secret = ""

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 (2일치) 조회"""
    # 새로운 전략 기술은 여기에
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        now = datetime.datetime.now()
        # 오전 9:00 시작
        start_time = get_start_time("KRW-BTC") 
        end_time = start_time + datetime.timedelta(days=1)

        # 9:00 < 현재 < #8:59:30 
        if start_time < now < end_time - datetime.timedelta(seconds=30):
            target_price_BTC = get_target_price("KRW-BTC", 0.8)
            current_price_BTC = get_current_price("KRW-BTC")
            if target_price_BTC < current_price_BTC:
                #현재 잔금조회
                krw_BTC = get_balance("KRW") * 0.4
                #현재 잔금이 5000원 이상이면 매수, 이때 수수료 0.05%고려
                if krw_BTC  > 5000:
                    upbit.buy_market_order("KRW-BTC", krw_BTC*0.9995)
                    
            target_price_ETH = get_target_price("KRW-ETH", 0.7)
            current_price_ETH = get_current_price("KRW-ETH")
            if target_price_ETH < current_price_ETH:
                #현재 잔금조회
                krw_ETH = get_balance("KRW") *0.3
                #현재 잔금이 5000원 이상이면 매수, 이때 수수료 0.05%고려
                if krw_ETH > 5000:
                    upbit.buy_market_order("KRW-ETH", krw_ETH*0.9995)        
                    
            target_price_XRP = get_target_price("KRW-XRP", 0.5)
            current_price_XRP = get_current_price("KRW-XRP")
            if target_price_XRP < current_price_XRP:
                #현재 잔금조회
                krw_XRP = get_balance("XRP") *0.3
                #현재 잔금이 5000원 이상이면 매수, 이때 수수료 0.05%고려
                if krw_XRP > 5000:
                    upbit.buy_market_order("KRW-XRP", krw_XRP*0.9995)                          
                             
                    
        # 9시 30초전일때 전량 매도            
        else:
            # 현재 btc잔고 조회
            btc = get_balance("BTC")
            # 0.0002이 대략 현재기준 5000원정도됨
            # 9시 10초전에 btc 잔고가 5000원 정도이상이면 전량 매도, 수수료 0.05% 고려
            if btc > 0.0002:
                upbit.sell_market_order("KRW-BTC", btc*0.9995)
                
          # 현재 ETH잔고 조회
            eth = get_balance("ETH")
            # 0.0036이 대략 현재기준 5000원정도됨
            # 9시 10초전에 eth 잔고가 5000원 정도이상이면 전량 매도, 수수료 0.05% 고려
            if eth > 0.0036:
                upbit.sell_market_order("KRW-ETH", eth*0.9995)

          # 현재 XRP잔고 조회
            xrp = get_balance("XRP")
          # 12이 대략 현재기준 5000원정도됨
          # 9시 10초전에 xrp 잔고가 5000원 정도이상이면 전량 매도, 수수료 0.05% 고려
            if xrp > 12:
                upbit.sell_market_order("KRW-XRP", xrp*0.9995)               
                
             
                
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)