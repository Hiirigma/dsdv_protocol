# TODO:
# + random graph generation
# + node choosing
# + generate route
# Destination-Sequenced Distance Vector Routing 
import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import math
from threading import Thread
import netgraph
import time

G = None
I = None

gPath = []
gRouteTable = []
# route = {"table"}
# route = {"hops"}
# index = src node
# { id: weight }

def ParseRoute(srcNode, dstNode):
    global G, I, gRouteTable, gPath
    if (gRouteTable == []):
        print('route table is empty')
        exit(-1)

    cur = dstNode

    if (gPath!= None and len(gPath) != 0):
        for node in gPath:
            I.node_artists[node].set_color('blue')

    gPath.clear()

    while cur != -1 and cur != srcNode:
        gPath.append(cur)
        cur = gRouteTable[srcNode]["hops"][cur]

    gPath.append(srcNode)

    for node in gPath:
        I.node_artists[node].set_color('red')

    # os.startfile('foo2.png', 'open')
    print (f"Path from {srcNode} to {dstNode} is: {gPath}")
    weight = gRouteTable[srcNode]["table"][dstNode]
    print (f"With weight: {weight}")

    return

def BellmanFord(
    graph: dict[int, dict[int, float]], source: int
) -> dict[int, float] | None:
    global G, fig, gRouteTable
    n = len(graph)
    predecessor = []

    for i in range(n):
        predecessor.append(-1)

    vertices: set[int] = set(graph.adj) | {
        w for v in graph for w in graph[v]
    }
    # A[i] is dist from the source with a budget of i edges
    A: list[dict[str, float]] = [
        {v: math.inf for v in vertices} for _ in range(n + 1)
    ]
    A[0][source] = 0

    for i in range(1, n + 1):
        A[i] = A[i - 1].copy()
        for w in graph:
            for v in graph[w]:
                if (A[i - 1][w] + graph[w][v]['weight'] < A[i][v]):
                    A[i][v] = A[i - 1][w] + graph[w][v]['weight']
                    predecessor[v] = w

    if A[n] != A[n - 1]:
        return None

    return A[n - 1], predecessor


def GenerateRandomGraph():
    global G, I, gRouteTable
    # random node's count
    rand1 = 10
    rand2 = 20

    dNodeCnt = random.randint(10,20)
    # Probability for edge creation (optimal - 0.22)
    # fig, ax = plt.subplots()
    G = nx.gnp_random_graph(dNodeCnt, 0.22)
    # add weight
    for u, v, w in G.edges.data():    
        G.add_weighted_edges_from([(u, v, 1)])
    # spring_layout - good view of graph
    # nodes labels - number
    # edge labels - weights
    labels = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G,weight='weight'),edge_labels=labels)
    # nx.draw(G,pos=nx.spring_layout(G,weight='weight'), with_labels=True)
    # plt.savefig('foo1.png', bbox_inches='tight')
    # plt.clf()
    # os.startfile('foo1.png', 'open')

    for i in range(len(G)):
        A, predecessor = BellmanFord(G,i)
        route = {}
        route["table"] = A
        route["hops"] = predecessor
        gRouteTable.append(route)

    color_map = ['blue' for node in G]

    color_map = dict()
    for node in G:
        color_map[node] = 'tab:blue'

    I = netgraph.EditableGraph(G,node_labels=True, node_color=color_map, node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=5),
                                node_size=5,)

    # fig.canvas.draw()
    plt.show()
    return

def UpdateGraph():
    srcNode = int(input("Input src node (or -1): "))
    if (srcNode < 0 or srcNode > len(G)):
        print('Bad src node name')
        exit(-1)

    dstNode = int(input("Input dst node: "))
    if (dstNode < 0 or dstNode > len(G)):
        print('Bad dst node name')
        exit(-1)    

    return

def ChangeGraph():
    global G
    while G == None:
        1
    while 1:
        if (G == None):
            print ('graph doesn\'t exists')
            exit(-1)

        srcNode = int(input("Input src node (or -1): "))
        if (srcNode < 0 or srcNode > len(G)):
            print('Bad src node name')
            exit(-1)

        dstNode = int(input("Input dst node: "))
        if (dstNode < 0 or dstNode > len(G)):
            print('Bad dst node name')
            exit(-1)
        
        if (srcNode == dstNode):
            print('Bad dst or src node name')
            exit(-1)

        ParseRoute(srcNode,dstNode)

def main():
    thread = Thread(target = ChangeGraph)
    thread.start()
    GenerateRandomGraph()
    # ChangeGraph()
    #thread.join()

    return

if __name__ == "__main__":
    main()