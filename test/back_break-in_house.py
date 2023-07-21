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
    {f"POS: 1.39", "VELOCITY: 0.45", f"TIME: {get_time()}"},
    {f"POS: 0.65", "VELOCITY: 0.15", f"TIME: {get_time()}"}
]

get_name = lambda x: f'{str(datetime.datetime.now().microsecond)}_{x}.jpg'

name1 = get_name(1)
name3 = get_name(3)

FC1_DATA = [
    {f"IMAGE: {name1}", "AUTHR: NO", "PERSON: UNKNOWN"},
    {f"IMAGE: {get_name(2)}", "AUTHR: NO", "PERSON: UNKNOWN"},
]

BC1_DATA = [
    {f"IMAGE: {name1}", "AUTHR: NO", "PERSON: UNKNOWN"},
    {f"IMAGE: {get_name(2)}", "AUTHR: NO", "PERSON: UNKNOWN"},
]


DC_DATA = [
    {f"IMAGE: {name3}", "AUTHR: NO", "PERSON: UNKNOWN"},
    {f"IMAGE: {get_name(4)}", "AUTHR: NO", "PERSON: UNKNOWN"},
]

DL_DATA = [
    {"AUTHR: NO", "OPEN: NO"},
    {"AUTHR: NO", "OPEN: NO"},
]

HC_DATA = [
    {f"TIME: {get_time()}", f"ALERT: {name1}", f"ALERT: {name3}"},
    {f"TIME: {get_time()}", "POWER: ON"},
    # {f"TIME: {get_time()}", "POWER: OFF"}
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
    [{"FROM": "DL", "TO": "HC", "DATA": DL_DATA[0]}],

    # OFMD
    # [{"FROM": "OFMD", "TO": "FC1", "DATA": OFMD_DATA[1]}],
    # [{"FROM": "OFMD", "TO": "DL", "DATA": OFMD_DATA[1]}],
    # [{"FROM": "OFMD", "TO": "DC", "DATA": OFMD_DATA[1]}],

    # HC
    [{"FROM": "HC", "TO": "HO", "DATA": HC_DATA[0]}],
    [{"FROM": "HC", "TO": "SL1", "DATA": HC_DATA[1]}],
    # [{"FROM": "HC", "TO": "TS", "DATA": HC_DATA[2]}],

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
    plt.title("Back Break-in home event", fontsize=20)
    plt.show()


if __name__ == '__main__':
    main()
