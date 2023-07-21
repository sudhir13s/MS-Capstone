import datetime
import random
import time

import networkx as nx
import matplotlib.pyplot as plt
import scipy
from networkx import to_directed
import pydot
from time import gmtime, strftime
from datetime import datetime

get_time = lambda: datetime.now().strftime("%H:%M:%S")
tm1 = get_time()
time.sleep(round(random.uniform(0.50, 0.01), 4))
tm2 = get_time()

get_name = lambda x: f'{str(datetime.now().microsecond)}_{x}.jpg'
fcname1 = get_name(1)
time.sleep(0.001)
fcname2 = get_name(2)

time.sleep(0.001)
dcname1 = get_name(1)
time.sleep(0.001)
dcname2 = get_name(2)


OFMD_DATA11 = [{"block_data": {"amount": "0", "data": [{"POS": "0.93", "TIME": "21:37:13",
                                                        "VELOCITY": "0.37"},
                                                       {"SERVICE": "MONITOR"}], "recipient": "FC1",
                               "sender": "FMD"}, "index": 2, "next_nodes": [],
                "previous_hashs": [
                    "c24202dc3f377b183eb9eec754948b4ed9fd111b2492e7b5a0869762a43dec60",
                    "9e128a391912b9d8a95dacaec771bd30e6db7cc849a492a0f13e97731de3300c"],
                "previous_nodes": [0, 1], "proof": 0, "timestamp": 1619746338.746644, "validity": 0}
               ]

OFMD_DATA12 = [{"block_data": {"amount": "0",
                               "data": [{"POS": "0.93", "TIME": "21:37:13",
                                         "VELOCITY": "0.37"},
                                        {"SERVICE": "MONITOR"}], "recipient": "DC",
                               "sender": "FMD"},
                "index": 3, "next_nodes": [],
                "previous_hashs": [
                    "34c82544dc95f00fb878a3498531b72321b7f09bf33ab8b7da1e5ae68311eed3",
                    "353570becff3f250b687328ea9577795c0af11e5860f8908fc824a55772c7ef2"],
                "previous_nodes": [2, 0], "proof": 0, "timestamp": 1619746461.6215098,
                "validity": 0}
               ]

OFMD_DATA13 = [{"block_data": {"amount": "0", "data": [{"POS": "0.93", "TIME": "21:37:13",
                                                        "VELOCITY": "0.37"},
                                                       {"SERVICE": "MONITOR"}], "recipient": "DL",
                               "sender": "FMD"}, "index": 4, "next_nodes": [],
                "previous_hashs": [
                    "bdc8487e6632298066a9061bd79eb50917fcd1779a48b69e1351e3b2d8aeff39",
                    "8ce1bf8f51b670e7ff2148818fd4aa29d1564953b5773f9ffc6135a8881da6dd"],
                "previous_nodes": [3, 2], "proof": 0, "timestamp": 1619746485.45936, "validity": 0}
               ]

OFMD_DATA21 = [{"block_data": {"amount": "0", "data": [{"POS": "0.32", "TIME": "21:37:18",
                                                        "VELOCITY": "0.11"},
                                                       {"SERVICE": "MONITOR"}], "recipient": "FC1",
                               "sender": "FMD"}, "index": 2, "next_nodes": [],
                "previous_hashs": [
                    "c24202dc3f377b183eb9eec754948b4ed9fd111b2492e7b5a0869762a43dec60",
                    "9e128a391912b9d8a95dacaec771bd30e6db7cc849a492a0f13e97731de3300c"],
                "previous_nodes": [0, 1], "proof": 0, "timestamp": 1619746338.746644, "validity": 0}
               ]

OFMD_DATA22 = [{"block_data": {"amount": "0",
                               "data": [{"POS": "0.32", "TIME": "21:37:18",
                                         "VELOCITY": "0.11"},
                                        {"SERVICE": "MONITOR"}], "recipient": "DC",
                               "sender": "FMD"},
                "index": 3, "next_nodes": [],
                "previous_hashs": [
                    "34c82544dc95f00fb878a3498531b72321b7f09bf33ab8b7da1e5ae68311eed3",
                    "353570becff3f250b687328ea9577795c0af11e5860f8908fc824a55772c7ef2"],
                "previous_nodes": [2, 0], "proof": 0, "timestamp": 1619746461.6215098,
                "validity": 0}
               ]

OFMD_DATA23 = [{"block_data": {"amount": "0", "data": [{"POS": "0.32", "TIME": "21:37:18",
                                                        "VELOCITY": "0.11"},
                                                       {"SERVICE": "MONITOR"}], "recipient": "DL",
                               "sender": "FMD"}, "index": 4, "next_nodes": [],
                "previous_hashs": [
                    "bdc8487e6632298066a9061bd79eb50917fcd1779a48b69e1351e3b2d8aeff39",
                    "8ce1bf8f51b670e7ff2148818fd4aa29d1564953b5773f9ffc6135a8881da6dd"],
                "previous_nodes": [3, 2], "proof": 0, "timestamp": 1619746485.45936, "validity": 0}
               ]

