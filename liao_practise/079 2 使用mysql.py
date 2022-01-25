# --*-- coding:utf-8 --*--
# MySQL是为服务器端设计的数据库，能承受高并发访问，同时占用的内存也远远大于SQLite。
# MySQL内部有多种数据库引擎，最常用的引擎是支持数据库事务的InnoDB。

# 在Mac或Linux上，需要编辑MySQL的配置文件，把数据库默认的编码全部改为UTF-8。MySQL的配置文件默认存放在/etc/my.cnf或者/etc/mysql/my.cnf
# [client]
# default-character-set = utf8
#
# [mysqld]
# default-storage-engine = INNODB
# character-set-server = utf8
# collation-server = utf8_general_ci
# 重启MySQL后，可以通过MySQL的客户端命令行检查编码：
# $ mysql -u root -p
# Enter password:
# Welcome to the MySQL monitor...
# ...
#
# mysql> show variables like '%char%';
# 注：如果MySQL的版本≥5.5.3，可以把编码设置为utf8mb4，utf8mb4和utf8完全兼容，但它支持最新的Unicode标准，可以显示emoji字符。

# 安装Mysql 驱动
# pip install mysql-connector-python --allow-external mysql-connector-python
# 或 pip install mysql-connector


# 如何连接到MySQL服务器的test数据库
import mysql.connector
conn = mysql.connector.connect(user='root', password='cuihuan', database='test')
cusor = conn.cursor()
# 创建user表
cusor.execute('create table user (id varchar(20) primary key , name varchar(20))')
# 插入一行记录，注意mysql的占位符是 %s:
cusor.execute('insert into user (id, name) value(%s, %s) ', ['1', 'Michael'])
print(cusor.rowcount)
# 提交事物
conn.commit()
cusor.close()
conn.close()

# 查询插入的数据
conn = mysql.connector.connect(user='root', password='cuihuan', database='test')
cusor = conn.cursor()
cusor.execute('select * from user where id = %s', ('1', ))
values = cusor.fetchall()
print(values)
cusor.close()
conn.close()

# Python的DB-API定义都是通用的，所以，操作MySQL的数据库代码和SQLite类似。
# 执行INSERT等操作后要调用commit()提交事务；
# MySQL的SQL占位符是%s。