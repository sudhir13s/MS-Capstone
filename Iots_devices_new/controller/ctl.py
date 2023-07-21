import datetime
import time

import requests
import pprint


BASE_URL = "http://localhost:5000"
SEED = "TZOVVZHPGLQZ9GDAFZBNBGULGHGNCWRIEAC9TKXTGNDROCAYZD9TFOPUUHYSUQJYVRZDZF9EUOSHTSSXZ"
CAMERA_ADDRESS = "25979705ED5E257030C6B4623D217C86E17E7C319F40E2ABE0A07EDBD8BB3D8E"


def start():

    url = f"{BASE_URL}/address"
    payload = {"seed": SEED}
    resp = requests.put(url=url, json=payload)

    data = resp.json()
    address = data["address"]
    print(data)
    print(address)


    start_time, end_time = time.time(), time.time()
    # while end_time - start_time <= 6:
    date_time = datetime.datetime.now()
    url = f"{BASE_URL}/tangle"
    resp = requests.get(url=url)
    data = resp.json()
    print(pprint.pprint(data["tangle"]))


if __name__ == '__main__':
    start()
