import requests

# 1분 캔들 조회
from sympy.physics.vector.printing import params

url = "https://api.upbit.com/v1/candles/minutes/1"
querystring = {"market":"KRW-BTC","count":"1"}
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)



# 최근 체결 내역 조회
# import requests
url = "https://api.upbit.com/v1/trades/ticks"
querystring = {"market": "KRW-BTC", "cont":"1"}
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)


# 현재가 정보
url = "https://api.upbit.com/v1/ticker"
querystring = {"market": "KRW-BTC", "cont":"1"}
headers = {"Accept": "application/json"}
response = requests.request("GET", url, headers=headers, params=querystring)
print(response.text)