FC1_DATA11 = [{"block_data": {"amount": "0",
                              "data": [
                                  {"AUTHORIZED": "NO", "IMAGE": "396535_1.jpg", "PERSON":
                                      "UNKNOWN"},
                                  {"SERVICE": "AUTHENTICATE"}], "recipient": "DC", "sender": "FC1"},
               "index": 5, "next_nodes": [],
               "previous_hashs": [
                   "720fd1e14585b5a8120ac3a5db225a02a50fbe501ff7af4d86b77c77e9e1c33e",
                   "9183b8975a0716d20c4036710aa583c861e233224d9721025036abf08358d481"],
               "previous_nodes": [4, 3], "proof": 0, "timestamp": 1619746712.9628868, "validity": 0}

              ]
FC1_DATA12 = [{"block_data": {"amount": "0",
                              "data": [
                                  {"AUTHORIZED": "NO", "IMAGE": "396535_1.jpg", "PERSON":
                                      "UNKNOWN"},
                                  {"SERVICE": "AUTHENTICATE"}], "recipient": "DL", "sender": "FC1"},
               "index": 7, "next_nodes": [],
               "previous_hashs": [
                   "ec574498cf4183f0e5e0b7d34bff5c903510d38c88e199e9c02efb2b5bf5308a",
                   "598e7669092670f6a7a0147010e86c3b5159fb32a6a8b9e821237ab2cdc0792c"],
               "previous_nodes": [6, 5], "proof": 0, "timestamp": 1619746821.279696, "validity": 0}

              ]
FC1_DATA13 = [{"block_data": {"amount": "0",
                              "data": [
                                  {"AUTHORIZED": "NO", "IMAGE": "396535_1.jpg", "PERSON":
                                      "UNKNOWN"},
                                  {"SERVICE": "ALERT"}], "recipient": "HC", "sender": "FC1"},
               "index": 8, "next_nodes": [],
               "previous_hashs": [
                   "c4ea78a1c28035fea1535678eebb660781937814d024fe8faee02bbe7f27ddc6",
                   "ff8250f825af307e806ee4319fb370f004fe9dff340d36b19b05ceab74902d3a"],
               "previous_nodes": [7, 6], "proof": 0, "timestamp": 1619746867.059011, "validity": 0}
              ]

VS111 = [{"block_data": {"amount": "0", "data": [
    {"AMPLITUDE": "57", "FREQUENCY": "170900"}, {"SERVICE": "ALERT"}],
                         "recipient": "HC", "sender": "VS1"}, "index": 9, "next_nodes": [],
          "previous_hashs": ["9089465e1201f67547e5d139fe363fc44b9c20797e39eed6ccfafa8022fbfa29",
                             "5ca4cd93799140ae8226a37bec6b7f6708f594da69ce5f361437695a9cfab9de"],
          "previous_nodes": [8, 7], "proof": 0, "timestamp": 1619747100.373667, "validity": 0}
         ]

USS1_DATA11 = [{"block_data": {"amount": "0", "data": [
    {"SOUND": "0.034", "DISTANCE": "9", "TIME": "23:10:45"}, {"SERVICE": "ALERT"}],
                               "recipient": "HC", "sender": "USS1"}, "index": 10, "next_nodes": [],
                "previous_hashs": [
                    "880c44c826d5b6dc6d973b7f2a8caeeb9418c829fbec59f952993aeda97cc04c",
                    "a2e0d84fd301f6db067099ac213cc9a19e3e3511889686952378ef643daab80f"],
                "previous_nodes": [9, 8], "proof": 0, "timestamp": 1619747133.917804, "validity": 0}
               ]

USS1_DATA21 = [
    {"block_data": {"amount": "0", "data": [
        {"SOUND": "0.031", "DISTANCE": "3", "TIME": "23:10:50"},
        {"SERVICE": "ALERT"}], "recipient": "HC",
                    "sender": "USS1"}, "index": 11, "next_nodes": [],
     "previous_hashs": ["7b1a585c615f1dc0a97d09136af9b96de9287bbf2b3bed6844f93a46cb8f5c8a",
                        "0f504405ccb25cbdf923ecb92283b983f7a1eb22987213a9ee8ae4c2aa75b638"],
     "previous_nodes": [10, 9], "proof": 0, "timestamp": 1619747230.181203, "validity": 0}
]

