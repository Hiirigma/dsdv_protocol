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

route_counter = 4
node_counter_in_route = 7

def rand_graph_and_analyze():
    global g_Type, route_counter, node_counter_in_route
    print (f"Types count: {len(g_Type)}")
    node_counts = random.randint(80,120)
    print (f"Nodes count: {node_counts}")

    G = nx.erdos_renyi_graph(node_counts, 0.06)
 
    color_map = [g_Type[random.randint(0,2**32 - 1) % len(g_Type)] for node in G]

    # convert list to dict to attach with every node as attribute
    res_dct = {i: color_map[i] for i in range(0, len(color_map))}
    nx.set_node_attributes(G, res_dct, name="color")

    print (f"Route count: {node_counter_in_route}")

    for n in range(node_counts):
        for nn in G.neighbors(n):
            edge_attrs = {}
            edge_attrs[(n, nn)] = 'black'
            nx.set_edge_attributes(G, edge_attrs, "color")

    color_counter = Counter()

    print ('')

    saved_start_nodes = []
    for cnt in range(route_counter):
        local_color_counter = Counter()
        d_groups = []
        d_nodes = []

        cur_node = random.randint(0,node_counts)
        saved_start_nodes.append(cur_node)
        d_nodes.append(cur_node)
        d_groups.append(color_map[cur_node])
        local_color_counter.update([color_map[cur_node]])
        print (f"{cnt}: Start node: {cur_node}")
        for i in range(node_counter_in_route):
            for n in G.neighbors(cur_node):
                if color_map[cur_node] != color_map[n] and n not in d_nodes:
                    edge_attrs = {}
                    edge_attrs[(cur_node, n)] = g_Type[cnt]
                    nx.set_edge_attributes(G, edge_attrs, "color")
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

    edge_colors = nx.get_edge_attributes(G,'color').values()
    nx.draw_networkx(G, with_labels=True, node_color=color_map, edge_color=edge_colors, width=3, node_size=300)

    file_name = datetime.datetime.now().strftime("%m_%d_%Y-%H.%M.%S")

    nx.write_gml(G, str(file_name+".gml"))

    with open(file_name+".nodes", "w") as f:
        for item in saved_start_nodes:
            # write each item on a new line
            f.write("%d\n" % item)

    with open(file_name+".colors", "w") as f:
        for item in color_map:
            # write each item on a new line
            f.write("%s\n" % item)

    plt.show()
    return

def load_graph_and_analyze(file_name):
    global g_Type, route_counter, node_counter_in_route
    G = nx.read_gml(file_name+".gml")

    saved_start_nodes = []
    with open(file_name+".nodes", "r") as f:
        for line in f:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            saved_start_nodes.append(int(x))

    color_map = []
    idx = 0
    with open(file_name+".colors", "r") as f:
        for line in f:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            color_map.append(x)
            idx += 1

    color_counter = Counter()

    print ('')
    for cnt in range(route_counter):
        local_color_counter = Counter()
        d_groups = []
        d_nodes = []

        cur_node = saved_start_nodes[cnt]
        d_nodes.append(cur_node)
        d_groups.append(color_map[cur_node])
        local_color_counter.update([color_map[cur_node]])
        print (f"{cnt}: Start node: {cur_node}")
        for i in range(node_counter_in_route):
            for n in G.neighbors(str(cur_node)):
                if color_map[cur_node] != color_map[int(n)] and int(n) not in d_nodes:
                    edge_attrs = {}
                    edge_attrs[(cur_node, int(n))] = g_Type[cnt]
                    nx.set_edge_attributes(G, edge_attrs, "color")
                    cur_node = int(n)
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

    edge_colors = nx.get_edge_attributes(G,'color').values()

    idx = 0

    # remove color from map
    for node in G.nodes:
        if idx != int(node):
             del color_map[idx]
             idx += 1
             if idx != int(node):
                del color_map[idx]
                
        idx += 1

    nx.draw_networkx(G, with_labels=True, node_color=color_map, edge_color=edge_colors, width=3, node_size=300)

    file_name = datetime.datetime.now().strftime("%m_%d_%Y-%H.%M.%S")

    # nx.write_gml(G, str(file_name+".gml"))
    # with open(file_name+".nodes", "w") as f:
    #     for item in saved_start_nodes:
    #         # write each item on a new line
    #         f.write("%d\n" % item)
    # with open(file_name+".colors", "w") as f:
    #     for item in color_map:
    #         # write each item on a new line
    #         f.write("%s\n" % item)

    plt.show()
    return

def load_graph_and_change(file_name):
    global g_Type, route_counter, node_counter_in_route
    G = nx.read_gml(file_name+".gml")

    saved_start_nodes = []
    with open(file_name+".nodes", "r") as f:
        for line in f:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            saved_start_nodes.append(int(x))

    color_map = []
    idx = 0
    with open(file_name+".colors", "r") as f:
        for line in f:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            color_map.append(x)
            idx += 1

    while 1:
        print(f"Nodes: {G.nodes}")
        print("Select node to delete it > ")
        node = 0
        node = int(input())
        
        if node < 0:
            break

        if str(node) not in G:
            continue

        G.remove_node(str(node))

    file_name = datetime.datetime.now().strftime("%m_%d_%Y-%H.%M.%S")

    nx.write_gml(G, str(file_name+".gml"))
    with open(file_name+".nodes", "w") as f:
        for item in saved_start_nodes:
            # write each item on a new line
            f.write("%d\n" % item)
    with open(file_name+".colors", "w") as f:
        for item in color_map:
            # write each item on a new line
            f.write("%s\n" % item)


def parse_args():
    parser = argparse.ArgumentParser(description='Erdos Renyi graph application.')
    parser.add_argument('--rand', dest='rand_graph',type=bool,default=False,
                        help='Choose that param to generate new random graph')

    parser.add_argument('--load', dest='loaded_graph',default='',type=str,
                    help='Choose that param to load graph from file without extension')

    parser.add_argument('--change', dest='change_graph',default='',type=str,
                    help='Choose that param to load graph from file without extension and change it\'s nodes')

    args = parser.parse_args()
    return args

def main():
    args = parse_args()
    
    if args.rand_graph == True:
        rand_graph_and_analyze()
    
    if len(args.loaded_graph) != 0:
        load_graph_and_analyze(args.loaded_graph)

    if len(args.change_graph) != 0:
        load_graph_and_change(args.change_graph)

    return

if __name__ == "__main__":
    main()