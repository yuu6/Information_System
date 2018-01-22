# -*- coding:utf-8 -*-
"""
@Time:2018/1/17 9:24
@Author:yuhongchao
"""
import pandas as pd
from bs4 import BeautifulSoup

#将标签属性变为列表
def tag_to_list(a_str):
    a_str = a_str.replace('\n', '').replace("\xa0 ",",")
    a_str = a_str.split(",")
    re_list = []
    for i in range(len(a_str)):
        if a_str[i].strip() !=None:
            re_list.append(a_str[i].strip())
    return re_list

#将信息属性变为字典
def detail_to_dict(a_html):
    a_dict = dict()

    soup = BeautifulSoup(a_html)
    if soup.a:
        a_dict['作者'] = str(soup.a.string).replace("\n", "").replace(" ", "").strip()

    author = soup.find('span')
    if author:
        author.extract()
    author = soup.find('a')
    if author:
        author.extract()
    author = soup.find('a')
    if author:
        author.extract()

    #     print(a_dict)

    aList = soup.get_text().split("\n")
    for i in range(len(aList)):
        if "出版社" in str(aList[i]):
            chubanshe = str(aList[i]).split(":")
            if (len(chubanshe) == 2):
                a_dict["出版社"] = chubanshe[1]
        elif "ISBN" in str(aList[i]):
            isbn = str(aList[i]).split(":")
            if (len(isbn) == 2):
                a_dict["ISBN"] = isbn[1]
        elif "定价" in str(aList[i]):
            price = str(aList[i]).split(":")
            if (len(price) == 2):
                a_dict["定价"] = price[1]
        elif "页数" in str(aList[i]):
            pages = str(aList[i]).split(":")
            if (len(pages) == 2):
                a_dict["页数"] = pages[1]
        elif "出版年" in str(aList[i]):
            year = str(aList[i]).split(":")
            if (len(year) == 2):
                a_dict["出版年"] = year[1]
        elif "装帧" in str(aList[i]):
            zhuang = str(aList[i]).split(":")
            if (len(zhuang) == 2):
                a_dict["装帧"] = zhuang[1]

    return a_dict


def movieinfo_to_dict(a_html):
    a_dict = dict()
    a_list = []
    soup = BeautifulSoup(a_html)

    #     print(soup.get_text())

    aList = soup.get_text().split("\n")
    for i in range(len(aList)):
        if "导演" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_dict["导演"] = item[1]
        elif "编剧" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_dict["编剧"] = item[1]
        elif "类型" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_list = item[1].split("/")
                a_dict["类型"] = a_list
        elif "制片国家/地区" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_dict["制片国家/地区"] = item[1]
        elif "语言" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_list = item[1].split("/")
                a_dict["语言"] = a_list
        elif "主演" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_list = item[1].split("/")
                a_dict["主演"] = a_list
        elif "上映日期" in str(aList[i]):
            item = str(aList[i]).split(":")
            if (len(item) == 2):
                a_dict["上映日期"] = item[1]

    return a_dict
def movietag_to_list(a_str):
    a_str = a_str.replace('\n', ',')
    a_str = a_str.split(',')
    re_list = []
    for i in range(len(a_str)):
        if a_str[i].strip() !=None:
            re_list.append(a_str[i].strip())
    return re_list
def grouptag_to_list(a_str):
    a_str = a_str.replace('\n', ',')
    a_str = a_str.split(',')
    re_list = []
    for i in range(len(a_str)):
        if a_str[i].strip() !=None:
            re_list.append(a_str[i].strip())
    return re_list
# 读入数据
df = pd.read_csv("../dataset/douban_data.csv")
my_df = df

# 删除一些无用的列数据
my_df = my_df.drop(['web-scraper-order', 'web-scraper-start-url', 'link',
                    'link-href', 'movielink', 'movielink-href', ], axis=1)
my_df.drop(['booklink', 'booklink-href'], axis=1)

# 将数据分为三部分，分别为书籍，电影，以及小组数据


#####################################书籍的数据处理#############################################
# 首先形成书籍的数据
douban_book = pd.DataFrame(my_df, columns=['name', 'bookname', 'bookdetail','bookrage', 'booktag'])
douban_book = douban_book.dropna(thresh=3)
# 对tag 标签进行清洗

douban_book['booktag'] = douban_book.apply(lambda row: tag_to_list(str(row['booktag'])), axis=1)

# douban_book['booktag'] = douban_book.apply(lambda row: str(row['booktag']).replace('\n', ''), axis=1)

# 然后解析bookdetail中的数据，将其包装成一个dict格式的数据
# 包括作者，出版社，出版年，定价，ISBN数据

douban_book['bookdetail'] = douban_book.apply(lambda row: detail_to_dict(str(row['bookdetail'])), axis=1)

#将书籍数据分为两部分
###第一部分是书籍的详细信息
douban_book_detail = pd.DataFrame(douban_book, columns=['bookname', 'bookdetail', 'bookrage', 'booktag'])
###第二部分是用户的读书信息
user_book = pd.DataFrame(douban_book, columns=['name', 'bookname', 'booktag'])

douban_book_detail.to_csv("../dataset/douban_book_detail.csv",encoding = "utf-8")
user_book.to_csv("../dataset/user_book.csv" , encoding = "utf-8")
############################################################################################
# 形成电影的数据
douban_movie = pd.DataFrame(my_df, columns=['name', 'movienames', 'movieinfo',
                                            'movietag', 'movierate'])
douban_movie = douban_movie.dropna(thresh=3)

douban_movie['movieinfo'] = douban_movie.apply(lambda row: movieinfo_to_dict(str(row['movieinfo'])), axis=1)
douban_movie['movietag'] = douban_movie.apply(lambda row: movietag_to_list(str(row['movietag'])), axis=1)


douban_movie_detail = pd.DataFrame(douban_movie, columns=['movienames', 'movieinfo', 'movietag', 'movierate'])
user_movie = pd.DataFrame(douban_movie, columns=['name', 'movienames'])

douban_movie_detail.to_csv("../dataset/douban_movie_detail.csv",encoding = "utf-8")
user_movie.to_csv("../dataset/user_movie.csv" , encoding = "utf-8")
#####################################################################################
# 最后形成小组的数据

douban_group = pd.DataFrame(my_df, columns=['name', 'g_name', 'g_tag'])
douban_group = douban_group.dropna(thresh=2)

douban_group['g_tag'] = douban_group.apply(lambda row: grouptag_to_list(str(row['g_tag'])), axis=1)

douban_group.to_csv("../dataset/douban_group.csv" , encoding = "utf-8")#columns=None

#################################################################################