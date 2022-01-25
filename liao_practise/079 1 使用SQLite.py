# --*-- coding:utf-8 --*--
# 数据库类别
# 付费的商用数据库：
# Oracle，典型的高富帅；
# SQL Server，微软自家产品，Windows定制专款；
# DB2，IBM的产品，听起来挺高端；
# Sybase，曾经跟微软是好基友，后来关系破裂，现在家境惨淡。
# 免费的开源数据库
# MySQL，大家都在用，一般错不了；
# PostgreSQL，学术气息有点重，其实挺不错，但知名度没有MySQL高；
# sqlite，嵌入式数据库，适合桌面和移动应用。

# SQLite是一种嵌入式数据库，它的数据库就是一个文件。由于SQLite本身是C写的，而且体积很小，所以，经常被集成到各种应用程序中，甚至在iOS和Android的App中都可以集成
# Python就内置了SQLite3，所以，在Python中使用SQLite，不需要安装任何东西，直接使用

# 要操作关系数据库，首先需要连接到数据库，一个数据库连接称为Connection；
# 连接到数据库后，需要打开游标，称之为Cursor，通过Cursor执行SQL语句，然后，获得执行结果。
# Python定义了一套操作数据库的API接口，任何数据库要连接到Python，只需要提供符合Python标准的数据库驱动即可。
# 由于SQLite的驱动内置在Python标准库中，所以我们可以直接来操作SQLite数据库。
# 我们在Python交互式命令行实践一下：
import os
import sqlite3
# 连接到SQLite数据库
# 数据库文件是test.db
# 如果数据库文件不存在，会自动在当前目录创建
db_file = os.path.join(os.path.dirname(__file__), 'test1.db')
if os.path.isfile(db_file):
    os.remove(db_file)
conn = sqlite3.connect(db_file)
# 创建一个Cursor
cursor = conn.cursor()
# 执行一条SQL语句，创建user表
cursor.execute('create table user (id varchar(20) primary key, name varchar(20)) ')
# 插入一条记录
cursor.execute('insert into user (id, name) values(\'1\', \'michael\')')
# 通过rowcount获得插入的行数:
print(cursor.rowcount)

# 关闭 cursor
cursor.close()
# 提交事物
conn.commit()
# 关闭connection
conn.close()

# 查询记录
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
# 执行查询语句
cursor.execute('select * from user where id=?', ('1',))
# 获取查询结果
values = cursor.fetchall()
print(values)  # [('1', 'michael')]
cursor.close()
conn.close()

# Connection和Cursor对象，打开后一定记得关闭，就可以放心地使用
# 使用Cursor对象执行insert，update，delete语句时，执行结果由rowcount返回影响的行数，就可以拿到执行结果。
# 使用Cursor对象执行select语句时，通过fetchall()可以拿到结果集。结果集是一个list，每个元素都是一个tuple，对应一行记录。
# 如果SQL语句带有参数，那么需要把参数按照位置传递给execute()方法，有几个?占位符就必须对应几个参数
# cursor.execute('select * from user where name=? and pwd=?', ('abc', 'password'))

# 练习
# 请编写函数，在Sqlite中根据分数段查找指定的名字：
db_file = os.path.join(os.path.dirname(__file__), 'test2.db')
if os.path.isfile(db_file):
    os.remove(db_file)
# 初始数据
conn = sqlite3.connect(db_file)
cursor = conn.cursor()
cursor.execute('create table user(id varchar(20) primary key, name varchar(20), score int)')
cursor.execute(r"insert into user values ('A-001', 'Adam', 95)")
cursor.execute(r"insert into user values ('A-002', 'Bart', 62)")
cursor.execute(r"insert into user values ('A-003', 'Lisa', 78)")
print(cursor.rowcount)
cursor.close()
conn.commit()
conn.close()


def get_score_in(low, high):
    # ' 返回指定分数区间的名字，按分数从低到高排序 '
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    cursor.execute('select name from user where score > ? and score<= ? ORDER BY score', (low, high))
    values = cursor.fetchall()
    cursor.close()
    conn.close()
    resp = []
    for name in values:
        resp.append(name[0])
    print(resp)
    return resp

# 测试:
assert get_score_in(80, 95) == ['Adam'], get_score_in(80, 95)
assert get_score_in(60, 80) == ['Bart', 'Lisa'], get_score_in(60, 80)
assert get_score_in(60, 100) == ['Bart', 'Lisa', 'Adam'], get_score_in(60, 100)
print('Pass')


