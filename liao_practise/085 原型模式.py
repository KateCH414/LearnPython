# --*-- coding:utf-8 --*--
"""
复制一个副本被称为一个克隆，
是某个时间点原有对象的一个完全副本：时间是一个重要因素。因为它会影响克隆所包含的内容。
注意区分引用与副本
原型设计模式（Prototype design pattern）：帮助我们创建对象的克隆，其最简单的形式就是一个 clone() 函数，接受一个对象作为输入参数，返回输入对象的一个副本。
在 Python 中，这可以使用 copy.deepcopy() 函数来完成。
"""
"""
很多 Python 应用都使用了原型模式，但几乎都不称之为原型模式，因为对象克隆是编程语言的一个内置特性。
    可视化工具套件（Visualization Toolkit，VTK）是原型模式的一个应用。VTK 是一个开源的跨平台系统，用于三维计算机图形/图片处理以及可视化。
    使用原型模式的项目是 music21。根据该项目页面所述，“music21 是一组工具，帮助 学者和其他积极的听众快速简便地得到音乐相关问题的答案”
"""
"""
应用案例
1：已有一个对象，并希望创建该对象的一个完整副本时，原型模式就派上用场
2：当我们想复制一个复杂对象时，使用原型模式会很方便：对于复制复杂对象，我们可以将对象当作是从数据库中获取的，并引用其他一些也是从数据库中获取的对象。若通过多次重复查询数据来创建一个对象，则要做很多工作。在这种场景下使用原型模式要方便得多。
可以引入数据共享和写时复制一类的技术来优化性能（例如， 减小克隆对象的创建时间）和内存使用。如果可用资源有限（例如，嵌入式系统）或性能至关重要（例如，高性能计算），那么使用浅副本可能更佳。
"""
# demo: 书籍的一个例子
import copy
from collections import OrderedDict

# 产品类
class Book:
    def __init__(self, name, authors, price, **rest):
        """rest的例子有：出版商，长度，标签，出版日期"""
        self.name = name
        self.authors = authors
        self.price = price   # 单位为美元
        self.__dict__.update(rest)

    def __str__(self):
        mylist = []
        ordered = OrderedDict(sorted(self.__dict__.items()))
        for i in ordered.keys():
            mylist.append('{}:{}'.format(i, ordered[i]))
            if i == 'price':
                mylist.append('$')
            mylist.append('\n')

        return ''.join(mylist)


# 原型设计
class Prototype:
    def __init__(self):
        self.objects = dict()

    def register(self, identifier, obj):
        self.objects[identifier] = obj

    def unregister(self, identifier):
        del self.objects[identifier]

    # 通过 arrt 属性来控制改变的的变量
    def clone(self, identifier, **attr):
        found = self.objects.get(identifier)
        if not found:
            raise ValueError('Incorrect object identifier: {}'.format(identifier))
        obj = copy.deepcopy(found)
        obj.__dict__.update(attr)
        return obj


def main():
    b1 = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'), price=118,
              publisher='Prentice hall', length=228, publication_date='1978-02-22',
              tags=('c', 'programming', 'algorithms', 'data structures'))

    prototype = Prototype()
    cid = 'k&r-first'
    prototype.register(cid, b1)
    b2 = prototype.clone(cid, name='The C Programming Language(ANSI)', price=48.99,
                         length=274, publication_date='1988-04-01', edition=2)

    print(b1)
    """
    authors:('Brian W. Kernighan', 'Dennis M.Ritchie')
    length:228
    name:The C Programming Language
    price:118$
    publication_date:1978-02-22
    publisher:Prentice hall
    tags:('c', 'programming', 'algorithms', 'data structures')
    """

    print(b2)
    """
    authors:('Brian W. Kernighan', 'Dennis M.Ritchie')
    edition:2
    length:274
    name:The C Programming Language(ANSI)
    price:48.99$
    publication_date:1988-04-01
    publisher:Prentice hall
    tags:('c', 'programming', 'algorithms', 'data structures')
    
    """


if __name__ == '__main__':
    main()


"""
创建一个浅副本时，副本依赖引用
    这种情况中，我们关注提升应用性能和优化内存使用，在对象之间引入数据共享，但需要小心地修改数据，因为所有变更对所有副本都是可见的
当创建一个深副本时，副本复制所有东西
    这种情况中，我们希望能够对一个副本进行更改而不会影响其他对象
"""


