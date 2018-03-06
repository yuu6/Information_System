from flask import Flask
from config import DevConfig
from flask import request, render_template, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
from flask import g
import pandas as pd
import csv
import json,math
from collections import Counter
from manage.nx import move_1
# from manage.wight import get_all_sim
import networkx as nx
from similarity.jaccard import jaccard
from similarity.ascos import ascos
DATABASE = 'data_procession/douban.db'

app = Flask(__name__)
app.config.from_object(DevConfig)
usertag = [] #这个里面存储的是用户的标签信息，用于对于用户进行推荐

def connect_db():
    return sqlite3.connect(DATABASE)

@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/second')
def second():
    return render_template('second.html')

@app.route('/network_gexf')
def network_gexf():
    print("run here")
    return render_template('info.gexf')

@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')

@app.route('/tuijian_user')
def tuijian_user():
    dic_tuijian = {}
    userlist = tuijianuser(usertag)
    # print(userlist)
    user = get_userinfo(userlist)
    list_book_name = get_userbookname(userlist)
    list_movie_name = get_usermovie_info(userlist)
    dic_tuijian["user"] = user
    dic_tuijian["book"] = list_book_name
    dic_tuijian["movie"] = list_movie_name
    print(dic_tuijian)
    return jsonify(dic_tuijian)


@app.route('/shejiao_tuijian_2', methods=['Get', 'POST'])
def shejiao_tuijian_2():
    #得到用户id 调用底层的函数
    name = request.args.get("name")
    fam_pd = pd.read_csv("manage/famility.csv")

    tag = []
    sql = "SELECT userid FROM all_tag WHERE name = \"" + name + '\"';

    sql2 = "select DISTINCT  userid from all_tag"
    data = []
    data2= []
    try:
        data = query_db(sql)
        data2 = query_db(sql2)
    except Exception:
        print("查询失败")
    # print(data)
    mubiao_user = data[0]["userid"]
    sim = []
    for i in range(len(data2)):
        tuijian_user = data2[i]["userid"]
        if tuijian_user==mubiao_user:
            continue
        temp_= get_all_sim(mubiao_user, tuijian_user, fam_pd)
        if len(list(temp_))>0:
            sim.append([mubiao_user,tuijian_user,list(temp_)[0]])
    sim.sort(key=lambda x:x[2],reverse=True)
    # print(sim)
    sim1 = []
    for i in range(len(sim)):
        sim1.append(sim[i][1])
    print(sim1)
    userlist = sim1[:6]

    # list1 = data[0]['book_tag'][1:-1].replace("'", "").strip().split(",")
    # list2 = data[0]['movie_tag'][1:-1].replace("'", "").strip().split(",")
    # # print(list1)
    # for j in list1:
    #     tag.append(j)
    # for t in list2:
    #     tag.append(t)
    #
    dic_tuijian = {}
    # userlist = tuijianuser(tag)

    #得到推荐的用户名称列表
    user = get_userinfo(userlist)
    list_book_name = get_userbookname(userlist)
    list_movie_name = get_usermovie_info(userlist)
    dic_tuijian["user"] = user
    dic_tuijian["book"] = list_book_name
    dic_tuijian["movie"] = list_movie_name
    print(dic_tuijian)
    return jsonify(dic_tuijian)

def tuijian_shejiao(name):
    #根据相似度和熟悉度对用户进行排序
    #产生前十的用户

    sql = "SELECT userid from UserNode where username=\""+name+"\""
    userid = query_db(sql)
    id = userid[0]["userid"]
    print(id)
    G_un = delDegreeOne(get_graph()).to_undirected()
    dic_ = jaccard(G_un)
    # filename = 'sim.csv'
    # with open(filename, 'w') as f:  # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    #     csvWriter = csv.writer(f)
    #     for k, v in dic_.items():
    #         csvWriter.writerow([k, v])
    #     f.close()

    # sim = dic[]
    print(dic_[12289])


    return dic_

def get_userbookname(l_):
    li_2= []
    for i in l_:
        sql = 'select BOOK_DETAIL.book_name from BOOK_DETAIL ,UserBook WHERE  UserBook.bookid = BOOK_DETAIL.book_id ' \
              'and UserBook.userid =  \"' + str(i) + '\"';
        data = query_db(sql)
        if len(data)!=0:
            for j in data:
                li_2.append(j["book_name"])
    # print(li_2)
    return li_2

