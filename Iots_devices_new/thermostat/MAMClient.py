import hashlib
import json
import redis

__all__ = ['MAMClient']


class MAMClient:
    def __init__(self, host="localhost", port=6379):
        self.client = redis.Redis(host=host, port=port, db=0)
        self.channels = []
        self.channels_data = {}

    def get_channel_id(self, seed):
        client = json.dumps(seed, sort_keys=True).encode()
        channel = hashlib.sha256(client).hexdigest().upper()
        if channel not in self.channels:
            self.channels.append(channel)
            self.channels_data[channel] = []
        return channel

    def publish_to_channel(self, channel_id, data):
        self.client.publish(channel_id, data)
        self.channels_data[channel_id].append(data)

    def subscribe_channel(self, channel_id):
        sub_obj = self.client.pubsub()
        sub_obj.subscribe(channel_id)

    def read_from_channel(self, channel_id):
        if channel_id in self.channels_data:
            return self.channels_data[channel_id]
