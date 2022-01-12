# --*-- coding:utf-8 --*--
# collections是Python内建的一个集合模块，提供了许多有用的集合类。
#

if __name__ == '__main__':
    # namedtuple
    # 我们知道tuple可以表示不变集合，例如，一个点的二维坐标就可以表示成
    p = (1, 2)
    # 但是，看到(1, 2)，很难看出这个tuple是用来表示一个坐标的。
    # 这时，namedtuple就派上了用场：
    from collections import namedtuple
    Point = namedtuple("Point", ["x", "y"])
    p = Point(1, 2)
    print(p.x)  # 1
    print(p.y)  # 2
    # namedtuple是一个函数，它用来创建一个自定义的tuple对象，并且规定了tuple元素的个数，并可以用属性而不是索引来引用tuple的某个元素。
    # 用namedtuple可以很方便地定义一种数据类型，它具备tuple的不变性，又可以根据属性来引用，使用十分方便。
    # 验证创建的Point对象是tuple的一种子类
    isinstance(p, Point)  # true
    isinstance(p, tuple)  # true
    # 类似的，如果要用坐标和半径表示一个圆，也可以用namedtuple定义
    # namedtuple('名称', [属性list]):
    Circle = namedtuple('Circle', ['x', 'y', 'r'])

    # deque 双向链表
    # 使用list存储数据时，按索引访问元素很快，但是插入和删除元素就很慢了，因为list是线性存储，数据量大的时候，插入和删除效率很低。
    # deque是为了高效实现插入和删除操作的双向列表，适合用于队列和栈：
    from collections import deque
    q = deque(['a', 'b', 'c'])
    q.append('x')
    q.appendleft('y')
    q.remove('a')
    print(q)  # deque(['y', 'b', 'c', 'x'])
    a = q.pop()
    print(a)  # x
    print(q)  # deque(['y', 'b', 'c'])
    # deque除了实现list的append()和pop()外，还支持appendleft()和popleft()，这样就可以非常高效地往头部添加或删除元素。
    # deque的翻转和轮转
    q.reverse()
    print(q)  # deque(['c', 'b', 'y'])
    q.rotate(2)
    print(q)  # deque(['b', 'y', 'c'])

    # defaultdict
    # 使用dict时，如果引用的Key不存在，就会抛出KeyError。如果希望key不存在时，返回一个默认值，就可以用defaultdict：
    from collections import defaultdict
    # 默认值是调用函数返回的，在创建defaultdict对象时传入
    dd = defaultdict(lambda: 'N/A')
    dd['key1'] = 'abc'
    print(dd['key1'])  # key存在 'abc'
    print(dd['kay2'])  # key不存在 'N/A'

    # OrderedDict
    # 保持Key的顺序的dict，可以用OrderedDict
    from collections import OrderedDict
    d = dict([('a', 1), ('b', 2), ('c', 3)])
    print(d)  # {'a': 1, 'c': 3, 'b': 2}   dict的Key是无序的
    od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    print(od)  # OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    # 注意，OrderedDict的Key会按照插入的顺序排列，不是Key本身排序

    # OrderedDict可以实现一个FIFO（先进先出）的dict，当容量超出限制时，先删除最早添加的Key：
    class LastUpdatedOrderedDict(OrderedDict):

        def __init__(self, capacity):
            super(LastUpdatedOrderedDict, self).__init__()
            self._capacity = capacity  # 初始化时设置容量

        def __setitem__(self, key, value):
            containsKey = 1 if key in self else 0  # 判断插入的key 是否已经存在
            if len(self) - containsKey >= self._capacity:  # 插入新元素是否已经超容量
                last = self.popitem(last=False)  # 超容量移除最先插入的元素
                print('remove:', last)
            if containsKey:
                del self[key]
                print('set:', (key, value))  # key 相同时更新value
            else:
                print('add:', (key, value))  # 正常插入新元素
            OrderedDict.__setitem__(self, key, value)

    # ChainMap
    # ChainMap可以把一组dict串起来并组成一个逻辑上的dict。
    # ChainMap本身也是一个dict，但是查找的时候，会按照顺序在内部的dict依次查找。
    # 什么时候使用ChainMap最合适？
    #   举个例子：应用程序往往都需要传入参数，参数可以通过命令行传入，可以通过环境变量传入，还可以有默认参数。
    #   我们可以用ChainMap实现参数的优先级查找，即先查命令行参数，如果没有传入，再查环境变量，如果没有，就使用默认参数。
    import os, argparse
    from collections import ChainMap
    # 构造缺省参数
    # 如何查找user和color这两个参数
    defaults = {
        'color': 'red',
        'user': 'guest'
    }

    # 构造命令行参数:
    parser = argparse.ArgumentParser()
    parser.add_argument('-u', '--user')
    parser.add_argument('-c', '--color')
    namespace = parser.parse_args()
    command_line_args = {k: v for k, v in vars(namespace).items() if v}

    # 组合成ChainMap:
    combined = ChainMap(command_line_args, os.environ, defaults)

    # 打印参数:
    print('color=%s' % combined['color'])
    print('user=%s' % combined['user'])

    # Counter
    # Counter是一个简单的计数器，例如，统计字符出现的个数：
    from collections import Counter
    # 对列表作用
    list_01 = [1, 's', 3, 2, 1, 2, 'd', 's', 'sad']
    print(Counter(list_01))  # Counter({1: 2, 's': 2, 2: 2, 3: 1, 'd': 1, 'sad': 1})
    # 对字符串作用
    temp = Counter('hello,word')
    print(temp)  # Counter({'l': 2, 'o': 2, 'h': 1, 'e': 1, ',': 1, 'w': 1, 'r': 1, 'd': 1})
    # 对于其他可迭代序列也是一样的套路
    print(type(temp))  # <class 'collections.Counter'>
    # 转换为字典
    print(dict(temp))  # {'h': 1, 'e': 1, 'l': 2, 'o': 2, ',': 1, 'w': 1, 'r': 1, 'd': 1}
    # 用自带的items()方法 输出元素
    for item in temp.items():
        print(item)
    # 统计出现次数最多的前N元素
    print(temp.most_common(2))  # 出现次数最多的两个元素 [('l', 2), ('o', 2)]
    # 与 或 操作
    print(Counter('AAB') & Counter('BBCC'))  # Counter({'B': 1})
    print(Counter('BBCC') & Counter('AAB'))  # Counter({'B': 1})
    print(Counter('AAB') | Counter('BBCC'))  # Counter({'A': 2, 'B': 2, 'C': 2})











