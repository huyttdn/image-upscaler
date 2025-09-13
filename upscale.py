import requests
import json

serverurl = "https://image-upscaling.net"
client_id = "54e41437548a1aae779e6b48e8d3ea59"
cookies = { "client_id": client_id }


use_face_enhance = False
scale = 4
path = "test_image.png"

url = "/".join([serverurl, "upscaling_upload"])
data = {"scale": scale, "model": "plus"}
if use_face_enhance:
    data["fx"] = ""

files = {"image": open(path, "rb")}
response = requests.post(url, data=data, files=files, cookies=cookies)
print(response.text)

while True:
    url = "/".join([serverurl, "upscaling_get_status"])
    response = requests.get(url, cookies=cookies).json()

    for url in response["processed"]:
        filename = url.split("/")[-1]
        filename = filename.replace(":", "-") 

        params = {"delete_after_download": ""}
        content = requests.get(url, cookies=cookies, params=params).content
        with open(filename, "wb") as f:
            f.write(content)

    if not response["pending"] and not response["processing"] and not response["processed"]:
        break
    else:
        import time
        time.sleep(1)