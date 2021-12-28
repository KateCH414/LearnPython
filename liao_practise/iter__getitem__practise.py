# --*-- coding:utf-8 --*--
# __iter__
# 如果一个类想被用于for ... in循环，类似list或tuple那样，就必须实现一个__iter__()方法，
# 该方法返回一个迭代对象，然后，Python的for循环就会不断调用该迭代对象的__next__()方法拿到循环的下一个值，直到遇到StopIteration错误时退出循环。
class Fib(object):
    def __init__(self):
        self.a ,self.b = 0, 1 # 初始化两个计数器a，b

    def __iter__(self):
        return  self # 实例本身就是迭代对象，故返回自己

    def __next__(self):
        self.a, self.b = self.b, self.a + self.b  # 计算下一个值
        if self.a > 100000:  # 退出循环的条件
            raise StopIteration()

        return self.a  # 返回下一个值

# __getitem__
# Fib实例虽然能作用于for循环，看起来和list有点像，但是，把它当成list来使用还是不行，比如，取第5个元素：
# 要表现得像list那样按照下标取出元素，需要实现__getitem__()方法：
class Fib1(object):
    def __getitem__(self, n):
        a, b = 1, 1
        for x in range(n):
            a, b = b, a + b
        return a

# 但是list有个神奇的切片方法：list(range(100))[5:10]
# 对于Fib却报错。原因是__getitem__()传入的参数可能是一个int，也可能是一个切片对象slice，所以要做判断：
class Fib3(object):
    def __getitem__(self, n):
        if isinstance(n, int): # n是索引
            a, b = 1, 1
            for x in range(n):
                a, b = b, a + b
            return a
        if isinstance(n, slice):  # n是切片
            start = n.start
            stop = n.stop
            if start is None:
                start = 0
            a, b = 1, 1
            L = []
            for x in range(stop):
                if x >= start:
                    L.append(a)
                a, b = b, a + b
            return L

# 如果把对象看成dict，__getitem__()的参数也可能是一个可以作key的object，例如str
# 与之对应的是__setitem__()方法，把对象视作list或dict来对集合赋值
# 还有一个__delitem__()方法，用于删除某个元素
# 总之，通过上面的方法，我们自己定义的类表现得和Python自带的list、tuple、dict没什么区别，这完全归功于动态语言的“鸭子类型”，不需要强制继承某个接口。

if __name__ == '__main__':
    # 现在，试试把Fib实例作用于for循环：

    for n in Fib():
        print(n)

    f = Fib1()
    print(f[100])

    f3 = Fib3()
    a = f3[4:10]
    print(a)

