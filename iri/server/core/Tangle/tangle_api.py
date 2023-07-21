import hashlib
import json
from textwrap import dedent
from time import time
from uuid import uuid4
from tangle import Tangle, TangleClient, MAMClient
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request

# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
tangle = Tangle()
tangle_client = TangleClient()
mam_client = MAMClient(tangle)


@app.route('/address', methods=['PUT'])
def get_address():
    values = request.json
    if not values or not values.get('seed'):
        response = {'Error': 'Missing seed', }
        print(response)
        return jsonify(response), 400

    seed = values.get('seed')
    address = tangle_client.generate_address(seed)
    response = {
        'address': address,
    }
    print(response)
    return jsonify(response), 201


@app.route('/channel', methods=['POST'])
def get_channel():
    values = request.json
    # Check that the required fields are in the POST'ed data
    required = ['channel_id']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Publish to channel and create a new Transaction
    values = json.loads(values)
    channel = values["channel_id"]
    channel_id = mam_client.get_channel_id(channel)
    response = {'channel': channel_id}
    return jsonify(response), 200


@app.route('/channel/create', methods=['PUT'])
def create_channel():
    values = request.json
    if not values or not values.get('side_seed'):
        response = {'Error': 'Missing side seed', }
        print(response)
        return jsonify(response), 400

    side_seed = values.get('side_seed')
    channel = mam_client.get_channel_id(side_seed)
    response = {
        'channel': channel,
    }
    print(response)
    return jsonify(response), 201


@app.route('/channel/publish', methods=['POST'])
def channel_publish():
    values = request.json
    # Check that the required fields are in the POST'ed data
    required = ['channel_id', 'channel_data', 'sender', 'recipient', 'amount', 'data']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Publish to channel and create a new Transaction
    values = json.loads(values)
    channel = values["channel_id"]
    data = values["channel_data"]
    node = mam_client.publish_to_channel(channel, data)
    response = node #{'Success': node}
    # tell peers to update tangle
    for peer in tangle.peers:
        requests.get("http://" + str(peer) + "/peers/resolve")
    return jsonify(response), 201


@app.route('/channel/subscribe', methods=['POST'])
def channel_subscribe():
    values = request.json
    # Check that the required fields are in the POST'ed data
    required = ['channel_id']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Publish to channel and create a new Transaction
    values = json.loads(values)
    channel = values["channel_id"]
    flag = mam_client.subscribe_channel(channel)
    if flag:
        response = {'Success': 'subscribed'}
    else:
        response = {'Error': 'No such channel'}
    return jsonify(response), 200


@app.route('/channel/data', methods=['POST'])
def channel_read_data():
    values = request.json
    # Check that the required fields are in the POST'ed data
    required = ['channel_id']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Publish to channel and create a new Transaction
    values = json.loads(values)
    channel = values["channel_id"]
    data = mam_client.read_from_channel(channel)
    response = {'Success': data}
    return jsonify(response), 200


@app.route('/channel/broadcast', methods=['POST'])
def channel_broadcast():
    values = request.json
    # Check that the required fields are in the POST'ed data
    required = ['channel_id']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Publish to channel and create a new Transaction
    values = json.loads(values)
    channel = values["channel_id"]
    for peer in tangle.peers:
        requests.post("http://" + str(peer) + "/channel", channel)

    data = mam_client.read_from_channel(channel)
    response = {'Success': data}
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    # update tangle
    tangle.resolve_conflicts()
    # begin transaction
    values = request.json
    print(values)

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount', 'data']
    if not values or not all(k in values for k in required):
        return jsonify({'Error': 'Missing values'}), 400

    # Create a new Transaction
    node = tangle.send_transaction(values)
    response = node
    # tell peers to update tangle
    for peer in tangle.peers:
        requests.get("http://" + str(peer) + "/peers/resolve")
    return jsonify(response), 201


@app.route('/tangle', methods=['GET'])
def full_chain():
    response = {
        'tangle': tangle.nodes,
        'length': len(tangle.nodes),
    }
    return jsonify(response), 200


@app.route('/peers/register', methods=['POST'])
def register_nodes():
    values = request.get_json()
    print(values)
    print("asdugdag")
    peers = None
    if type("") == type(values):
        print(json.loads(values))
        peers = json.loads(values)['peers']
    else:
        peers = values.get('peers')
    if peers is None:
        return jsonify({"Error": "Please supply a valid list of nodes"}), 400

    for peer in peers:
        tangle.register_peer(peer)

    response = {
        'message': 'New peers have been added',
        'total_nodes': list(tangle.peers),
    }

    return jsonify(response), 201


# Consensus
@app.route('/peers/resolve', methods=['GET'])
def consensus():
    replaced = tangle.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'chain': tangle.nodes
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': tangle.nodes
        }

    return jsonify(response), 200


@app.route('/peers', methods=['GET'])
def list_peers():
    response = {
        'known_peers': list(tangle.peers),
    }

    return jsonify(response), 201


if __name__ == '__main__':
    print("hihihii")
    app.run(port=5000, debug=True)

