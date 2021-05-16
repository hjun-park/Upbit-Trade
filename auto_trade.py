import datetime
import os
import time
import signal
from upbit_api.api import *
import asyncio
import traceback
from multiprocessing import Queue, Process, Pool, current_process

file_path = "./upbit_api/coin_info.json"
coin_json = 0


def handler(signum, frame):
    print('TERMINATE')
    with open(file_path, 'w') as outfile:
        json.dump(coin_json, outfile, indent=4)


# 매도 후 메일 전송
async def dead_cross(symbol):
    print("전량매도")

    # ==========================================
    # Sell ( 전량매도 : 매도가 = 현재가 - 가격단위 )
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
    await send_mail(title, content)


# 매수 후 메일 전송
async def golden_cross(symbol, info):
    print("매수")
    # ==========================================
    # Buy
    # ==========================================
    # 시장가로 매수
    buy_price = 6000
    upbit.buy_market_order(ticker=symbol, price=buy_price)

    # ==========================================
    # Send Email
    # ==========================================
    title = f'{symbol} 매수, 가격 {buy_price}'
    # content = f'매수 : {symbol}, 가격: {buy_price}'
    await send_mail(title, info)


# 3번 연속 하락을 감지하거나 현재가보다 떨어질 경우 판매
async def check_low_candle(symbol, before_price):
    candle = pyupbit.get_ohlcv(ticker=symbol, interval='minutes10', count=4)
    close = candle['close']

    print(f"\t\t=============================")
    print(f"\t\t======== Candle Info ========")
    print(f"\t\t=============================")
    print(f"\t\t1-1) close[0]: {close[0]}")
    print(f"\t\t1-2) close[1]: {close[1]}")
    print(f"\t\t1-3) close[2]: {close[2]}\n")
    print(f"\t\t2-1) 이전가(-4%): {before_price * 0.96}")
    print(f"\t\t3-1) 현재 잔고 평균가({symbol}): {upbit.get_avg_buy_price(symbol)}")

    content = f'''
    ===================
    === Candle Info ===
    ===================
    1-1) close[0]: {close[0]}
    1-2) close[1]: {close[1]}
    1-3) close[2]: {close[2]}
    2-1) 이전가(-4%): {before_price * 0.96}
    3-1) 현재 잔고 평균가({symbol}): {upbit.get_avg_buy_price(symbol)}
    '''

    # 3번 연속 하락 시 판매
    if int(close[0]) > int(close[1]) > int(close[2]):
        print("3연속 하락에 의한 매도")
        await send_mail(f"{symbol}3연속 하락에 의한 매도", f"..{content}...")
        await dead_cross(symbol)

        return 0

    # 이전값에서 4%보다 같거나 더 빠진 경우
    if pyupbit.get_current_price(symbol) <= (before_price * 0.96):
        print("4% 하락에 의한 판매")
        await send_mail(f"{symbol}4% 하락에 의한 판매", f"..{content}...")
        await dead_cross(symbol)

        return 0

    # # 매수가가 현재가보다 더 큰 경우
    # if pyupbit.get_current_price(symbol) < upbit.get_avg_buy_price(symbol):
    #     print("현재값보다 떨어져 판매")
    #     await send_mail(f"{symbol} 현재값보다 떨어져 판매", f"..{content} :{upbit.get_avg_buy_price(symbol)}...")
    #     await dead_cross(symbol)
    # 
    #     return 0

    return 0