HC_DATA11 = [{"block_data": {"amount": "0",
                             "data": [{"POWER": "ON"},
                                      {"SERVICE": "LIGHT"}],
                             "recipient": "SL1", "sender": "HC"}, "index": 12, "next_nodes": [],
              "previous_hashs": ["b9a3592e033aadeb371e321ab08cd6d38fc7a0ef5a59de24a3762480504f860a",
                                 "8d51df82c14975d66c9d1c5dbcfb46021b58e603bc3d6876e530f586f3657231"],
              "previous_nodes": [11, 10], "proof": 0, "timestamp": 1619747492.6768692,
              "validity": 0}
             ]

HC_DATA12 = [{"block_data": {"amount": "0",
                             "data": [{"ALARM": "RING", "SOUND": "MAX"}, {"SERVICE": "ALERT"}],
                             "recipient": "AL1", "sender": "HC"}, "index": 13, "next_nodes": [],
              "previous_hashs": ["2c85899eca752cb7e32391c9c1baf40ccbe1ddd088b74d249ed581b74aba4a72",
                                 "0dd23658ca6189a821a4c4448bc6d372f97fc61e56dd42680c6152dc36f6c957"],
              "previous_nodes": [12, 11], "proof": 0, "timestamp": 1619747580.584586, "validity": 0}
             ]

HC_DATA13 = [{"block_data": {"amount": "0",
                             "data": [[{"AUTHORIZED": "NO", "IMAGE": "396535_1.jpg", "PERSON":
                                 "UNKNOWN"},
                                       {"AMPLITUDE": "57", "FREQUENCY": "170900"}],
                                      {"SERVICE": "ALERT"}],
                             "recipient": "HO", "sender": "HC"}, "index": 14, "next_nodes": [],
              "previous_hashs": ["bd0ed3cd6ad02d04705d58010aab75f704dc491b9575a63289f5ca1f69c7146c",
                                 "654f1a5de2561abb93677f7e7becc6f49f00f25e09ee3b281dc26c79131fb17a"],
              "previous_nodes": [13, 12], "proof": 0, "timestamp": 1619747657.351687, "validity": 0}
             ]

EVENT_DATA = [OFMD_DATA11, OFMD_DATA12, OFMD_DATA13,
              FC1_DATA11, FC1_DATA12, FC1_DATA13,
              VS111,
              USS1_DATA11, USS1_DATA21,
              HC_DATA11, HC_DATA12, HC_DATA13
              ]


def main():
    G = nx.DiGraph(directed=True)
    for event in EVENT_DATA:
        bundle = event[0]
        bundle_data = bundle.get("block_data")
        i_data = bundle_data.get("data")
        frm = bundle_data.get("sender")
        to = bundle_data.get("recipient")
        data = i_data[0]
        ser = i_data[1].get("SERVICE")

        data12 = None
        node_attrs = nx.get_node_attributes(G, 'DATA')
        for node, attr in node_attrs.items():
            if frm == node:
                data1 = str(data)
                if data1 not in attr:
                    if isinstance(data, list):
                        b = ""
                        for el in data:
                            b = f"{el}\n{b}"
                        data12 = f"{attr}\n{b}"
                    else:
                        data12 = f"{attr}\n{data1}"
                    break
                else:
                    data12 = attr

        if data12:
            data13 = data12
        else:
            data13 = str(data)

        G.add_node(frm, DATA=data13)
        G.add_node(to)
        G.add_edge(frm, to, SERVICE=ser)

    # print(G.edges.data())
    # for edge in G.edges.data():
    #     print(edge[2].get("data"))
    #     labels["data"]
    node = G.nodes
    size = [800 for _ in range(len(node))]
    edge_labels = nx.get_edge_attributes(G, 'SERVICE')
    plt.figure(figsize=(14, 10))
    plt.box(False)
    pos = nx.spring_layout(G, k=0.8, iterations=1, scale=20)
    nx.draw(G, pos, with_labels=True, node_size=900, node_color='lightblue')
    # pos = nx.nx_pydot.graphviz_layout(G)
    pos_attrs = {}
    for node, coords in pos.items():
        pos_attrs[node] = (coords[0], coords[1] + 1.9)

    node_attrs = nx.get_node_attributes(G, 'DATA')
    custom_node_attrs = {}
    for node, attr in node_attrs.items():
        custom_node_attrs[node] = attr

    # nx.draw_networkx_nodes(G, pos=pos_attrs, node_size=800, node_color='lightblue')
    nx.draw_networkx_labels(G, pos=pos_attrs, labels=custom_node_attrs)

    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos=pos)
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_labels, arrows=True,
                           arrowsize=25)

    print(EVENT_DATA)
    plt.box(False)
    plt.title("Front Break-in home event", fontsize=20)
    plt.show()


if __name__ == '__main__':
    main()
