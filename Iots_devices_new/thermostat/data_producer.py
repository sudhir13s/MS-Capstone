#!/usr/bin/env python
import json
import random
import time
from MAMClient import MAMClient


def create_data():
    humidity = random.random()*100.
    temperature = random.random()*50-30.
    radon_activity = random.random()*200
    data = {'humidity'   : {'value': humidity, 'unit':'%RH'},
            'temperature': {'value': temperature, 'unit':'C'},
            'radon_activity': {'value':radon_activity, 'unit':'Bq'}}
    return data


def create_location():
    latitude = 2*(random.random()-0.5)*90.
    longitude = 2*(random.random()-0.5)*180.
    location = {'latitude' :{'value':latitude , 'unit':'deg'},
                'longitude':{'value':longitude, 'unit':'deg'}}
    return location


def get_timestamp():
    return time.time() # unix timestamp in utc


if __name__ == "__main__":
    host = '172.25.0.2'
    port = 6379

    try:
        print("connecting to MAMClient")
        client = MAMClient(host, port)
        location = create_location()
        sensor_id = 'radon sensor'
        a = 1
        while a:
            data = create_data()
            timestamp = get_timestamp()
            json_object = {'id': sensor_id,
                           'location': location,
                           'timestamp': timestamp,
                           'data': data}
            # stringify the json data:
            print('sending data to mqtt broker...')
            # print(json_object)
            stringified_json_object = json.dumps(json_object, separators=(',',':'))
            channel_id = client.get_channel_id("1234")
            print("channel_id", channel_id)
            client.subscribe_channel(channel_id)
            client.publish_to_channel(channel_id, stringified_json_object)

            client.publish_to_channel(channel_id, "stringified_json_object")
            client.publish_to_channel(channel_id, "hihihi")

            print('client.channels', client.channels)
            print('client.channels_data', client.channels_data)

            data = client.read_from_channel(channel_id)
            print(data)
            # time.sleep(30.)
            a -= 1
    except Exception as e:
        print("Exception", e)
        exit(1)
