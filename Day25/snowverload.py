#!/usr/bin/env python3 -u

import sys
from collections import defaultdict
import networkx as nx

def main():
    filename = sys.argv[1]

    E = defaultdict(set)

    with open(filename, 'r') as file:
        for line in file:
            v, connected_v = line.strip().split(': ')
            E[v] = set(connected_v.split())

    # print(f"{len(E)=} {E=}")

    G = nx.Graph()

    for k, vs in E.items():
        for v in vs:
            G.add_edge(k, v, capacity=1.0)
            G.add_edge(v, k, capacity=1.0)

    # print(f"{G.nodes=}")
    # print(f"{list(G.nodes)=}")

    V = list(G.nodes)
    src = V[0]
    for sink in V[1:]:
        cut_value, (L,R) = nx.minimum_cut(G, src, sink)
        if cut_value == 3:
            # print(f"{L=}\n{R=}")
            print(len(L)*len(R))
            break


if __name__ == "__main__":
    main()