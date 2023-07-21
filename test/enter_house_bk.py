import datetime
import time

import networkx as nx
import matplotlib.pyplot as plt
import scipy
from networkx import to_directed
import pydot
from time import gmtime, strftime

get_time = lambda: strftime("%H:%M:%S", gmtime())

OFMD_DATA = [
    {f"POS: 0.97", "VELOCITY: 0.15", f"TIME : {get_time()}"},
    {f"POS: 0.27", "VELOCITY: 0.15", f"TIME : {get_time()}"}
]

get_name = lambda x: f'image_{str(datetime.datetime.now().microsecond)}_{x}.jpg'

FC1_DATA = [
    {f"IMAGE : {get_name(1)} ", "AUTHC: YES", "AUTHR: YES"},
    {f"IMAGE : {get_name(2)} ", "AUTHC: YES", "AUTHR: YES"},
]

DC_DATA = [
    {f"IMAGE : {get_name(1)} ", "AUTHC: YES", "AUTHR: YES"},
    {f"IMAGE : {get_name(2)} ", "AUTHC: YES", "AUTHR: YES"},
]

DL_DATA = [
    {"AUTHC: YES", "AUTHR: YES"},
    {"AUTHC: YES", "AUTHR: YES"},
]

HC_DATA = [
    {"POWER: ON", "COLOR: BLUE"},
    {"POWER: ON", "CHANNEL: 41"},
    {"TEMP: OUTSIDE"}
]

EVENT_DATA = [
    # OFMD
    [{"FROM": "OFMD", "TO": "FC1", "DATA": OFMD_DATA[0]}],
    [{"FROM": "OFMD", "TO": "DL", "DATA": OFMD_DATA[0]}],
    [{"FROM": "OFMD", "TO": "DC", "DATA": OFMD_DATA[0]}],
    # FC1
    [{"FROM": "FC1", "TO": "DL", "DATA": FC1_DATA[0]}],
    [{"FROM": "FC1", "TO": "DC", "DATA": FC1_DATA[0]}],
    [{"FROM": "FC1", "TO": "HC", "DATA": FC1_DATA[0]}],
    # DC
    [{"FROM": "DC", "TO": "DL", "DATA": DC_DATA[0]}],
    [{"FROM": "DC", "TO": "HC", "DATA": DC_DATA[0]}],
    # DL
    [{"FROM": "DL", "TO": "HC", "DATA": DC_DATA[0]}],

    # OFMD
    # [{"FROM": "OFMD", "TO": "FC1", "DATA": OFMD_DATA[1]}],
    # [{"FROM": "OFMD", "TO": "DL", "DATA": OFMD_DATA[1]}],
    # [{"FROM": "OFMD", "TO": "DC", "DATA": OFMD_DATA[1]}],

    # HC
    [{"FROM": "HC", "TO": "SL1", "DATA": HC_DATA[0]}],
    [{"FROM": "HC", "TO": "TV1", "DATA": HC_DATA[1]}],
    [{"FROM": "HC", "TO": "TS", "DATA": HC_DATA[2]}],

]


def main():
    G = nx.DiGraph(directed=True)

    i = 1
    pos = {}
    size = []
    pos[i] = "OFMD"
    labels = {}
    for event in EVENT_DATA:
        # print(event[0])
        to, frm, data = event[0].get("TO"), event[0].get("FROM"), event[0].get("DATA")

        G.add_node(frm, data=frm)
        G.add_node(to, data=to)
        # G.add_edges_from([(to, frm)])
        G.add_edge(frm, to, data=data)
        # G[frm][to]["data"] = data

        # pos[i] = to
        # i += 1

    # print(G.edges.data())
    # for edge in G.edges.data():
    #     print(edge[2].get("data"))
    #     labels["data"]
    node = G.nodes
    size = [800 for _ in range(len(node))]
    # labels["data"] = nx.get_node_attributes(G, 'data')
    # print(labels)
    # print(size, node)
    #
    # pos = nx.spring_layout(G)
    # nx.draw(G, pos, node_size=size)
    # for a in G.nodes.items():
    #     print(a)

    # node_labels = nx.get_node_attributes(G, 'data')
    # print(node_labels)
    # nx.draw_networkx_labels(G, pos, labels=node_labels)
    edge_labels = nx.get_edge_attributes(G, 'data')
    # print(edge_labels)
    # nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    #
    # plt.figure(figsize=(50,20))
    # plt.show()

    plt.figure(figsize=(14, 12))
    pos = nx.spring_layout(G, k=15, iterations=70)
    # pos = nx.nx_pydot.graphviz_layout(G)

    nx.draw_networkx_nodes(G, pos=pos, node_size=800, node_color='lightblue')
    nx.draw_networkx_labels(G, pos=pos)
    print(edge_labels)
    nx.draw_networkx_edge_labels(G, pos=pos)
    nx.draw_networkx_edges(G, pos=pos, edgelist=edge_labels, arrows=True,
                           arrowsize=20)

    plt.box(False)
    plt.show()



if __name__ == '__main__':
    main()
