# encoding: utf-8
import sys
import pyupbit
import time
import datetime

# print(pyupbit.Upbit)
#
# # 가상화폐 티커 조회
# tickers = pyupbit.get_tickers()
# print(tickers)
#
# # 원화시장에서 주문 가능한 티커 조회
# tickers_krw = pyupbit.get_tickers(fiat="KRW")
# print(tickers_krw)
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
# # 스텔라루멘에 대한 OHLCV 조회
# xlm = pyupbit.get_ohlcv("KRW-XLM")
# print("======== 스텔라루멘 OHLCV =======")
# print(xlm)
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

