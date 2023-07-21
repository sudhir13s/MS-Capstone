import hashlib
import json
import paho.mqtt.client as paho

import redis


class MAMClient:
    def __init__(self, host, port=6379):
        # self.host = host
        # self.port = port
        # self.client = paho.Client()
        # self.client.on_connect = self.on_connect
        # self.client.on_subscribe = self.on_subscribe
        # self.client.on_publish = self.on_publish
        # self.client.on_message = self.on_message
        # self.client.connect(broker, port)
        self.client = redis.Redis(host=host, port=port, db=0)
        self.channels = []
        self.channels_data = {}
        # self.client.loop_forever()

    # def __exit__(self, exc_type, exc_val, exc_tb):
    #     self.client.loop_stop()

    # def on_connect(self, client, userdata, flags, rc):
    #     print("Connected with result code " + str(rc))

    # def on_publish(self, client, userdata, mid):
    #     print("on_publish", userdata, mid)
        # for channel in self.channels:
        #     if channel in mid:
        #         self.channels_data[channel].append(mid)

    # def on_subscribe(self, client, userdata, mid):
    #     print("on_subscribe", userdata, mid)
    #
    # def on_message(self, client, userdata, message):
    #     print("on_message", userdata, message)
    #     self.channels_data[message.topic].append(message.payload)

    def get_channel_id(self, seed):
        client = json.dumps(seed, sort_keys=True).encode()
        channel = hashlib.sha256(client).hexdigest().upper()
        if channel not in self.channels:
            self.channels.append(channel)
            self.channels_data[channel] = []
        return channel

    def publish_to_channel(self, channel_id, data):
        # if not channel_id or not data:
        #     return False
        # self.client.publish(channel_id, data, retain=True)
        # return True
        self.client.publish(channel_id, data)
        self.channels_data[channel_id].append(data)

    def subscribe_channel(self, channel_id):
        sub_obj = self.client.pubsub()
        sub_obj.subscribe(channel_id)

        # return self.client.subscribe(channel_id)

    def read_from_channel(self, channel_id):
        if channel_id in self.channels_data:
            return self.channels_data[channel_id]