def get_usermovie_info(l_):
    li_2= []
    for i in l_:
        sql = 'select MOVIE_DETAIL.movie_name from MOVIE_DETAIL ,UserMovie WHERE  UserMovie.movieid = MOVIE_DETAIL.movie_id ' \
              'and UserMovie.userid =  \"' + str(i) + '\"';
        data = query_db(sql)
        if len(data)!=0:
            for j in data:
                li_2.append(j["movie_name"])
    # print(li_2)
    return li_2


@app.route('/ciyun', methods=['Get', 'POST'])
def ciyun():
    my_name = request.args.get("user_name")
    print("my_name is " + my_name)
    sql = 'SELECT  * from all_tag WHERE  name = \"' + my_name + '\"'
    print(sql)
    dict = {}
    try:
        data = query_db(sql)
        dict = data[0]
    except Exception:
        print("查询失败")
    movie = str(dict["movie_tag"])
    book = str(dict["book_tag"])
    all = movie.replace("]",",")+book.replace("[","")
    list1 = all[1:-1].replace("'", "").strip().split(",")
    list2 = []
    wordcount = {}
    for i in list1:
        if list1.count(i) >= 1:
            wordcount[i] = list1.count(i)
    for key, values in wordcount.items():
        dict = {}
        dict["name"] = key.strip()
        dict["value"] = values
        list2.append(dict)
    print(list2)
    return jsonify(list2)


@app.route('/username')
def username():
    try:
        name_list = query_db('select DISTINCT name  from UserBook');
        # print(name_list)
    except Exception:
        print("查询失败")
    return jsonify(name_list);


@app.route('/analyse')
def analyse():
    return jsonify([1233]);

@app.route('/bookname')
def bookname():
    try:
        name_list = query_db('select DISTINCT book_name  from BOOK_DETAIL');
        # print(name_list)
    except Exception:
        print("查询失败")
    return jsonify(name_list);


@app.route('/get_tag',methods = ['Get', 'POST'])
def get_tag():
    book_name = request.args.get("book_name")
    movie_name = request.args.get("movie_name")
    tag = []
    if book_name!=[]:
        book_name = json.loads(book_name)
        for i in book_name:
            sql = 'SELECT  book_tag from BOOK_DETAIL WHERE book_name =\"' + i + '\"';
            data = []
            try:
                data = query_db(sql)
                # print(data)
            except Exception:
                print("查询失败")
            # print(data)
            list1 = data[0]['book_tag'][1:-1].replace("'", "").strip().split(",")
            # print(list1)
            for j in list1:
                tag.append(j)

    if movie_name != []:
        movie_name = json.loads(movie_name)
        for i in movie_name:
            sql = 'SELECT  movie_tag from MOVIE_DETAIL WHERE movie_name =\"' + i + '\"';
            try:
                data2 = query_db(sql)
                list2 = data2[0]["movie_tag"][1:-1].replace("'", "").strip().split(",")
                for t in list2:
                    tag.append(t)
            except Exception:
                print("查询失败")
    # print(tag)
    list2 = []
    wordcount = {}
    usertag = tag
    print(usertag)
    for i in tag:
        if tag.count(i) >= 1:
            wordcount[i] = tag.count(i)
    for key, values in wordcount.items():
        dict = {}
        dict["name"] = key.strip()
        dict["value"] = values
        list2.append(dict)
    return jsonify(list2)

@app.route('/moviename')
def moviename():
    try:
        name_list = query_db('select DISTINCT movie_name  from MOVIE_DETAIL');
        # print(name_list)
        # for i in name_list:
        #     # print(i)
        #     name = i["movie_name"]
        #     if len(name)>15:
        #         i["movie_name"] = name[0:5]+"..."+name[-5:]
    except Exception:
        print("查询失败")
    return jsonify(name_list);

@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/tuijian')
def tuijian():
    return render_template('tuijian.html')
@app.route('/shejiao_tuijian')
def shejiao_tuijian():
    return render_template('shejiao_tuijian.html')

