# -*- coding:utf-8 -*-
"""
@Time:2018/2/25 19:11
@Author:yuhongchao
"""
import sqlite3
from flask import g
import pandas as pd
import math
from collections import Counter
"""计算用户之间的相似度"""
def get_movie_tag():
    DATABASE = '../data_procession/douban.db'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # print("Opened database successfully")
    movie_tag = pd.DataFrame(columns=['userid','username','movietag'])
    cursor = c.execute("SELECT userid, name, movie_tag  FROM UserMovie  u left JOIN MOVIE_DETAIL b ON u.movieid = b.movie_id")
    curr_userid = 0
    curr_name = ""
    stri = ""
    for row in cursor:
        if curr_userid == 0:
            curr_userid = row[0]
            curr_name = row[1]
            stri = str(row[2])
        else:
            if curr_userid !=row[0]:
                movie_tag.loc[movie_tag.shape[0] + 1] = {'userid':curr_userid,'username':curr_name,'movietag':stri}
                curr_userid = row[0]
                curr_name = row[1]
                stri = str(row[2])
            else:
                stri = stri.replace("]",",") + str(row[2]).replace("[","")
    movie_tag.to_csv("movie_tag.csv",index = False)
    # print("Operation done successfully")
    conn.close()

def get_book_tag():
    DATABASE = '../data_procession/douban.db'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # print("Opened database successfully")
    movie_tag = pd.DataFrame(columns=['userid','username','booktag'])
    cursor = c.execute("SELECT userid,name , book_tag  from UserBook  u left join BOOK_DETAIL b on u.bookid = b.book_id")
    curr_userid = 0
    curr_name = ""
    stri = ""
    for row in cursor:
        if curr_userid == 0:
            curr_userid = row[0]
            curr_name = row[1]
            stri = str(row[2])
        else:
            if curr_userid !=row[0]:
                movie_tag.loc[movie_tag.shape[0] + 1] = {'userid':curr_userid,'username':curr_name,'booktag':stri}
                curr_userid = row[0]
                curr_name = row[1]
                stri = str(row[2])
            else:
                stri = stri.replace("]",",") + str(row[2]).replace("[","")
    movie_tag.to_csv("book_tag.csv",index = False)
    print("Operation done successfully")
    conn.close()

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
    return similarity

def str_to_set(data1):
    temp0 = data1[1:-1].replace("'", "").strip().split(",")
    temp = list(set(temp0))
    return temp

def zhixing(a):
    DATABASE = '../data_procession/douban.db'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # print("Opened database successfully")
    sql1 = "SELECT  * from all_tag where userid= " + a
    cursor1 = c.execute(sql1)

    str1 = ""
    for row in cursor1:
        if str1 == "":
            str1 = row[2].replace("]", ",") + row[3].replace("[", "")
    # printprint(str1)(str1)
    set1 = str_to_set(str1)
    conn.close()
    return set1

def get_Similar(a,b):
    s1 = zhixing(a)
    s2 = zhixing(b)
    return  calcuteSimilar(s1,s2)

def get_Filmity(a,b):
    fam_pd = pd.read_csv("famility.csv")
    print(fam_pd)
    str_ = "source == " + a +" & target == "+b
    str_2 = "source == " + b +" & target == "+a
    # print(fam_pd.query(str_2))
    if fam_pd.query(str_) is not None:
        c = fam_pd.query(str_)
        return c["famility"]
    elif fam_pd.query(str_2) is not None:
        c = fam_pd.query(str_2)
        return c["famility"]


def get_all_sim(a,b):
    return get_Similar(a, b)+get_Filmity(a,b)

def tuijianuser(tag):
    DATABASE = '../data_procession/douban.db'
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    # print("Opened database successfully")
    sql1 = "SELECT DISTINCT  userid from UserNode"
    userid = c.execute(sql1)
    # print(list(userid))
    dict_ = {}
    for i in list(userid):
        print(i[0])
        s1 = zhixing(i[0])
        simi = calcuteSimilar(s1, tag)
        dict_[i[0]] = simi
    conn.close()
    c = Counter(dict_).most_common()
    print(c)
    return dict_

if __name__ =="__main__":
    print(get_all_sim("12287","11233"))
    #得到每个用户的标签 13402 10000 13404 13409
    # get_movie_tag()
    # get_book_tag()
    # 讲这样的标签转化为向量
    # book = pd.read_csv("book_tag.csv")
    # movie = pd.read_csv("movie_tag.csv")
    # all = book.join(movie,how="outer",lsuffix='_caller', rsuffix='_other')
    # print(all.columns)
    # all.drop(["userid_other","username_other"],axis=1,inplace=True)
    # all.to_csv("all.csv", index=False)
    #
    # DATABASE = '../data_procession/douban.db'
    # conn = sqlite3.connect(DATABASE)
    # c = conn.cursor()
    # # print("Opened database successfully")
    # sql1 = "SELECT DISTINCT  userid from UserNode"
    # userid = list(c.execute(sql1))
    # list_ = []
    #
    # for i in range(len(userid)):
    #     print(userid[i][0])
    #     for j in range(i,len(userid)):
    #         li_=[userid[i][0],userid[j][0],get_Similar(userid[i][0],userid[j][0])]
    #         list_.append(li_)
    #
    #
    # print(li_)

    # conn.close()
    #计算相似度

    # ed_pd = pd.read_csv("../dataset/edges.csv")
    # ed_pd["wight"] = None
    # ed_pd["wight"] = ed_pd.apply(lambda row:get_Similar(str(row['source']),str(row['target'])),axis=1)
    # ed_pd.to_csv("edges_wight.csv",index=False)
    # print(get_Similar("10012","10009"))
    # pass
    # list_ = []
    # list_.append('日本')
    # list_.append('小说')
    # list_.append('治愈系')
    # tuijianuser(list_)
