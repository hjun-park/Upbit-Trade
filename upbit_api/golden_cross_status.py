import pickle
import json

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

file_path = "./coin_info.json"
#
coin_info = {}

for i in coin_list:
    coin_info[i] = 0

# coin_info['coin'] = []
#
# for i in coin_list:
#     coin_info['coin'].append({
#         "name": i,
#         "is_golden": 0
#     })
#
with open(file_path, 'w') as outfile:
    json.dump(coin_info, outfile, indent=4)

# 특정 정보 읽어오기
# with open(file_path, "r") as json_file:
#     json_data = json.load(json_file)

# print(json_data['KRW-DOGE'])
#
# # 변경 후 다시저장
# json_data['KRW-DOGE'] = 1
#
# with open(file_path, 'w') as outfile:
#     json.dump(json_data, outfile, indent=4)

# print (json_data['KRW-DOGE'])

# for name, value in json_data.items():
#     print(name, value)

