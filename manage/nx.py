# -*- coding:utf-8 -*-
"""
@Time:2018/2/25 19:07
@Author:yuhongchao
"""
import networkx as nx
import pandas as pd
import SIR.SIR
import matplotlib.pyplot as plt
from networkx.algorithms import community
from networkx.algorithms.community import k_clique_communities
from propagation.independent_cascade import independent_cascade
from propagation.linear_threshold import linear_threshold
import matplotlib.pyplot as plt
from similarity.jaccard import *


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
    # G=nx.Graph()
    G=nx.DiGraph()
    # G.add_nodes_from([2,3])
    G.add_nodes_from(node_list)
    # print(G.nodes(data=True))

    G.add_weighted_edges_from(edge_list,act_prob=0.8)
    # print(G.edges(data=True))

    # degree = list(G.degree())
    # for temp in degree:
    #     if temp[1]==0:
    #         G.remove_node(temp[0])

    # c = list(k_clique_communities(G, 1))

    # for i in range(len(c)):
    #     nodeL = list(c[i])
    #     print(len(nodeL))
    #     for j in nodeL:
    #         G.node[int(j)]['class'] = i
    # for node,degree in G.degree().item():
    #

    # remove = [node for node, degree in G.degree().items()  if degree == 0]
    # G.remove_nodes_from(remove)
    # print(G.nodes(data = True))
    return G

    # G.add_edges_from(edges)
    # nx.write_gexf(G, 'network.gexf',encoding='utf-8')

def delDegreeOne(G):
    # print(G.number_of_nodes())
    d = nx.degree(G)
    list_de =[]
    for i in d:
        if i[1]==0:
            list_de.append(i[0])
    G.remove_nodes_from(list_de)
    # print(G.number_of_nodes())
    return G
    # pass


def topNBetweeness(G,n):
    score = nx.betweenness_centrality(G)
    score = sorted(score.items(), key=lambda item: item[1], reverse=True)
    print("betweenness_centrality: ", score)
    betweeness = []
    for i in score[:n]:
        betweeness.append(i[0])
    return betweeness
def topNCentility(G,n):
    score = nx.degree_centrality(G)
    score = sorted(score.items(), key=lambda item: item[1], reverse=True)
    print("betweenness_centrality: ", score)
    betweeness = []
    for i in score[:n]:
        betweeness.append(i[0])
    return betweeness
def topNCloseness(G,n):
    score = nx.closeness_centrality(G)
    score = sorted(score.items(), key=lambda item: item[1], reverse=True)
    print("betweenness_centrality: ", score)
    betweeness = []
    for i in score[:n]:
        betweeness.append(i[0])
    return betweeness

def topNDegree(G,n):
    score = nx.degree(G)
    # print(score.items)
    # for i in score:

    score = sorted(score, key=lambda x:x[1], reverse=True)
    print("degree: ", score[:n])

    degree = []
    for i in score[:n]:
        degree.append(i[0])
    return degree
    # output = []
    # for node in score:
    #     output.append(node[0])
    #
    # # print(output)
    # fout = open("betweennessSorted.data", 'w')
    # for target in output:
    #     fout.write(str(target) + " ")

def degree_fenbu(G):
    print(nx.degree_histogram(G))

def move_2(moxing,id,G=None):
    id = int(id)
    layers = []
    print(type(moxing))
    if int(moxing) == 1:
        print("linear_threshold")
        layers = linear_threshold(G, [id])
    elif int(moxing) == 2:
        print("independent_cascade")
        layers = independent_cascade(G, [id])
    print(layers)
    return layers

def move_1(moxing,m,G=None):
    if G==None:
        G = delDegreeOne(get_graph())
    m = int(m)
    if m==3:
        n=1
    elif m==4:
        n=10
    elif m==5:
        n=100
    topDegreelist = topNBetweeness(G, n)
    layers = []
    print(topDegreelist)
    print(type(moxing))
    if int(moxing)==1:
        print("linear_threshold")
        layers = linear_threshold(G,topDegreelist)
    elif int(moxing)==2:
        print("independent_cascade")
        layers = independent_cascade(G, topDegreelist)
    print(layers)
    return layers

def degree_ana(G):
    score = nx.degree(G)

    n1=0
    n2=0
    n3=0
    n4=0
    n5=0
    for i in score:
        if i[1]<=10:
            n1+=1
        elif i[1]>10 and i[1]<=50:
            n2+=1
        elif i[1]>50 and i[1]<=100:
            n3+=1
        elif i[1] > 100:
            n5 += 1

    print(n1,n2,n3,n5)

def get_famility(G):

    ans = jaccard(G)
    li = []
    for source, v in ans.items():
        for target, simil in v.items():
            lis = [source, target, simil]
            li.append(lis)
    print(li)
    fam = pd.DataFrame(data=li, columns=["source", "target", "famility"])
    fam.to_csv("famility.csv")

#
# if  __name__ =="__main__":
#     G = delDegreeOne(get_graph()).to_undirected()
#
#     ans = jaccard(G)
#     li = []
#     for source,v in ans.items():
#         for target,simil in v.items():
#             lis = [source,target,simil]
#             li.append(lis)
#     print(li)
#     fam = pd.DataFrame(data=li,columns=["source", "target", "famility"])
#     fam.to_csv("famility.csv",index=False)

    #现在求每两个用户的相似度，根据他们的userid 直接获得用户的标签，之后根据标签计算相似度






    # degree = nx.degree_histogram(G)
    # x = range(len(degree))
    # y = [z / float(sum(degree)) for z in degree]
    # plt.loglog(x, y, color="blue", linewidth=2)
    # plt.show()
    # dic = degree_ana()
    # topDegreelist = topNBetweeness(G,100)
    # print(topDegreelist)
    # topDegreelist = topNCloseness(G,100)
    # print(dic)

    # print(nx.diameter(G))
    # # degree_fenbu(G)
    # layers = independent_cascade(G,topDegreelist)
    # DG = nx.DiGraph()
    # DG.add_edges_from([(1, 2), (1, 3), (1, 5), (2, 1), (3, 2), (4, 2), (4, 3),  (4, 6), (5, 3), (5, 4), (5, 6), (6, 4), (6, 5)])
    # layers =linear_threshold(DG, [1])
    # sum = 0
    # for i in layers:
    #     sum+=len(i)
    #





    # print(sum)
    # print(len(layers))




    # get_graph_exist()





