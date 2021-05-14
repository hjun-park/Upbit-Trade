import time
import pyupbit
import datetime
import pandas as pd
import requests
import webbrowser
import numpy as np



def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    k = 1 - abs(df.iloc[0]['open'] - df.iloc[0]['close']) / (df.iloc[0]['high'] - df.iloc[0]['low'])
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    print(target_price)
    return target_price


def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute1", count=1)
    start_time = df.index[0]
    return start_time


def get_ma20(ticker):
    """20일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=20)
    ma20 = df['close'].rolling(window=20, min_periods=1).mean().iloc[-1]
    print(ma20)
    return ma20


def get_balance(ticker):
    """잔고 조회"""
    balances = pyupbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0


def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(tickers=ticker)[0]["orderbook_units"][0]["ask_price"]


def goldencross(symbol):
    #### 현재 방식
    global before_price
    cbk = pyupbit.get_ohlcv(symbol, interval="minute3")
    close = cbk['close']

    bf_ma20 = close.rolling(20).mean().iloc[-2]
    bf_ma60 = close.rolling(60).mean().iloc[-2]
    ma20 = close.rolling(20).mean().iloc[-1]
    ma60 = close.rolling(60).mean().iloc[-1]

    ####
    test1 = bf_ma20 - bf_ma60
    test2 = ma20 - ma60

    call = '해당없음'

    now_price = pyupbit.get_current_price("KRW-XRP")
    is_state = now_price - before_price
    # 양봉이고 20이평선과 60이평선보다 더 클 때 (전과 지금 값보다 비교해서 많은 경우 )
    # # 양봉인 경우는 3분 전의 가격과 현재 가격을 비교해서 상승했을 경우
    # #
    # 그리고 20이평선이 60 이평선을 가로지를 때 매수신호

    # 20이평선이 60이평선보다 가로지르는 상태인데 20이평선이 캔들 3번 하락세면 매도신호
    # 60 이평선이 20이평선을 가로지르면 매도신호

    # 이전 값은 20이 우세하다가 지금은 60이 가로지르는 경우
    if :


    # 이전 값은 60이 우세하다가 지금은 20이 가로지르는 경우
    if test1 < 0 and test2 > 0:
        call = '골든크로스'

    print(symbol)
    print("======== 20/60일 이동평균선 계산 ======")
    print(f"20일 이평선 : {round(ma20, 2)}")
    print(f"60일 이평선 : {round(ma60, 2)}")
    print('골든크로스/데드크로스: ', call)
    print('')

    # 현재 양봉상태이며 골든크로스라면
    if is_state > 0 and (test1 > 0 and test2 < 0):
        call = '골든크로스'
        print("매수")
    elif test1 < 0 and test2 > 0:
        call = '데드크로스'
        # 3번 하락세거나 하락한 현재가가 골든크로스 매수가보다 낮을 때
        if sell_cnt == 0 or (now_price < buy_price):
            
    else:
        pass

    # 루프가 끝나고 현재 가격은 이전 값으로 등록
    before_price = pyupbit.get_current_price("KRW-XRP")

    time.sleep(60 * 3)


if __name__ == '__main__':
    before_price = 0
    buy_price = 0
    sell_cnt = 3
    # 로그인
    f = open("upbit.txt")
    lines = f.readlines()
    access = lines[0].strip()
    secret = lines[1].strip()
    f.close()

    upbit = pyupbit.Upbit(access, secret)
    print(upbit)
    print("autotrade start")

    # 자동매매 시작
    while True:
        goldencross('KRW-DOGE')
        print(f"balance: {get_balance('KRW')}")

        print("[+] Start Trading loop")
        try:

            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)
