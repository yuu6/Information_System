# -*- coding:utf-8 -*-
"""
@Time:2018/1/17 21:20
@Author:yuhongchao
"""

import sqlite3
import pandas as pd

conn = sqlite3.connect('douban.db')
print("Opened database successfully")
c = conn.cursor()

# user_book = pd.read_csv("../dataset/user_book.csv")  # ../dataset/douban_data.csv
# user_movie = pd.read_csv("../dataset/user_movie.csv")  # ../dataset/douban_data.csv
# douban_movie_detail = pd.read_csv("../dataset/douban_movie_detail.csv")  # ../dataset/douban_data.csv
# douban_group = pd.read_csv("../dataset/douban_group.csv")  # ../dataset/douban_data.csv
# douban_book_detail = pd.read_csv("../dataset/modelData/BookDetail.csv")  # ../dataset/douban_data.csv
# print(len(douban_book_detail))
# for i in range(len(douban_book_detail)):
#     # print(douban_book_detail.iloc[i]["bookid"])
#     id = int(douban_book_detail.iloc[i]['bookid'])
#     name = douban_book_detail.iloc[i]['bookname']
#     detail = douban_book_detail.iloc[i]['bookdetail']
#     rate = douban_book_detail.iloc[i]['bookrate']
#     tag = douban_book_detail.iloc[i]['booktag']
#     c.execute("INSERT INTO BOOK_DETAIL (book_id,book_name,book_rate,book_detail,book_tag)"
#               " VALUES (?,?, ?, ?, ?)", (id, name, rate, detail, tag));

movie_detail = pd.read_csv("../dataset/modelData/UserMovie.csv")  # ../dataset/douban_data.csv
print(len(movie_detail))
for i in range(len(movie_detail)):
    # print(douban_book_detail.iloc[i]["bookid"])
    um_id = movie_detail.iloc[i]['um_id']
    uid = movie_detail.iloc[i]['userid']
    name = movie_detail.iloc[i]['name']
    movieid = movie_detail.iloc[i]['movieid']
    print(movieid)
    # c.execute("INSERT INTO USER_MOVIE (um_id,user_id,user_name,movie_id)"
    #           " VALUES (?,?,?,?)", (um_id, uid, name, movieid));

print("insert database successfully")

conn.commit()
conn.close()