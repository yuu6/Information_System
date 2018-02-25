from flask import Flask
from config import DevConfig
from flask import request, render_template, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
from flask import g
import pandas as pd
import csv

DATABASE = 'data_procession/douban.db'

app = Flask(__name__)
app.config.from_object(DevConfig)


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

@app.route('/userinfo')
def userinfo():
    return render_template('userinfo.html')


@app.route('/username')
def username():
    try:
        name_list = query_db('select DISTINCT name  from UserBook');
        # print(name_list)
    except Exception:
        print("查询失败")
    return jsonify(name_list);

@app.route('/network')
def network():
    return render_template('network.html')

@app.route('/tuijian')
def tuijian():
    return render_template('tuijian.html')

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



@app.route('/get_userbookinfo', methods=['Get', 'POST'])
def get_userbookinfo():
    my_name = request.args.get("user_name")
    print("my_name is " + my_name)
    sql = 'select * from MOVIE_DETAIL ,UserMovie WHERE  UserMovie.movieid = MOVIE_DETAIL.movie_id and UserMovie.name =  \"'+ my_name +'\"';
    print(sql)
    try:
        data = query_db(sql);
        print(data[0])
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




def query_db(query, args=(), one=False):
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv


if __name__ == '__main__':
    app.run()
