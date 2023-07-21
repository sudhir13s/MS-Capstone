#!/usr/bin/env python

import time
# import picamera
import datetime
import requests

BASE_URL = "http://localhost:5000"
SEED = "ATWSLAZTZLUWKTKECYTYLWSMKYVTIAHVBUIDHZWEFBJVOASEHXEORPQJIDEEHXDHRSLLXG9HBQAP9XUCC"
CONTROLLER_ADDRESS = "AAB7CFB4A90AE94AC1CFBE4826620A176B316A76C310EB603C8FD11AFDE87AA0"


def start():
    # *********************************************
    # get address
    url = f"{BASE_URL}/address"
    payload = {"seed": SEED}
    resp = requests.put(url=url, json=payload)
    data = resp.json()
    address = data["address"]
    print(data)

    start_time, end_time = time.time(), time.time()
    # while end_time - start_time <= 6:
    # with picamera.PiCamera() as camera:
    #     camera.resolution = (1280, 720)   # 720p
    #
    #     time.sleep(30)
    #     date_time = datetime.datetime.now()
    #     date_time = str(date_time).replace(" ", "")
    #     name = f'/data/image_{date_time}.jpg'
    #     camera.capture(name)

    # *********************************************
    # get channel
    url = f"{BASE_URL}/channel/create"
    payload = {"side_seed": SEED[:len(SEED) // 2]}
    resp = requests.put(url=url, json=payload)
    data = resp.json()
    channel_id = data["channel"]
    print(data)

    # *********************************************
    # subscribe to channel
    url = f"{BASE_URL}/channel/subscribe"
    payload = {"channel_id": channel_id}
    resp = requests.post(url=url, json=payload)
    print(resp.json())

    # *********************************************
    # broadcast channel id
    url = f"{BASE_URL}/channel/subscribe"
    payload = {"channel_id": channel_id}
    resp = requests.post(url=url, json=payload)
    print(resp.json())

    # *********************************************
    # publish to channel
    date_time = datetime.datetime.now()
    date_time = str(date_time).replace(" ", "")
    name = f"/data/image_{date_time}.jpg"
    url = f"{BASE_URL}/channel/publish"
    payload = {
            "channel_id": channel_id,
            "channel_data": {
                "sender": address,
                "recipient": CONTROLLER_ADDRESS,
                "amount": "0",
                "data": [{
                    "image": name,
                    "notification": "pass"
                    }]
                }
            }

    resp = requests.post(url=url, json=payload)
    if str(resp.status_code).startswith('2'):
        print(f'Data published to tangle {resp.json()}')


    # now verify tangle
    url = f"{BASE_URL}/peers/resolve"
    resp = requests.get(url=url)
    if resp:
        data = resp.json()
        print(data["message"])
        print(data["chain"])
    else:
        print(resp)

        # time.sleep(1)
        # end_time = time.time()


if __name__ == '__main__':
    start()
