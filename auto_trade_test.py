import time
import pyupbit
import datetime
import pandas as pd
import requests
import webbrowser
import numpy as np

### test
ma20 = 654
ma60 = 660
bf_ma20 = ma20
bf_ma60 = ma60
now_price = 1000
before_price = 1000


def golden_cross(symbol):
    ### test
    global ma20, now_price, bf_ma20
    global ma60, before_price, bf_ma60
    global sell_cnt
    """
        # 매수 시기
        양봉 > 20이평선 > 60이평선 더 클 때 (전과 지금 값보다 비교해서 많은 경우 )
        양봉인 경우는 3분 전의 가격과 현재 가격을 비교해서 상승했을 경우

        # 매도 시기
        20이평선이 60이평선보다 가로지르는 상태인데 20이평선이 캔들 3번 하락세면 매도신호

    """
    global before_price
    cbk = pyupbit.get_ohlcv(symbol, interval="minute3")
    close = cbk['close']

    ### test
    # bf_ma20 = close.rolling(20).mean().iloc[-2]
    # bf_ma60 = close.rolling(60).mean().iloc[-2]
    # ma20 = close.rolling(20).mean().iloc[-1]
    # ma60 = close.rolling(60).mean().iloc[-1]

    ####
    '''
        골든크로스
            - test1 : 음수
            - test2 : 같거나 양수
        데드크로스
            - test1 : 같거나 양수
            - tset2 : 음수
    '''
    ####
    test1 = bf_ma20 - bf_ma60
    test2 = ma20 - ma60

    bf_ma20 = ma20
    bf_ma60 = ma60

    call = '해당없음'

    ### test
    # now_price = pyupbit.get_current_price("KRW-XRP")

    print(f'now_price : {now_price}')
    print(f'before_price : {before_price}')
    is_state = now_price - before_price

    print(symbol)
    print("======== 20/60일 이동평균선 계산 ======")
    print(f"20일 이평선 : {round(ma20, 2)}")
    print(f"60일 이평선 : {round(ma60, 2)}")
    print('')

    print(f'## is_state : {is_state}')
    # 현재 양봉상태이며 골든크로스라면
    print(f'''#########
        test1 : {test1}
        test2 : {test2}    
    ##########''')

    # 양봉일 때는 sell_cnt 초기화
    if is_state > 0:
        sell_cnt = 3

    # if is_state > 0 and (test1 < 0 and test2 > 0):
    if is_state > 0 and (test1 < 0 and test2 >= 0):
        call = '골든크로스'
        # buy_price = buy_thing
        print("매수")
    elif test1 >= 0 and test2 < 0:
        call = '데드크로스'
        # 3번 하락세거나 하락한 현재가가 골든크로스 매수가보다 낮을 때
        if sell_cnt == 0 or (now_price < buy_price):
            call = '~~~~~~~!!!!!!!!!!!! 매도 '
            print("매도")
    else:
        pass

    print('### 골든크로스/데드크로스 ###: ', call)

    # 루프가 끝나고 현재 가격은 이전 값으로 등록
    before_price = now_price

    # time.sleep(60 * 3)
    time.sleep(1)

    ### test
    ma20 += 1
    # ma60 -= 1
    now_price += 1


if __name__ == '__main__':
    f = open("upbit.txt")
    lines = f.readlines()
    access = lines[0].strip()
    secret = lines[1].strip()
    f.close()

    upbit = pyupbit.Upbit(access, secret)

    ### test
    # before_price = 0
    buy_price = 0
    sell_cnt = 3
    # 로그인

    print(upbit)
    print("autotrade start")

    # 자동매매 시작
    while True:
        golden_cross('KRW-DOGE')
        print(f"balance: {upbit.get_balance('KRW')}")

        print("[+] Start Trading loop")
        try:

            time.sleep(1)

        except Exception as e:
            print(e)
            time.sleep(1)
