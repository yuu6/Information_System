# -*- coding:utf-8 -*-
"""
@Time:2018/1/17 21:05
@Author:yuhongchao
"""
import sqlite3

conn = sqlite3.connect('douban.db')
print("Opened database successfully")
c = conn.cursor()

c.execute('''DROP TABLE USER_MOVIE;''')


# c.execute('''CREATE TABLE BOOK_DETAIL
#        (book_id TEXT      NOT NULL,
#        book_name           TEXT    NOT NULL,
#        book_rate            REAL,
#        book_detail        CHAR(500),
#        book_tag         CHAR(500));''')
#
# c.execute('''CREATE TABLE MOVIE_DETAIL
#        (movie_id TEXT      NOT NULL,
#        movie_name           TEXT    NOT NULL,
#        movie_rate            REAL,
#        movie_detail        CHAR(500),
#        movie_tag         CHAR(500));''')
#
#
# c.execute('''CREATE TABLE USER_GROUP
#        (user_id TEXT     NOT NULL,
#        user_name           TEXT    NOT NULL,
#        group_name           TEXT,
#        group_tag         CHAR(500));''')
# c.execute('''CREATE TABLE USER_MOVIE
#        (user_id TEXT     NOT NULL,
#        user_name           TEXT    NOT NULL,
#        movie_id         TEXT    NOT NULL);''')
c.execute('''CREATE TABLE USER_MOVIE
       ( um_id TEXT  PRIMARY KEY     NOT NULL,
       user_id TEXT      NOT NULL,
       user_name           TEXT     ,
       movie_id           TEXT    );''')

print("Table created successfully")
conn.commit()
conn.close()