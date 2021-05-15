import time
import os
from upbit_api.api import *
import asyncio
from multiprocessing import Pool, Process, Queue

upbit_tickers_queue = Queue()
upbit_candle_list = []


# 매도 후 메일 전송
def dead_cross(symbol):
    print("전량매도")

    # ==========================================
    # Sell
    # ==========================================
    # 구매 단위 선정
    unit_size = get_min_price_unit(pyupbit.get_current_price(symbol))

    # 매도량 계산
    sell_volume = upbit.get_balance(symbol)

    # 현재가보다 살짝 낮게 판매
    sell_price = pyupbit.get_current_price(symbol) - unit_size
    print(upbit.sell_limit_order(ticker=symbol, price=sell_price, volume=sell_volume))

    # ==========================================
    # Send Email
    # ==========================================
    title = f'{symbol} 전량매도'
    content = f' 매도 가격: {sell_price}\n매도 수량: {sell_volume}'
    send_mail(title, content)


# 매수 후 메일 전송
def golden_cross(symbol):
    print("매수")
    # ==========================================
    # Buy
    # ==========================================
    # 시장가로 매수
    buy_price = 5000
    upbit.buy_market_order(ticker=symbol, price=buy_price)

    # ==========================================
    # Send Email
    # ==========================================
    title = f'{symbol} 매수'
    content = upbit.get_order(symbol)
    send_mail(title, content)


# 3번 연속 하락을 감지하거나 현재가보다 떨어질 경우 판매
def check_low_candle(symbol):
    candle = pyupbit.get_ohlcv(ticker=symbol, interval='minutes30', count=4)
    close = candle['close']

    # 3번 연속 하락 시 판매
    if close[0] > close[1] > close[2]:
        send_mail("3연속 하락에 의한 매도", f'{symbol}')
        dead_cross(symbol)

        return False

    # 현재가보다 떨어질 경우 판매
    if pyupbit.get_current_price(symbol) > upbit.get_avg_buy_price(symbol):
        send_mail("현재값보다 떨어져 판매", f'{symbol}')
        dead_cross(symbol)

        return False

    return False


# 10개씩 조회
# async def lookup_symbol():
def lookup_symbol():
    symbol_list = []
    print("async start")

    for i in range(10):
        symbol_list.append(upbit_tickers_queue.get())

    print("SYMBOL_LIST ##########")
    print(symbol_list)
    return symbol_list


async def checking_moving_average(symbol):
    '''
        골든크로스
            - test1 : 음수
            - test2 : 같거나 양수
        데드크로스
            - test1 : 같거나 양수
            - tset2 : 음수
    '''
    print(symbol, end='|')
    before_price = 0
    is_golden_cross = False

    try:
        while True:
            # loop = asyncio.get_event_loop()
            # loop.run_until_complete(lookup_symbol())
            # loop.close()

            # asyncio.run(lookup_symbol())

            candle_30min = pyupbit.get_ohlcv(symbol, interval="minute30")
            close = candle_30min['close']

            bf_ma20 = close.rolling(20).mean().iloc[-2]
            bf_ma60 = close.rolling(60).mean().iloc[-2]
            ma20 = close.rolling(20).mean().iloc[-1]
            ma60 = close.rolling(60).mean().iloc[-1]

            ma_test1 = bf_ma20 - bf_ma60
            ma_test2 = ma20 - ma60

            now_price = pyupbit.get_current_price(symbol)

            # print("======== 현재/이전가 계산 ======")
            # print(f'현재가 : {now_price}')
            # print(f'이전가 : {before_price}\n')
            is_state = now_price - before_price
            # print(f'## 음봉/양봉 : {is_state}')
            #
            # print(symbol)
            # print("======== 20/60일 이동평균선 계산 ======")
            # print(f"20일 이평선 : {round(ma20, 2)}")
            # print(f"60일 이평선 : {round(ma60, 2)}")
            #
            # print(f"======== test result ========")
            # print(f"ma_test1 : {ma_test1}")
            # print(f"ma_test2 : {ma_test2}")

            if is_golden_cross:
                is_golden_cross = check_low_candle(symbol)

            if is_state > 0 and (ma_test1 < 0 and ma_test2 >= 0):
                send_mail(f"golden_cross : {symbol}", "...")
                is_golden_cross = True
                golden_cross(symbol)

            elif ma_test1 >= 0 and ma_test2 < 0:
                send_mail(f"dead_cross : {symbol}", "...")
                dead_cross(symbol)
                is_golden_cross = False

            else:
                pass

            # 루프가 끝나고 현재 가격은 이전 값으로 등록
            before_price = now_price

            # time.sleep(60 * 30)
            await asyncio.sleep(60 * 10)

    except Exception as e:
        send_mail("error", e)


async def check_loop(proc_name):
    """
        # 매수 시기
        양봉 > 20이평선 > 60이평선 더 클 때 (전과 지금 값보다 비교해서 많은 경우 )
        양봉인 경우는 3분 전의 가격과 현재 가격을 비교해서 상승했을 경우

        # 매도 시기
        20이평선이 60이평선보다 가로지르는 상태인데 20이평선이 캔들 3번 하락세면 매도신호

    """

    # 10개 코인 감시
    symbol_list = lookup_symbol()

    moves = [asyncio.Task(checking_moving_average(symbol)) for symbol in symbol_list]
    await asyncio.gather(*moves)


if __name__ == '__main__':
    # ==========================================
    # Send Email
    # ==========================================
    send_mail('start the program', '....')

    # ==========================================
    # Enqueue Upbit Tickers
    # ==========================================
    tickers_list = pyupbit.get_tickers(fiat="KRW")

    for ticker in tickers_list:
        upbit_tickers_queue.put(ticker)

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
    # ==========================================
    # Login
    # ==========================================
    print(upbit)
    print("autotrade start")

    # ==========================================
    # START Trading
    # ==========================================
    print("[+] Start Trading loop")
    print(f"balance: {upbit.get_balance('KRW')}")

    asyncio.run(check_loop('proc main'))

    upbit_tickers_queue.close()
    upbit_tickers_queue.join_thread()

