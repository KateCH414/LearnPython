# --*-- coding:utf-8 --*--
# Python的内建模块itertools提供了非常有用的用于操作迭代对象的函数。
import itertools

if __name__ == '__main__':
    # count()
    # 会创建一个无限的迭代器
    natuals = itertools.count(1)
    for n in natuals:
        print(n)
        # 上述代码会打印出自然数序列，根本停不下来，只能按Ctrl+C退出
        if n > 20:
            break

    # cycle()
    # 会把传入的一个序列无限重复下去
    cs = itertools.cycle('ABC')
    for c in cs:
        print(c)
        # 会打印'A'，'B'， 'C' 循环，同样停不下来
        if c == 'C':
            break

    # repeat()
    # 负责把一个元素无限重复下去，不过如果提供第二个参数就可以限定重复次数：
    rs = itertools.repeat('A', 4)
    for r in rs:
        print(r)

    # 无限序列只有在for迭代时才会无限地迭代下去，如果只是创建了一个迭代对象，它不会事先把无限个元素生成出来，
    # 事实上也不可能在内存中创建无限多个元素。

    # takewhile()
    # 无限序列虽然可以无限迭代下去，但是通常我们会通过takewhile()等函数根据条件判断来截取出一个有限的序列
    natuals2 = itertools.count(1)
    ns = itertools.takewhile(lambda x: x < 10, natuals2)
    print(list(ns))

    # chain()
    # 可以把一组迭代对象串联起来，形成一个更大的迭代器：
    for n in itertools.chain('ABC','XYZ'):
        print(n)

    # groupby()
    # 把迭代器中相邻的重复元素挑出来放在一起：
    for key, group in itertools.groupby('aaaaabbbbbaaaacccccddd'):
        print(key, list(group))
        # a ['a', 'a', 'a', 'a', 'a']
        # b ['b', 'b', 'b', 'b', 'b']
        # a ['a', 'a', 'a', 'a']
        # c ['c', 'c', 'c', 'c', 'c']
        # d ['d', 'd', 'd']

    # 挑选规则是通过函数完成的，只要作用于函数的两个元素返回的值相等，这两个元素就被认为是在一组的
    # 而函数返回值作为组的key。如果我们要忽略大小写分组，就可以让元素'A'和'a'都返回相同的key：
    for key, group in itertools.groupby('AAaabbBBSSSs', lambda c: c.upper()):
        print(key, list(group))
        # A ['A', 'A', 'a', 'a']
        # B ['b', 'b', 'B', 'B']
        # S ['S', 'S', 'S', 's']

    # 计算圆周率可以根据公式: pai/4 = 1- 1/3+ 1/5- 1/7+..

    def pi(N):
        ' 计算pi的值 '
        # step 1: 创建一个奇数序列: 1, 3, 5, 7, 9, ...
        # step 2: 取该序列的前N项: 1, 3, 5, 7, 9, ..., 2*N-1.
        # step 3: 添加正负符号并用4除: 4/1, -4/3, 4/5, -4/7, 4/9, ...
        # step 4: 求和:
        a = 1
        s = 0
        for i in itertools.count(1):
            if i % 2 == 1:
                s = s+(4/i)*a
                a = -a
            if i >= 2*N:
                break
        return s


    # 测试:
    print(pi(10))
    print(pi(100))
    print(pi(1000))
    print(pi(10000))
    assert 3.04 < pi(10) < 3.05
    assert 3.13 < pi(100) < 3.14
    assert 3.140 < pi(1000) < 3.141
    assert 3.1414 < pi(10000) < 3.1415
    print('ok')






