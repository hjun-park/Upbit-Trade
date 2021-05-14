import os
import jwt
import uuid
import hashlib
from urllib.parse import urlencode
import pyupbit
import requests
import json


# 현재 자산 조회
os.environ['UPBIT_OPEN_API_ACCESS_KEY'] = '46PB8FwZLoe2IjKxU0OnJToTtOtjOMxIx5l3dh2h'
os.environ['UPBIT_OPEN_API_SECRET_KEY'] = 'B1oYGuJi7Y4TowhFnTsnv5LSKpuMSyNxKEej8ojk'
os.environ['UPBIT_OPEN_API_SERVER_URL'] = "https://api.upbit.com"

access_key = os.environ['UPBIT_OPEN_API_ACCESS_KEY']
secret_key = os.environ['UPBIT_OPEN_API_SECRET_KEY']
server_url = os.environ['UPBIT_OPEN_API_SERVER_URL']

upbit = pyupbit.Upbit(access_key, secret_key)

payload = {
    'access_key': access_key,
    'nonce': str(uuid.uuid4()),
}

jwt_token = jwt.encode(payload, secret_key)
authorize_token = 'Bearer {}'.format(jwt_token)
headers = {"Authorization": authorize_token}

res = requests.get(server_url + "/v1/accounts", headers=headers)


'''
  - currency : 화폐 단위
  - balance : 주문가능 금액
  - locked : 주문 중 묶여있는 금액, 수량
  - avg_buy_price : 매수 평균가
  - avg_buy_price_modified : 매수 평균가 수정여부
'''
json_obj = json.loads(res.text)
asset = json_obj[0]

# print(upbit.buy_limit_order(ticker="KRW-DOGE", price=580, volume=1))
print(upbit.get_order(ticker_or_uuid='KRW-DOGE', state='done'))

