# -*- coding:utf-8 -*-
"""
@Time:2018/2/25 19:07
@Author:yuhongchao
"""
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

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
    print(node_list)
    G=nx.Graph()
    # G.add_nodes_from([2,3])
    G.add_nodes_from(node_list)
    # print(G.nodes(data=True))

    G.add_weighted_edges_from(edge_list)
    print(G.edges(data=True))
    # G.add_edges_from(edges)
    nx.write_gexf(G, 'network.gexf',encoding='utf-8')

if __name__ =="__main__":
    get_graph()





