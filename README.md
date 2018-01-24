# xinxixitong

__信息系统大作业__

+ 数据准备,使用爬虫插件web scrapy ,从豆瓣上爬取了用户的电影，读书，以及加入小组的信息, 建立了数据库，数据库中有五张表，下面分别是五张表的字段解释

+ MOVIE_DETAIL 这张表记录的是电影信息 

  |movie_id|movie_name|movie_rate|movie_detail|movie_tag|
  |-----|-----|----|------|-------|
  |电影的id|电影的名字|电影的评分|电影的细节信息|电影的标签信息|

+ BOOK_DETAIL 这张表记录的是书籍信息 

  |book_id|book_name|book_rate|book_detail|book_tag|
  |-----|-----|----|------|-------|
  |书籍的id|书籍的名字|书籍的评分|书籍的细节信息|书籍的标签信息|

+ USER_GROUP 这个是用户参加豆瓣小组信息

  |gu_id|userid|name|g_name|g_tag|
  |-----|------|-----|------|------|
  |主键无实质含义|用户的id|用户的名字|小组的评分|小组的标签信息|
  
+ USER_BOOK 这个是用户读书信息

  |eventid|name|userid|bookid|
  |-----|-----|----|------|
  |主键无实质含义|用户的名字|用户的id|书籍的id|
  
+ USER_MOVIE 这个是用户看电影信息

  |um_id|name|userid|movieid|
  |-----|-----|----|------|
  |主键无实质含义|用户的名字|用户的id|电影的id|

+ User_Attention 这张表里面记录的是用户之间相互关注的信息

  |name|attention_ids|userid|
  |-----|-----|----|
  |用户的姓名|该用户关注的用户id|该用户的id|
  
+ 框架选取的是Falsk，数据库是采用sqlite,数据库名称是.db
+ 使用的IDE是pycharm
+ 运行方法，构建项目，安装环境依赖，点击run.py中的main函数就可以运行
