from typing import Counter
import networkx as nx
import matplotlib.pyplot as plt
import random
import argparse
import datetime

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

def rand_graph_and_analyze():
    global g_Type
    print (f"Types count: {len(g_Type)}")
    dNodeCnt = random.randint(80,120)
    print (f"Nodes count: {dNodeCnt}")

    gG = nx.erdos_renyi_graph(dNodeCnt, 0.06)
 
    color_map = [g_Type[random.randint(0,2**32 - 1) % len(g_Type)] for node in gG]

    # convert list to dict to attach with every node as attribute
    res_dct = {i: color_map[i] for i in range(0, len(color_map))}
    nx.set_node_attributes(gG, res_dct, name="color")

    node_counter_in_route = random.randint(4,10)
    route_counter = 4

    print (f"Route count: {node_counter_in_route}")

    for n in range(dNodeCnt):
        for nn in gG.neighbors(n):
            edge_attrs = {}
            edge_attrs[(n, nn)] = 'black'
            nx.set_edge_attributes(gG, edge_attrs, "color")

    color_counter = Counter()

    print ('')
    for cnt in range(route_counter):
        local_color_counter = Counter()
        d_groups = []
        d_nodes = []

        cur_node = random.randint(0,dNodeCnt)
        d_nodes.append(cur_node)
        d_groups.append(color_map[cur_node])
        local_color_counter.update([color_map[cur_node]])
        print (f"{cnt}: Start node: {cur_node}")
        for i in range(node_counter_in_route):
            for n in gG.neighbors(cur_node):
                if color_map[cur_node] != color_map[n] and n not in d_nodes:
                    edge_attrs = {}
                    edge_attrs[(cur_node, n)] = g_Type[cnt]
                    nx.set_edge_attributes(gG, edge_attrs, "color")
                    cur_node = n
                    if color_map[cur_node] not in d_groups:
                        d_groups.append(color_map[cur_node])
                    local_color_counter.update([color_map[cur_node]])
                    d_nodes.append(cur_node)
                    break

        # get local percentages per cycle
        color_list_perc = {cc:(local_color_counter[cc] / node_counter_in_route)*100 for cc in local_color_counter}
        print (f"percentage per cycle: {color_list_perc}")

        color_counter.update(local_color_counter)

        print (f"{d_nodes[0]}", end='')
        for n in range(1,len(d_nodes)):
            print (f"->{d_nodes[n]}", end='')

        print ('')

        print (f"{color_map[d_nodes[0]]}", end='')
        for n in range(1,len(d_nodes)):
            print (f"->{color_map[d_nodes[n]]}", end='')
        print ('')
        print ('')

    # get global percentages per all cycles
    color_list_perc = {cc: (color_counter[cc] / (node_counter_in_route*route_counter))*100 for cc in color_counter}
    print (f"global percentages: {color_list_perc}")

    edge_colors = nx.get_edge_attributes(gG,'color').values()
    nx.draw_networkx(gG, with_labels=True, node_color=color_map, edge_color=edge_colors, width=3, node_size=300)

    file_name = datetime.datetime.now().strftime("%m_%d_%Y-%H.%M.%S")

    nx.write_gml(gG, str(file_name+".gml"))

    plt.show()
    return

def parse_args():
    parser = argparse.ArgumentParser(description='Erdos Renyi graph application.')
    parser.add_argument('--rand', dest='rand_graph',type=bool,default=True,
                        help='Choose that param to generate new random graph')

    parser.add_argument('--load', dest='loaded_graph',default='',type=str,
                    help='Choose that param to load graph from file')

    args = parser.parse_args()
    return args

def load_graph_and_analyze(loaded_graph):
    pass

def main():
    args = parse_args()
    
    if args.rand_graph == True:
        rand_graph_and_analyze()
    
    if len(args.loaded_graph) != 0:
        load_graph_and_analyze(args.load_graph)

    return

if __name__ == "__main__":
    main()