# --*-- coding:utf-8 --*--
"""
hasattr() 函数用于判断对象是否包含对应的属性。

hasattr 语法：
    hasattr(object, name)
参数
    object -- 对象
    name -- 字符串，属性名
返回值
    如果对象有该属性返回 True，否则返回 False。

实例 如下
"""
class Coordinate:
    x = 10
    y = -5
    z = 0

if __name__ == '__main__':
    c = Coordinate()
    print(hasattr(c, 'x'))
    print(hasattr(c, 'y'))
    print(hasattr(c, 'z'))
    print(hasattr(c, 'c'))

    # 输出
    # True
    # True
    # True
    # False






