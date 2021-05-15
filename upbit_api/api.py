import sys
import pyupbit
import smtplib
from email.mime.text import MIMEText


def get_coin_list():
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

    return coin_list

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