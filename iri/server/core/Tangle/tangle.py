import properties as prop
import json
from time import time
import hashlib
import requests
from urllib.parse import urlparse
import redis

# https://docs.iota.org/docs/client-libraries/1.0/overview
# https://blog.iota.org/the-tangle-an-illustrated-introduction-4d5eae6fe8d4/


class MAMClient:
    def __init__(self, tangle, host=None, port=None):
        self.tangle = tangle
        if not host:
            host = prop.mamClientHost
        if not port:
            port = prop.mamClientPort
        self.client = redis.Redis(host=host, port=port, db=0)
        self.channels = []
        self.channels_data = {}

    def get_channel_id(self, channel_id):
        if channel_id and channel_id in self.channels:
            return channel_id
        return ""

    def create_channel_id(self, seed):
        client = json.dumps(seed, sort_keys=True).encode()
        channel = hashlib.sha256(client).hexdigest().upper()
        if channel not in self.channels:
            self.channels.append(channel)
            self.channels_data[channel] = []
        return channel

    def publish_to_channel(self, channel_id, data):
        # update tangle
        self.tangle.resolve_conflicts()
        node = self.tangle.send_transaction(data)
        # now publish to channel
        self.client.publish(channel_id, node)
        self.channels_data[channel_id].append(node)
        return node

    def subscribe_channel(self, channel_id):
        if channel_id not in self.channels:
            return False
        sub_obj = self.client.pubsub()
        sub_obj.subscribe(channel_id)
        return True

    def read_from_channel(self, channel_id):
        if channel_id not in self.channels_data:
            return []
        return self.channels_data[channel_id]


class TangleClient:
    def __init__(self):
        self.address = []

    def generate_address(self, seed):
        client = json.dumps(seed, sort_keys=True).encode()
        address = hashlib.sha256(client).hexdigest().upper()
        if address not in self.address:
            self.address.append(address)
        return address


class Tangle(object):
    def __init__(self):
        self.nodes = []
        self.peers = set()
        for i in range(prop.numberOfValidationNodesNeeded):
            # Genesis block
            self.nodes.append(
                self.create_node(None, [], len(self.nodes), validity=prop.RequiredProofs))

    @staticmethod
    def valid_proof(last_proof, last_hash, proof):
        # last 4 char are - 0
        guess = (str(last_proof) + str(last_hash) + str(proof)).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def proof_of_work(self, last_proof, last_hash):
        # PoW
        proof = 0
        while self.valid_proof(last_proof, last_hash, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def block_hash(node):
        # make a hash of the block
        # We must make sure that the Dictionary is Ordered, or we'll have inconsistent hashes
        node_string = json.dumps(node, sort_keys=True).encode()
        return hashlib.sha256(node_string).hexdigest()

    def validate_node(self, node):
        if self.nodes[node['index']]['validity'] < prop.RequiredProofs:
            last_proof = self.nodes[node['index']]['proof']  # this nodes proof
            last_hash = ""
            for prevHash in self.nodes[node['index']]['previous_hashs']:
                # the hashes of the nodes this node connects
                last_hash += prevHash
            self.nodes[node['index']]['proof'] = self.proof_of_work(last_proof, last_hash)
            self.nodes[node['index']]['validity'] += 1

    def create_node(self, data, prevNodes, newIndex, validity=0):
        # these prevNodes are the  indexes in the dag that points to the previous nodes
        prevHashes = []
        '''
        may need to update every node that points to this when sending transaction
        '''
        for i in prevNodes:
            prevHashes.append(self.block_hash(self.nodes[i]))
            # now we tell the nodes that we are pointing to that we are poiinting to them
            self.nodes[i]['next_nodes'].append(newIndex)

        Node = {
            'index': newIndex,
            'timestamp': time(),
            'proof': 0,
            'previous_hashs': prevHashes,  # hashes of the nodes we are connecting to
            'previous_nodes': prevNodes,  # indexes of the nodes we are connecting to
            'next_nodes': [],  # indexes of future nodes that will connect to us
            'validity': validity,
            'block_data': data,
        }
        return Node

    def send_transaction(self, data):
        # find 2 nodes in the network that are un proven
        nodesToattach = []
        nodesIndexes = []
        newIndex = len(self.nodes)
        worstCaseScinario = []
        worstCaseScinarioindexes = []
        '''
        this function should be changed to search randomly
        '''
        for i in range(len(self.nodes) - 1, -1, -1):
            node = self.nodes[i]
            if node['validity'] < prop.RequiredProofs:
                nodesToattach.append(node)
                nodesIndexes.append(node['index'])
            else:
                if worstCaseScinario == [] or len(
                        worstCaseScinario) < prop.numberOfValidationNodesNeeded:
                    worstCaseScinario.append(node)
                    worstCaseScinarioindexes.append(node['index'])
            if len(nodesToattach) == prop.numberOfValidationNodesNeeded:
                break
        # if there are not enough un verified transactions then use verified transactions
        while len(nodesToattach) < prop.numberOfValidationNodesNeeded:
            nodesToattach.append(worstCaseScinario.pop())
            nodesIndexes.append(worstCaseScinarioindexes.pop())
        # process nodes to attach
        for node in nodesToattach:
            self.validate_node(node)
        # now that those nodes are proven
        # we can now attatch our node to the dag
        self.nodes.append(self.create_node(data, nodesIndexes, newIndex))
        return self.nodes[-1]

    def valid_tangle(self, tangle):
        # consensus
        for node in tangle:
            if node['index'] >= prop.numberOfValidationNodesNeeded:  # dont test genesis nodes
                validitiyOfNode = node['validity']
                # make sure that the same number of nodes saying that they have
                # validated him as his validity level
                nextNodes = node['next_nodes']
                print(nextNodes)
                if validitiyOfNode < len(nextNodes):
                    return False
                # make sure these nodes are pointing to him
                for Nnode in nextNodes:
                    print(tangle[Nnode])
                    if node['index'] not in tangle[Nnode]['previous_nodes']:
                        return False
        return True

    def register_peer(self, address):
        parsed_url = urlparse(address)
        self.peers.add(parsed_url.netloc)

    def resolve_conflicts(self):
        neighbours = self.peers
        new_tangle = None

        # We're only looking for chains longer than ours
        max_length = len(self.nodes)

        # Grab and verify the chains from all the peers in our network
        for peer in neighbours:
            response = requests.get("http://" + str(peer) + "/tangle")

            if response.status_code == 200:
                length = response.json()['length']
                tangle = response.json()['tangle']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_tangle(tangle):
                    max_length = length
                    new_tangle = tangle

        # Replace our chain if we discovered a new, valid chain longer than ours
        if new_tangle:
            self.nodes = new_tangle
            return True

        return False
