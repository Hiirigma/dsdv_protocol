# TODO:
# + random graph generation
# + node choosing
# + generate route
# Destination-Sequenced Distance Vector Routing 
import networkx as nx
import matplotlib.pyplot as plt
import random
import math
from threading import Thread
import netgraph
import time

gG = None
gI = None
gSlow = 0.1

gSrcNode = -1
gDstNode = -1

gPath = []
gRouteTable = []
gSavedEdges = None
gDefaultCount = 0

gMaxEdgeDif = 0.2
# route = {"table"}
# route = {"hops"}
# index = src node
# { id: weight }

def BellmanFord(graph, source: int) -> dict[int, float] | None:
    global gG, gSlow, gSavedEdges, gDefaultCount
    n = len(graph.nodes)
    predecessor = []

    lMax = max(gDefaultCount,max(gG.nodes))

    for _ in range(lMax + 1):
        predecessor.append(-1)

    vertices = graph.nodes
    # A[i] is dist from the source with a budget of i edges
    A: list[dict[str, float]] = [
        {v: math.inf for v in vertices} for _ in range(n + 1)
    ]
    A[0][source] = 0

    adj = []

    for _ in range(lMax + 1):
        adj.append(set())

    # not crutch
    for _ in range(len(graph.edges)):
        node1 = graph.edges[_]
        l = []
        for node2 in graph.edges:
            if node1[0] == node2[0]:
                adj[node2[1]].add(node1[0])
                l.append(node2[1])
                _+=1
        if len(l) != 0:
            _ -= 1

        adj[node1[0]].update(set(l))

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
    global gG, gI, gRouteTable, gPath

    gRouteTable.clear()
    for i in gI.nodes:
        A, predecessor = BellmanFord(gI,i)
        route = {}
        route["table"] = A
        route["hops"] = predecessor
        gRouteTable.append(route)

    if (gRouteTable == []):
        print('route table is empty')
        exit(-1)

    if gSrcNode not in gI.nodes or \
    gDstNode not in gI.nodes:
        for node in gI.nodes:
            gI.node_artists[node].set_color('blue')
        return

    # time.sleep(5)
    cur = dstNode

    for node in gI.nodes:
        gI.node_artists[node].set_color('blue')

    gPath.clear()

    while cur != -1 and cur != srcNode:
        gPath.append(cur)
        cur = gRouteTable[srcNode]["hops"][cur]

    gPath.append(srcNode)

    weight = gRouteTable[srcNode]["table"][dstNode]
    if (weight != math.inf):
        print (f"Path from {srcNode} to {dstNode} is: {gPath}")
        for node in gPath:
            gI.node_artists[node].set_color('red')
    
    print (f"With weight: {weight}")

    return

def GenerateRandomGraph():
    global gG, gI, gSavedEdges, gDefaultCount
    # random node's count
    rand1 = 10
    rand2 = 20

    dNodeCnt = random.randint(5,10)
    # Probability for edge creation (optimal - 0.22)
    # fig, ax = plt.subplots()
    gG = nx.gnp_random_graph(dNodeCnt, 0.5)
    # add weight
    for u, v, w in gG.edges.data():    
        gG.add_weighted_edges_from([(u, v, 1)])

    labels = nx.get_edge_attributes(gG,'weight')
    gDefaultCount = len(gG)
 
    color_map = ['blue' for node in gG]

    color_map = dict()
    for node in gG:
        color_map[node] = 'blue'

    gI = netgraph.EditableGraph(gG,node_labels=True, node_color=color_map,node_size=3,)

    gSavedEdges = gI.edges.copy()
    plt.show()
    return


def ChangeGraph():
    global gG, gI, gSrcNode, gDstNode
    while gG == None:
        1

    while 1:
        gSrcNode = int(input("Input src node (or -1): "))

        gDstNode = int(input("Input dst node: "))
        
        if (gSrcNode == gDstNode):
            print('Bad dst or src node name')
            continue

        ParseRoute(gSrcNode, gDstNode)

def CheckGraphAndUpdate():
    global gI, gSavedEdges

    while gI == None or gSavedEdges == None:
        time.sleep(5) 
        continue
    while 1:
        time.sleep(4)
        if gI.edges != gSavedEdges:
            gRouteTable.clear()
            ParseRoute(gSrcNode, gDstNode)
            gSavedEdges = gI.edges.copy()

    return

def CheckDistance():
    global gI

    while gI == None:
        time.sleep(5) 
        continue
    while 1:
        time.sleep(3)
        for node_pos1 in gI.node_positions:
            for node_pos2 in gI.node_positions:

                if node_pos1 == node_pos2:
                    continue

                # Return the Euclidean norm, sqrt(x*x + y*y). This is the length of the vector from the origin to point (x, y).
                dist = math.hypot(gI.node_positions[node_pos2][0] - gI.node_positions[node_pos1][0], 
                gI.node_positions[node_pos2][1] - gI.node_positions[node_pos1][1])

                if (dist > gMaxEdgeDif):
                    if ((node_pos1,node_pos2) in gI.edges) or \
                        ((node_pos2, node_pos1) in gI.edges):
                        gI._delete_edge((node_pos1,node_pos2))
                else:
                    if ((node_pos1,node_pos2) not in gI.edges) and \
                    ((node_pos2, node_pos1) not in gI.edges):
                        gI._add_edge((node_pos1,node_pos2))
                        # try to change weights
                        # gG.add_weighted_edges_from([(node_pos1, node_pos2, dist)])

def main():
    tComputeRoute = Thread(target = ChangeGraph)
    tComputeRoute.start()

    tCheckGraphChanges = Thread(target = CheckGraphAndUpdate)
    tCheckGraphChanges.start()

    tCheckDist = Thread(target = CheckDistance)
    tCheckDist.start()

    GenerateRandomGraph()

    return

if __name__ == "__main__":
    main()