async def checking_moving_average(symbol):
    """
        골든크로스
            - test1 : 음수
            - test2 : 같거나 양수
        데드크로스
            - test1 : 같거나 양수
            - test2 : 음수
    """
    global coin_json
    before_price = pyupbit.get_current_price(symbol)
    now_price = 0
    coin_json = load_golden_cross_info(file_path)

    print(coin_json)
    try:
        while True:
            index = 0
            # ==========================================
            # CHECK ACCESS KEY
            # ==========================================
            check_key_expire(upbit)

            # ==========================================
            # START LOOP
            # ==========================================
            print(symbol, end='|')

            # 가끔 값을 받아오지 못하는 경우는 다시
            try:
                candle_min = pyupbit.get_ohlcv(symbol, interval="minute10")
                close = candle_min['close']
            except TypeError:
                await send_mail('some errer in load candle', '...')
                print('!!!!!!!!!!!!!!!!! TYPE ERROR !!!!!!!!!!!!!!!!!')
                continue

            bf_ma20 = close.rolling(20).mean().iloc[-2]
            bf_ma60 = close.rolling(60).mean().iloc[-2]
            ma20 = close.rolling(20).mean().iloc[-1]
            ma60 = close.rolling(60).mean().iloc[-1]

            ma_test1 = bf_ma20 - bf_ma60
            ma_test2 = ma20 - ma60

            now_price = pyupbit.get_current_price(symbol)

            is_state = int(now_price) - int(before_price)

            info = f'''
                ###########################################
                ============ {index}: {symbol} =============
                ============ {datetime.datetime.now()} ============
                ============ 현재/이전가 계산 =============
                1) 현재가 : {now_price}
                2) 이전가 : {before_price}
                3) 음봉/양봉 : {is_state}
                
                ======= 이평선 계산 =======
                1) 20일 이평선 : {round(ma20, 2)}
                2) 60일 이평선 : {round(ma60, 2)}
                
                ======= 크로스 테스트 =======
                1) ma_test1 : {round(ma_test1, 2)}
                2) ma_test2 : {round(ma_test2, 2)}
                
                골든크로스
                    - test1 : 음수
                    - test2 : 같거나 양수    
                데드크로스
                    - test1 : 같거나 양수
                    - test2 : 음수
                ###########################################
                
                
                
            '''
            index += 1

            # ==========================================
            # 골든크로스 상태에서의 체크 루프
            # ==========================================
            if coin_json[symbol]:
                print(f' ##### {symbol} in golden_cross')
                coin_json[symbol] = await check_low_candle(symbol, before_price)

            if is_state > 0 and (ma_test1 < 0 and ma_test2 >= 0):
                await send_mail(f"KEEP CHECKING : {symbol}", "...")
                coin_json[symbol] = 1
                await golden_cross(symbol, info)

            elif ma_test1 >= 0 and ma_test2 < 0:
                await send_mail(f"dead_cross : {symbol}", "...")
                await dead_cross(symbol)
                coin_json[symbol] = 0

            else:
                pass

            # 루프가 끝나고 현재 가격은 이전 값으로 등록
            before_price = now_price

            # time.sleep(60 * 30)
            print(f'########## {symbol} SCAN DONE ############\n\n\n')
            await asyncio.sleep(60 * 10)

    except Exception as e:
        print(traceback.format_exc())
        await send_mail("error", str(traceback.format_exc()))
        await asyncio.sleep(2)


async def check_loop():
    """
        # 매수 시기
        양봉 > 20이평선 > 60이평선 더 클 때 (전과 지금 값보다 비교해서 많은 경우 )
        양봉인 경우는 3분 전의 가격과 현재 가격을 비교해서 상승했을 경우

        # 매도 시기
        20이평선이 60이평선보다 가로지르는 상태인데 20이평선이 캔들 3번 하락세면 매도신호

    """
    # ==========================================
    # Send Email
    # ==========================================
    await send_mail('start the program', '....')
    print('###### START ######')

    # ==========================================
    # 코인 20개 이평선 감시
    # ==========================================
    symbol_list = get_coin_list(file_path)
    moves = [asyncio.Task(checking_moving_average(symbol)) for symbol in symbol_list]
    await asyncio.gather(*moves)


# def func():
#     while True:
#         name = current_process().name
#         print("starting of process named: ", name)
#         time.sleep(2)
#         print("exiting process")

def sell_proc():
    try:
        while True:
            #  1. 주기적으로 잔고확인하여 잔고가 -5% 수익이면 전량 매도
            time.sleep(60 * 10)

            balance = upbit.get_balances()  # 매수 총 내역
            size = len(balance)
            for i in range(1, size):
                buy_avg_price = int(balance[i]['avg_buy_price'])
                minus_5p = round(buy_avg_price * 0.95)

                # -5% 이하라면 판매
                if buy_avg_price < minus_5p:
                    symbol = f"KRW-{balance[i]['currency']}"
                    dead_cross(symbol)

    except Exception as e:
        print(traceback.format_exc())
        send_mail("error(sell_proc)", str(traceback.format_exc()))
        time.sleep(2)


def buy_proc():
    #  2. +2% 수익이 나면 추가 매수 ( 이건 신중해서 해볼 것 )
    time.sleep(60 * 3)


if __name__ == '__main__':
    signal.signal(signal.SIGTERM, handler)
    signal.signal(signal.SIGINT, handler)
    # signal.signal(signal.SIGKILL, handler)
    # ==========================================
    # GET Upbit Account Info
    # ==========================================
    os.environ['UPBIT_OPEN_API_ACCESS_KEY'] = '46PB8FwZLoe2IjKxU0OnJToTtOtjOMxIx5l3dh2h'
    os.environ['UPBIT_OPEN_API_SECRET_KEY'] = 'B1oYGuJi7Y4TowhFnTsnv5LSKpuMSyNxKEej8ojk'
    os.environ['UPBIT_OPEN_API_SERVER_URL'] = "https://api.upbit.com"

    access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
    secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
    server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

    # ==========================================
    # Login
    # ==========================================
    upbit = pyupbit.Upbit(access_key, secret_key)
    print(upbit)

    # ==========================================
    # START Trading
    # ==========================================
    print("[+] Start Trading loop")
    print(f"balance: {upbit.get_balance('KRW')}")

    # ==========================================
    # make Thread
    # ==========================================
    sell_proc = Process(target=sell_proc, name="sell_proc")
    buy_proc = Process(target=buy_proc, name="buy_proc")
    main_proc = Process(target=asyncio.run(check_loop()), name="main_proc")

    proc_list = [sell_proc, buy_proc, main_proc]

    for proc in proc_list:
        proc.daemon = True
    for proc in proc_list:
        proc.start()
    for proc in proc_list:
        proc.join()
