#-*- codeing = utf-8 -*-
#@Time:2022/2/27 17:28
#@Author:张佳源
#@File:testSqlite.py
#@Sofeware:PyCharm


import sqlite3


#创建数据表

# conn = sqlite3.connect("test.db")   #打开或创建数据库文件
#
# print("成功打开数据库")
# c = conn.cursor()
#
# sql = '''
#     create table company
#         (id int primary key not null,
#         name text not null,
#         age int not null,
#         address char(50),
#         salary real );
# '''
#
# c.execute(sql)      #执行sql语句
# conn.commit()       #提交数据库操作
# conn.close()         #关闭数据库链接
#
# print("成功建表")



#插入数据

# conn = sqlite3.connect("test.db")   #打开或创建数据库文件
#
# print("成功打开数据库")
# c = conn.cursor()
#
# sql1 = '''
#     insert into company(id,name,age,address,salary)
#     values (1,'张三',32,'成都',8000);
# '''
#
# sql2 = '''
#     insert into company(id,name,age,address,salary)
#     values (2,'李四',30,'重庆',15000);
# '''
#
# c.execute(sql1)      #执行sql语句
# c.execute(sql2)
# conn.commit()       #提交数据库操作
# conn.close()         #关闭数据库链接
#
# print("插入数据完毕")

#查询数据

conn = sqlite3.connect("test.db")   #打开或创建数据库文件

print("成功打开数据库")
c = conn.cursor()

sql = "select * from company"

cursor = c.execute(sql)      #执行sql语句
for row in cursor:
    print("id = ",row[0])
    print("name = ", row[1])
    print("age = ", row[2])
    print("address = ", row[3])
    print("salary = ", row[4])

conn.close()         #关闭数据库链接

print("查询完毕")