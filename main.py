# TODO:
# + random graph generation
# + node choosing
# - generate route
import networkx as nx
import matplotlib.pyplot as plt
import random
import os
import math

from networkx.generators.classic import null_graph

gRouteTable = []
# route = {"table"}
# route = {"hops"}
# index = src node
# { id: weight }

def ParseRoute(G, srcNode, dstNode):
    if (gRouteTable == []):
        print('route table is empty')
        exit(-1)

    cur = dstNode
    path = []

    while cur != -1 and cur != srcNode:
        path.append(cur)
        cur = gRouteTable[srcNode]["hops"][cur]

    print (f"Path from {srcNode} to {dstNode} is: {path}")
    weight = gRouteTable[srcNode]["table"][dstNode]
    print (f"With weight: {weight}")

    return

def BellmanFord(
    graph: dict[int, dict[int, float]], source: int
) -> dict[int, float] | None:
    """Bellman-Ford algorithm
    O(n m) time, O(n^2) space (with a sliding row space would be O(m))
    Based on Tim Roughgarden's lectures
    :returns: shortest distances from the source to all the graph's vertices
    or None for negative cycle
    """
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
    # random node's count
    rand1 = 10
    rand2 = 20

    dNodeCnt = random.randint(10,20)
    # Probability for edge creation (optimal - 0.22)
    G = nx.gnp_random_graph(dNodeCnt, 0.22)
    # add weight
    for u, v, w in G.edges.data():    
        G.add_weighted_edges_from([(u, v, 1)])
    # spring_layout - good view of graph
    # nodes labels - number
    # edge labels - weights
    # labels = nx.get_edge_attributes(G,'weight')
    # nx.draw_networkx_edge_labels(G,pos=nx.spring_layout(G,weight='weight'),edge_labels=labels)
    nx.draw(G,pos=nx.spring_layout(G,weight='weight'), with_labels=True)
    # print (G.edges())
    plt.savefig('foo.png', bbox_inches='tight')
    os.startfile('foo.png', 'open')
    for i in range(len(G)):
        A, predecessor = BellmanFord(G,i)
        route = {}
        route["table"] = A
        route["hops"] = predecessor
        gRouteTable.append(route)

    return G

def main():
    G = GenerateRandomGraph()
    while 1:
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

        ParseRoute(G,srcNode,dstNode)

    return


if __name__ == "__main__":
    main()