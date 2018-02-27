# -*- coding:utf-8 -*-
"""
@Time:2018/2/25 19:07
@Author:yuhongchao
"""
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities

def get_graph():
    nodes_pd = pd.read_csv("../dataset/nodes.csv")
    edges_pd = pd.read_csv("../manage/edges_wight.csv")
    #使用一个tuple  (node, attrdict) 构建node
    node_list = []

    for indexs in nodes_pd.index:
        dict = {}
        node = nodes_pd.loc[indexs].values[0]
        dict["name"] = nodes_pd.loc[indexs].values[1]
        dict["label"] = nodes_pd.loc[indexs].values[2]
        tup1 = (node,dict)
        node_list.append(tup1)

    edge_list = []
    for indexs in edges_pd.index:
        node1 = int(edges_pd.loc[indexs].values[0])
        node2 = int(edges_pd.loc[indexs].values[1])
        weight = edges_pd.loc[indexs].values[2]
        tup2 = (node1, node2, weight)
        edge_list.append(tup2)
    # print(node_list)
    G=nx.Graph()
    # G.add_nodes_from([2,3])
    G.add_nodes_from(node_list)
    # print(G.nodes(data=True))

    G.add_weighted_edges_from(edge_list)
    # print(G.edges(data=True))

    degree = list(G.degree())
    for temp in degree:
        if temp[1]==0:
            G.remove_node(temp[0])

    c = list(k_clique_communities(G, 1))

    for i in range(len(c)):
        nodeL = list(c[i])
        print(len(nodeL))
        for j in nodeL:
            G.node[int(j)]['class'] = i
    # for node,degree in G.degree().item():
    #

    # remove = [node for node, degree in G.degree().items()  if degree == 0]
    # G.remove_nodes_from(remove)
    print(G.nodes(data = True))
    # G.add_edges_from(edges)
    nx.write_gexf(G, 'network.gexf',encoding='utf-8')

def get_graph_exist():
    G = nx.read_gexf("../templates/info.gexf")
    print(G.nodes(data = True))

if __name__ =="__main__":
    # get_graph()
    get_graph_exist()





