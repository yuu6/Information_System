# -*- coding:utf-8 -*-
"""
@Time:2018/1/22 18:01
@Author:yuhongchao
"""
import sqlite3
import pandas
import pandas as pd


conn= sqlite3.connect("douban.db")
df = pandas.read_csv('../dataset/attention.csv')
df.to_sql('User_Attention', conn, if_exists='append', index=False)
print('ok')