@app.route('/move')
def move():
    return render_template('move.html')

@app.route('/cy_data', methods=['Get', 'POST'])
def cy_data():
    # data = {
    #     "elements": {
    #         "edges": [
    #                      {"data": {"relationship": "ACTED_IN", "source": "173", "target": "327"}},
    # ],
    # "nodes": [
    #              {"data": {"id": "173", "label": "Movie", "released": 1999, "tagline": "Welcome to the Real World",
    #                        "title": "The Matrix"}},
    #              {"data": {"born": 1962, "id": "327", "label": "Person", "name": "Tom Cruise"}},
    # ]
    # }
    # }
    #现在需要封装数据，这些数据主要是用户之间的关注信息
        #每个用户是一个顶点，每个用户之间的专注信息是边，应该将顶点分为两部分，一部分是孤立点，另一部分是关联点，
        #我们主要构件的是关联点之间的关系
    sql = 'select * from User_Attention'

    pd_node = pd.DataFrame(columns=["id", "name", "label"])
    data1=query_db(sql)
    #形成的节点
    nodes = []
    for i in range(len(data1)):
        dict_o = {}
        dict = {}
        dict["id"] = str(data1[i]["userid"])
        dict["name"] = data1[i]["name"]
        dict["label"] = data1[i]["name"]
        dict_o["data"] = dict
        nodes.append(dict_o)
        pd_node.loc[pd_node.shape[0] + 1] = {'id': str(data1[i]["userid"]), 'name': data1[i]["name"],'label':data1[i]["name"]}
    pd_node.to_csv("nodes.csv", index=False)
    #形成的边
    # print(nodes)
    edges = []

    # pd_edge = pd.DataFrame(columns=["source","target"])

    for i in range(len(data1)):
        source = str(data1[i]["userid"])
        temp0 = data1[i]["attention_ids"][1:-1].replace("'","").strip().split(",")
        temp = list(set(temp0))
        print(temp)
        if temp != ['']:
            for j in range(len(temp)):
                dict_o = {}
                dict = {}
                dict["source"] = str(source)
                dict["target"] = temp[j].strip()
                dict_o["data"] = dict
                edges.append(dict_o)
                # pd_edge.loc[pd_edge.shape[0] + 1] = {'source':str(source) , 'target': temp[j].strip()}

    # pd_edge.to_csv("edges.csv",index = False)
    return jsonify(elements={"nodes": nodes, "edges": edges})

@app.route('/propagation', methods=['Get', 'POST'])
def propagation():
    print("run here")
    moxing = request.args.get("moxing")
    degree = request.args.get("degree")
    print(moxing,degree)
    G = delDegreeOne(get_graph())
    jieguo = move_1(moxing,degree,G)
    lens = len(jieguo)-1
    output = []
    for i in jieguo:
        node = []
        for j in i:
            node.append(int(j))
        output.append(node)
    return jsonify(output)




@app.route('/get_userbookinfo', methods=['Get', 'POST'])
def get_userbookinfo():
    my_name = request.args.get("user_name")
    print("my_name is " + my_name)
    sql = 'select * from MOVIE_DETAIL ,UserMovie WHERE  UserMovie.movieid = MOVIE_DETAIL.movie_id and UserMovie.name =  \"'+ my_name +'\"';
    print(sql)
    try:
        data = query_db(sql)
        # print(data[0])
    except Exception:
        print("查询失败")
    return jsonify(data)

@app.route('/get_usermovieinfo', methods=['Get', 'POST'])
def get_usermovieinfo():
    my_name = request.args.get("user_name")
    print("my_name is " + my_name)
    sql = 'select * from BOOK_DETAIL ,UserBook WHERE  UserBook.bookid = BOOK_DETAIL.book_id and UserBook.name =  \"'+ my_name +'\"';
    print(sql)
    try:
        data = query_db(sql)
        # print(data[0])
    except Exception:
        print("查询失败")
    return jsonify(data)





@app.route('/get_booktag', methods=['Get', 'POST'])
def get_booktag():
    my_name = request.args.get("book_name")
    print("my_name is " + my_name)
    sql = 'SELECT  book_tag from BOOK_DETAIL WHERE book_name =\"'+ my_name +'\"';
    print(sql)
    try:
        data = query_db(sql)
        # print(data[0])
    except Exception:
        print("查询失败")
    return jsonify(data)

