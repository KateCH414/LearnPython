# --*-- coding:utf-8 --*--
"""
set() 函数创建一个无序不重复元素集，可进行关系测试，删除重复数据，还可以计算交集、差集、并集等。

set 语法：
    class set([iterable])
参数：
    iterable -- 可迭代对象对象；
返回值
   返回新的集合对象。
"""
x = set('runoob')
# 重复的被删除
print(x)  # {'r', 'b', 'n', 'u', 'o'}


y = set('google')
print(y)  # {'e', 'g', 'l', 'o'}

print(x & y)  # 交集 {'o'}
print(x | y)  # 并集 {'r', 'e', 'b', 'n', 'l', 'g', 'u', 'o'}
print(x - y)  # 差集 {'u', 'n', 'b', 'r'}

