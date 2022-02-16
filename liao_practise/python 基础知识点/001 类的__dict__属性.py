# --*-- coding:utf-8 --*--
"""
首先看一下类的__dict__属性和类对象的__dict__属性
"""


class A(object):
    """
    class A
    """
    a = 0
    b = 1

    def __init__(self):
        self.a = 2
        self.b = 3

    def test(self):
        print('a normal func')

    @staticmethod
    def static_test(self):
        print('a static func')

    @classmethod
    def class_test(self):
        print('a calss func')


a = A()
print(A.__dict__)
# {'__module__': '__main__', '__doc__': '\n    class A\n    ', 'a': 0, 'b': 1, '__init__': <function A.__init__ at 0x7fe7b803cb00>, 'test': <function A.test at 0x7fe7b803cb90>, 'static_test': <staticmethod object at 0x7fe7b8048490>, 'class_test': <classmethod object at 0x7fe7b80484d0>, '__dict__': <attribute '__dict__' of 'A' objects>, '__weakref__': <attribute '__weakref__' of 'A' objects>}
print(a.__dict__)
# {'a': 2, 'b': 3}

"""
类__dict__: 包含了类的静态函数、类函数、普通函数、全局变量以及一些内置的属性
对象的__dict__：存储了一些self.xxx的一些东西
"""
"""
Python里什么没有__dict__属性
虽然说一切皆对象，但对象也有不同，一些内置的数据类型是没有__dict__属性的
    int, list, dict等这些常用的数据类型是没有__dict__属性的，
    就算给了它们dict属性也没啥用，毕竟它们只是用来做数据容器的。
"""
num = 3
ll = []
dd = {}
try:
    print(num.__dict__)  # 'int' object has no attribute '__dict__'
    print(ll.__dict__)
    print(dd.__dict__)
except AttributeError as e:
    print(e)

"""
发生继承时候的__dict__属性
子类有自己的__dict__, 父类也有自己的__dict__,
子类的全局变量和函数放在子类的dict中，父类的放在父类dict中
"""


class Parent(object):
    a = 0
    b = 1

    def __init__(self):
      self.a = 2
      self.b = 3

    def p_test(self):
        pass


class Child(Parent):
    a = 4
    b = 5
    c = 6

    def __init__(self):
        super(Child, self).__init__()
        self.c = 7

    def c_test(self):
        pass

    def p_test(self):
        pass


p = Parent()
c = Child()
print(Parent.__dict__)
# {'__module__': '__main__', 'a': 0, 'b': 1, '__init__': <function Parent.__init__ at 0x7f906003b170>, 'p_test': <function Parent.p_test at 0x7f906003b200>, '__dict__': <attribute '__dict__' of 'Parent' objects>, '__weakref__': <attribute '__weakref__' of 'Parent' objects>, '__doc__': None}
print(Child.__dict__)
# {'__module__': '__main__', 'a': 4, 'b': 5, 'c': 6, '__init__': <function Child.__init__ at 0x7f906003b290>, 'c_test': <function Child.c_test at 0x7f906003b320>, 'p_test': <function Child.p_test at 0x7f906003b3b0>, '__doc__': None}
print(p.__dict__)
# {'a': 2, 'b': 3}
print(c.__dict__)
# {'a': 2, 'b': 3, 'c': 7}
"""
每个类的类变量、函数名都放在自己的__dict__中
实力变量的__dict__中，父类和子类对象的__dict__是公用的
"""
"""
总结：
内置的数据类型没有__dict__属性
每个类有自己的__dict__属性，就算存着继承关系，父类的__dict__ 并不会影响子类的__dict__
对象也有自己的__dict__属性， 存储self.xxx 信息，父子类对象公用__dict__
"""
















