from flask import Flask
from config import DevConfig
from flask import request, render_template, jsonify
# from flask.ext.sqlalchemy import SQLAlchemy
import sqlite3
from flask import g

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
