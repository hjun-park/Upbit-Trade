# -*- coding:utf-8 -*-
import sys
import pyupbit
import time
import datetime
import smtplib
import auto_trade
import asyncio
import os
from upbit_api.api import *
from email.mime.text import MIMEText


# print(pyupbit.Upbit)
#
# # 가상화폐 티커 조회
# tickers = pyupbit.get_tickers()
# print(tickers)
#
# 원화시장에서 주문 가능한 티커 조회
# tickers_krw = pyupbit.get_tickers(fiat="KRW")
# print(len(tickers_krw))
#
#
# # 리플 시세 조회
# price_btc = pyupbit.get_current_price("KRW-DOGE")
# print("======== 리플 시세 =======")
# print(price_btc)
#
# # 비트코인과 이더리움 시세 한 번에 조회
# price_btc_eth = pyupbit.get_current_price(["KRW-BTC", "KRW-ETH"])
# print("======== 비트코인 & 이더리움 시세 =======")
# print(price_btc_eth)
#
#
# 스텔라루멘에 대한 OHLCV 조회 (종가를 기준으로 3개)
# xlm = pyupbit.get_ohlcv(ticker="KRW-DOGE", interval='minutes30', count=3)
# close = xlm['close']
# print("======== 도지코인 OHLCV =======")
# # print(close)
#
# if close[0] > close[1] > close[2]:
#     print('hell')

# print(close[0])
# print(close[1])
# print(close[2])
#
# # 이동평균 계산
# close = xlm['close']
#
# print("======== 스텔라루멘 종가 =======")
# print(close)
#
# # 5일 이동평균선 계산
# window = close.rolling(5)
# ma5 = window.mean()
# print("======== 5일 이동평균선 계산 =======")
# print(ma5)
# print(pyupbit.get_orderbook('KRW-DOGE'))


def get_min_price_unit(price):
    if price >= 2000000:
        unit_size = 1000
    elif price >= 1000000:
        unit_size = 500
    elif price >= 500000:
        unit_size = 100
    elif price >= 100000:
        unit_size = 50
    elif price >= 10000:
        unit_size = 10
    elif price >= 1000:
        unit_size = 5
    elif price >= 100:
        unit_size = 1
    elif price >= 10:
        unit_size = 0.1
    else:
        unit_size = 0.01
    return unit_size


if __name__ == '__main__':
    # ==========================================
    # GET Upbit Account Info
    # ==========================================
    os.environ['UPBIT_OPEN_API_ACCESS_KEY'] = '46PB8FwZLoe2IjKxU0OnJToTtOtjOMxIx5l3dh2h'
    os.environ['UPBIT_OPEN_API_SECRET_KEY'] = 'B1oYGuJi7Y4TowhFnTsnv5LSKpuMSyNxKEej8ojk'
    os.environ['UPBIT_OPEN_API_SERVER_URL'] = "https://api.upbit.com"

    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

    upbit = pyupbit.Upbit(access_key, secret_key)
    symbol = 'KRW-XLM'

    # print(upbit.get_balances())
    check_key_expire(upbit)
    # # ==========================================
    # # Buy
    # # ==========================================
    # 시장가로 매수
    # print(upbit.buy_market_order(ticker=symbol, price=6000))

    # # ==========================================
    # # Sell
    # # ==========================================
    # # 구매 단위 선정
    # unit_size = get_min_price_unit(pyupbit.get_current_price(symbol))
    #
    # # 매도량 계산
    # sell_volume = upbit.get_balance(symbol)
    #
    # # 현재가보다 살짝 낮게 판매
    # sell_price = pyupbit.get_current_price(symbol) - unit_size
    # print(upbit.sell_limit_order(ticker=symbol, price=sell_price, volume=sell_volume))

    # ==========================================
    # 잔고 확인
    # ==========================================
    # print(upbit.get_balance(symbol))    # 매수 개수
    # print(upbit.get_avg_buy_price(symbol))  # 매수 평균가
    # print(upbit.get_amount(symbol)) # 매수 KRW
    # print(upbit.get_chance(symbol))
    balance = upbit.get_balances()  # 매수 총 내역
    size = len(balance)
    print(balance)


    # # 매수평균가 계산
    # for i in range(1, size):
    #     print(balance[i]['avg_buy_price'])
    #
    # symbol = f"KRW-{balance[1]['currency']}"
    # print(f'symbol: {symbol}')
    #
    # print(f'''
    #     test1
    #     test2
    # ''')

    # a = upbit.get_avg_buy_price('KRW-BTC')
    # print (a)

    # candle = pyupbit.get_ohlcv(ticker=symbol, interval='minutes3', count=4)
    # close = candle['close']
    # print(type(close[0]))
    # print(int(close[0]))