@app.route('/get_movietag', methods=['Get', 'POST'])
def get_movietag():
    my_name = request.args.get("movie_name")
    print("my_name is " + my_name)
    sql = 'SELECT  movie_tag from MOVIE_DETAIL WHERE movie_name =\"'+ my_name +'\"';
    print(sql)
    try:
        data = query_db(sql)
        # print(data[0])
    except Exception:
        print("查询失败")
    return jsonify(data)



@app.route('/get_movie')
def get_movie():
    try:
        data = query_db('select * from MOVIE_DETAIL');
        print(data[0])
    except Exception:
        print("查询失败")
    return jsonify(data)


def tuijianuser(tag):
    # print("Opened database successfully")
    sql1 = "SELECT DISTINCT  userid from UserNode"
    userid = query_db(sql1)
    # print(list(userid))
    dict_ = {}
    for i in list(userid):
        # print(i["userid"])
        s1 = zhixing(i["userid"])
        simi = calcuteSimilar(s1, tag)
        dict_[i["userid"]] = simi

    c = Counter(dict_).most_common()
    # print("qianliuge")
    top_6 = []
    for i in c[:6]:
        top_6.append(int(i[0]))
    # print(top_6)
    return top_6

#使用的是余弦相似度
def calcuteSimilar(series1,series2):
    '''''
    计算余弦相似度
    :param data1: 数据集1 Series
    :param data2: 数据集2 Series
    :return: 相似度
    '''
    # print(len(series1),len(series2))
    # print(series2[0])
    if len(series1)==1 and series1[0]=="":
        return 0.01
    elif len(series2)==1 and series2[0]=='':
        # print("here")
        return 0.01
    unionLen = len(set(series1) & set(series2))
    if unionLen ==0 :
        return 0.01

    if unionLen == 0: return 0.0
    product = len(series1) * len(series2)
    similarity = unionLen / math.sqrt(product)
    return similarity>0 if similarity else 0.01

def get_userinfo(li):
    li_ = []
    for i in li:
        sql = "select * from UserNode where userid  =\""+ str(i) + "\"";
        # print(sql)
        userinfo = query_db(sql)
        # print(userinfo)
        li_.append(userinfo[0])
    # print(li_)
    return li_


def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv

def get_Similar(a,b):
    s1 = zhixing(a)
    s2 = zhixing(b)
    c = calcuteSimilar(s1,s2)
    # print(c)
    return  c

def get_all_sim(a,b,f):
    return get_Similar(a, b)+get_Filmity(a,b,f)

def get_Filmity(a,b,fam_pd):
    str_ = "source == " + a +" & target == "+b
    str_2 = "source == " + b +" & target == "+a
    # print(fam_pd.query(str_2))
    if fam_pd.query(str_) is not None:
        c = fam_pd.query(str_)
        return c["famility"]
    elif fam_pd.query(str_2) is not None:
        c = fam_pd.query(str_2)
        return c["famility"]


def zhixing(a):
    # print("Opened database successfully")
    sql1 = "SELECT  * from all_tag where userid= " + a
    cursor1 = query_db(sql1)
    # print(cursor1)

    str1 = ""
    for row in cursor1:
        if str1 == "":
            str1 = row["book_tag"].replace("]", ",") + row["movie_tag"].replace("[", "")
    # printprint(str1)(str1)
    set1 = str_to_set(str1)
    return set1

def str_to_set(data1):
    temp0 = data1[1:-1].replace("'", "").strip().split(",")
    temp = list(set(temp0))
    return temp

def get_graph():
    nodes_pd = pd.read_csv("dataset/nodes.csv")
    edges_pd = pd.read_csv("manage/edges_wight.csv")
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
    print(G.number_of_nodes())
    d = nx.degree(G)
    list_de =[]
    for i in d:
        if i[1]==0:
            list_de.append(i[0])
    G.remove_nodes_from(list_de)
    print(G.number_of_nodes())
    return G

if __name__ == '__main__':
    app.run()
