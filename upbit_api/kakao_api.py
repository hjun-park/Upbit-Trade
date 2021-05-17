import os
import json
import requests

def sendToMeMessage(text):
    header = {"Authorization": 'Bearer ' + KAKAO_TOKEN}

    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send" #나에게 보내기 주소

    post = {
        "object_type": "text",
        "text": text,
        "link": {
            "web_url": "https://developers.kakao.com",
            "mobile_web_url": "https://developers.kakao.com"
        },
        "button_title": "바로 확인"
    }
    data = {"template_object": json.dumps(post)}
    return requests.post(url, headers=header, data=data)

text = "Hello, This is KaKao Message Test!!("+os.path.basename(__file__).replace(".py", ")")

KAKAO_TOKEN = "rsGYY_dN9DWuRMngjqx_lf6aN64RJi9A-BWyMQopyWAAAAF5dEUKpg"

print(sendToMeMessage(text).text)

