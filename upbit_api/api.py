import sys
import pyupbit
import asyncio
import json
import smtplib
from email.mime.text import MIMEText

# print("\n# =======================================")
# print(datetime.datetime.now())
# print("\n# =======================================")
# print("============ 현재/이전가 계산 =============")
# print(f'\t1) 현재가 : {now_price}')
# print(f'\t2) 이전가 : {before_price}\n')
# is_state = int(now_price) - int(before_price)
# print(f'\t3) 음봉/양봉 : {is_state}')
#
# print("========= 20/60일 이동평균선 계산 =========")
# print(f"\t1) 20일 이평선 : {round(ma20, 2)}")
# print(f"\t2) 60일 이평선 : {round(ma60, 2)}")
#
# print(f"============= 크로스 테스트 =============")
# print(f"\t1) ma_test1 : {round(ma_test1, 2)}")
# print(f"\t2) ma_test2 : {round(ma_test2, 2)}")

coin_list = [
    'KRW-DOGE',
    'KRW-ETC',
    'KRW-XRP',
    'KRW-ETH',
    'KRW-BTC',
    'KRW-ADA',
    'KRW-EOS',
    'KRW-DOT',
    'KRW-BCH',
    'KRW-QTUM',
    'KRW-SSX',
    'KRW-BTT',
    'KRW-CHZ',
    'KRW-XLM',
    'KRW-LTC',
    'KRW-BTG',
    'KRW-NEO',
    'KRW-SNT',
    'KRW-VET',
    'KRW-HUNT'
]


def load_golden_cross_info(file_path):
    with open(file_path, "r") as json_file:
        coin_json = json.load(json_file)

    return coin_json

    # for name, value in json_data.items():
    #     print(name, value)


def check_key_expire(upbit):
    INVALID_AKEY = "invalid_access_key"
    is_valid_key = upbit.get_balances()

    try:
        if is_valid_key['error']['name'] == INVALID_AKEY:
            print('send_mail')
            asyncio.run(send_mail("INVALID_AKEY", "Please Check API KEY"))
    except TypeError:
        pass

    print('done')


def get_coin_list(file_path):
    '''

    :param file_path: file_path
    :return: list
    '''

    coin_info = []

    with open(file_path, "r") as json_file:
        coin_json = json.load(json_file)

    for name in coin_json.keys():
        coin_info.append(name)

    return coin_info


# 최소 거래 금액 단위 반환
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


# 메일 전송 서비스
async def send_mail(title, content):
    '''
    :param title: 전송 제목
    :param content: 전송 내용
    :return: 성공 시 0 반환
    '''
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.ehlo()  # say Hello
    smtp.starttls()  # TLS 사용시 필요
    smtp.login('phj0860@gmail.com', 'shnjmugpuizaudjb')

    msg = MIMEText(content)
    msg['Subject'] = title
    msg['To'] = 'tkdldjs35@naver.com'
    smtp.sendmail('phj0860@gmail.com', 'tkdldjs35@naver.com', msg.as_string())

    smtp.quit()

    return 0


# 주기적으로 팔렸는지 체크하는 스크립트
def check_is_sold():
    return None
