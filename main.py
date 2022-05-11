from typing import Counter
import networkx as nx
import matplotlib.pyplot as plt
import random

g_Type = [
    'red',
    'green',
    'blue',
    'grey',
    'yellow',
    'orange',
    'purple',
    'maroon',
    'aqua',
    'brown',
    'pink',
    'violet',
    'navy',
    'silver',
    'cyan',
]

def GenerateRandomGraph():
    global g_Type
    print (f"Types count: {len(g_Type)}")
    dNodeCnt = random.randint(80,120)
    print (f"Nodes count: {dNodeCnt}")

    gG = nx.erdos_renyi_graph(dNodeCnt, 0.06)
 
    color_map = [g_Type[random.randint(0,2**32 - 1) % len(g_Type)] for node in gG]

    # convert list to dict to attach with every node as attribute
    res_dct = {i: color_map[i] for i in range(0, len(color_map))}
    nx.set_node_attributes(gG, res_dct, name="color")

    dRouteCnt = random.randint(4,10)

    print (f"Route count: {dRouteCnt}")

    for n in range(dNodeCnt):
        for nn in gG.neighbors(n):
            edge_attrs = {}
            edge_attrs[(n, nn)] = 'black'
            nx.set_edge_attributes(gG, edge_attrs, "color")

    color_counter = Counter()

    for cnt in range(4):
        d_groups = []
        d_nodes = []

        cur_node = random.randint(0,dNodeCnt)
        d_nodes.append(cur_node)
        d_groups.append(color_map[cur_node])
        print (f"{cnt}: Start node: {cur_node}")
        for i in range(dRouteCnt):
            for n in gG.neighbors(cur_node):
                if color_map[cur_node] != color_map[n] and n not in d_nodes:
                    edge_attrs = {}
                    edge_attrs[(cur_node, n)] = g_Type[cnt]
                    nx.set_edge_attributes(gG, edge_attrs, "color")
                    cur_node = n
                    if color_map[cur_node] not in d_groups:
                        d_groups.append(color_map[cur_node])
                    d_nodes.append(cur_node)
                    break

        color_counter.update(d_groups)
        print (f"groups: {d_groups}")

        print (f"{d_nodes[0]}", end='')
        for n in range(1,len(d_nodes)):
            print (f"->{d_nodes[n]}", end='')

        print ('')

        # TODO:
        # Think about counter in this place
        print (f"{color_map[d_nodes[0]]}", end='')
        for n in range(1,len(d_nodes)):
            print (f"->{color_map[d_nodes[n]]}", end='')
        print ('')

    print (f"Counter: {color_counter}")

    edge_colors = nx.get_edge_attributes(gG,'color').values()

    # print("edges")
    # print(list(gG.edges(data=True)))
    # print("default graph attributes")
    # print(gG.graph)
    # print("node attributes")
    # print(gG.nodes.data(True))
    nx.draw_networkx(gG, with_labels=True, node_color=color_map, edge_color=edge_colors, width=3, node_size=300)
    
    plt.show()
    return

def main():
    GenerateRandomGraph()
    return

if __name__ == "__main__":
    main()