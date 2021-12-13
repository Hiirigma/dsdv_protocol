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

gG = None
gI = None
gIprev = None
gSlow = 0.1

gPath = []
gRouteTable = []
# route = {"table"}
# route = {"hops"}
# index = src node
# { id: weight }

def BellmanFord(graph, source: int) -> dict[int, float] | None:
    global gG, gSlow
    n = len(graph.nodes)
    predecessor = []

    for i in range(n):
        predecessor.append(-1)

    vertices = graph.nodes
    # A[i] is dist from the source with a budget of i edges
    A: list[dict[str, float]] = [
        {v: math.inf for v in vertices} for _ in range(n + 1)
    ]
    A[0][source] = 0

    adj = []

    for _ in graph.nodes:
        adj.append(set())

    # not crutch
    prev = -1
    for node1 in graph.edges:
        l = []
        if (node1[0] <= prev):
            continue
        for node2 in graph.edges:
            prev = node1[0]
            if node1[0] == node2[0]:
                adj[node2[1]].add(prev)
                l.append(node2[1])
        adj[prev].update(set(l))

    for i in range(1, n + 1):
        A[i] = A[i - 1].copy()
        for w in graph.nodes:
            for v in adj[w]:
                if (A[i - 1][w] + 1 < A[i][v]):
                    # time.sleep(gSlow)
                    A[i][v] = A[i - 1][w] + 1
                    # gI.node_artists[w].set_color('green')
                    predecessor[v] = w
                #else:
                    #gI.node_artists[w].set_color('blue')

    if A[n] != A[n - 1]:
        return None

    return A[n - 1], predecessor

def ParseRoute(srcNode, dstNode):
    global gG, gI, gIprev, gRouteTable, gPath

    gRouteTable.clear()
    for i in range(len(gI.nodes)):
        A, predecessor = BellmanFord(gI,i)
        route = {}
        route["table"] = A
        route["hops"] = predecessor
        gRouteTable.append(route)

    if (gRouteTable == []):
        print('route table is empty')
        exit(-1)

    # time.sleep(5)
    cur = dstNode

    if (gPath!= None and len(gPath) != 0):
        for node in gPath:
            gI.node_artists[node].set_color('blue')

    gPath.clear()

    while cur != -1 and cur != srcNode:
        gPath.append(cur)
        cur = gRouteTable[srcNode]["hops"][cur]

    gPath.append(srcNode)

    for node in gPath:
        gI.node_artists[node].set_color('red')

    # os.startfile('foo2.png', 'open')
    print (f"Path from {srcNode} to {dstNode} is: {gPath}")
    weight = gRouteTable[srcNode]["table"][dstNode]
    print (f"With weight: {weight}")

    return

def GenerateRandomGraph():
    global gG, gI, gIprev, gRouteTable
    # random node's count
    rand1 = 10
    rand2 = 20

    dNodeCnt = random.randint(10,20)
    # Probability for edge creation (optimal - 0.22)
    # fig, ax = plt.subplots()
    gG = nx.gnp_random_graph(dNodeCnt, 0.22)
    # add weight
    for u, v, w in gG.edges.data():    
        gG.add_weighted_edges_from([(u, v, 1)])
    # spring_layout - good view of graph
    # nodes labels - number
    # edge labels - weights
    labels = nx.get_edge_attributes(gG,'weight')
    # nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G,weight='weight'),edge_labels=labels)
    # nx.draw(G,pos=nx.spring_layout(G,weight='weight'), with_labels=True)
    # plt.savefig('foo1.png', bbox_inches='tight')
    # plt.clf()
    # os.startfile('foo1.png', 'open')

    color_map = ['blue' for node in gG]

    color_map = dict()
    for node in gG:
        color_map[node] = 'tab:blue'

    gIprev = gI = netgraph.EditableGraph(gG,node_labels=True, node_color=color_map, node_label_bbox=dict(fc="lightgreen", ec="black", boxstyle="square", lw=5),
                                node_size=5,)

    # fig.canvas.draw()
    plt.show()
    return


def ChangeGraph():
    global gG
    while gG == None:
        1
    while 1:
        srcNode = int(input("Input src node (or -1): "))
        if (srcNode < 0 or srcNode > len(gG)):
            print('Bad src node name')
            exit(-1)

        dstNode = int(input("Input dst node: "))
        if (dstNode < 0 or dstNode > len(gG)):
            print('Bad dst node name')
            exit(-1)
        
        if (srcNode == dstNode):
            print('Bad dst or src node name')
            exit(-1)

        ParseRoute(srcNode,dstNode)

def CheckGraphAndUpdate():
    global gI, gIprev

    while gI == None or gIprev == None:
        time.sleep(5) 
        continue
    while 1:
        time.sleep(4)
        if gI != gIprev:
            gIprev = gI
            gRouteTable.clear()
            for i in range(len(gI.nodes)):
                A, predecessor = BellmanFord(gI,i)
                route = {}
                route["table"] = A
                route["hops"] = predecessor
                gRouteTable.append(route)

    return

def main():
    thread = Thread(target = ChangeGraph)
    thread.start()

    thread1 = Thread(target = CheckGraphAndUpdate)
    thread1.start()

    GenerateRandomGraph()

    return

if __name__ == "__main__":
    main()