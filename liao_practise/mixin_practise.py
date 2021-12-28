# --*-- coding:utf-8 --*--

# 继承是面向对象编程的一个重要的方式，因为通过继承，子类就可以扩展父类的功能。
# 多种特征分类，一直继承下去，类的数量会呈指数增长，很明显这样设计是不行的，正确的做法是采用多重继承
# 通过多重继承，一个子类就可以同时获得多个父类的所有功能。
# 多继承 如果多个类有共同得方法名,会调用第一顺位继承父类的方法

from socketserver import  TCPServer,ForkingMixIn,UDPServer,ThreadingMixIn

# 首先，主要的类层次仍按照哺乳类和鸟类设计：
class Animal(object):
    pass

# 大类:
class Mammal(Animal):
    pass

class Bird(Animal):
    pass

# 各种动物:
# class Dog(Mammal):
#     pass
#
# class Bat(Mammal):
#     pass

class Parrot(Bird):
    pass

class Ostrich(Bird):
    pass
# 现在，我们要给动物再加上Runnable和Flyable的功能，只需要先定义好Runnable和Flyable的类：
class Runnable(object):
    def run(self):
        print('Running...')

class Flyable(object):
    def fly(self):
        print('Flying...')

# 需要Runnable功能的动物，就多继承一个Runnable，例如Dog
class Dog(Mammal, Runnable):
    pass

# 对于需要Flyable功能的动物，就多继承一个Flyable，例如Bat
class Bat(Mammal, Flyable):
    pass

# MixIn
# 在设计类的继承关系时，通常，主线都是单一继承下来的，例如，Ostrich继承自Bird。
# 但是，如果需要“混入”额外的功能，通过多重继承就可以实现，比如，让Ostrich除了继承自Bird外，再同时继承Runnable。这种设计通常称之为MixIn。
# 为了更好地看出继承关系，我们把Runnable和Flyable改为RunnableMixIn和FlyableMixIn。
# 类似的，你还可以定义出肉食动物CarnivorousMixIn和植食动物HerbivoresMixIn，让某个动物同时拥有好几个MixIn

class RunnableMixIn(object):
    pass

class CarnivorousMixIn(object):
    pass

class Dog(Mammal, RunnableMixIn, CarnivorousMixIn):
    pass

# Python自带的很多库也使用了MixIn
# 举个例子，Python自带了TCPServer和UDPServer这两类网络服务，而要同时服务多个用户就必须使用多进程或多线程模型，
# 这两种模型由ForkingMixIn和ThreadingMixIn提供。通过组合，我们就可以创造出合适的服务来

# 编写一个多进程模式的TCP服务，定义如下：
class MyTCPServer(TCPServer, ForkingMixIn):
    pass

# 编写一个多线程模式的UDP服务，定义如下：

class MyUDPServer(UDPServer, ThreadingMixIn):
    pass
if __name__ == '__main__':
    pass