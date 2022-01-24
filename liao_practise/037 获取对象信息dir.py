# -*- coding:utf-8 -*-

class Animal(object):
    a = 1
    def run(self):
        print('Animal is running...')


class Dog(Animal):
    def run(self):
        print('dog is running...')


class Cat(Animal):
    def run(self):
        print('cat is running...')

class MyObject(object):
     def __init__(self):
         self.x = 9
     def power(self):
         print('power ing')
         return self.x * self.x


if __name__ == '__main__':
    # 获得一个对象的所有属性和方法，可以使用dir()函数，它返回一个包含字符串的list
    print(dir(Animal())) # ['__class__', ....省略..., '__weakref__', 'a', 'run']

    #类似__xxx__的属性和方法在Python中都是有特殊用途的，
    #比如__len__方法返回长度。在Python中，如果你调用len()函数试图获取一个对象的长度，
    # 实际上，在len()函数内部，它自动去调用该对象的__len__()方法，所以，下面的代码是等价的：

    print('abc'.__len__()) # 3
    print(len('abc'))# 3

    # 仅仅把属性和方法列出来是不够的，配合getattr()、setattr()以及hasattr()，我们可以直接操作一个对象的状态：
    obj = MyObject()
    # 有属性'x'吗？
    print(hasattr(obj,'x'))# True
    print(obj.x)# 9
    # 有属性'y'吗？
    print(hasattr(obj,'y'))# false
    # 设置一个属性'y'
    setattr(obj,'y',19)
    print(hasattr(obj,'y'))# True
    # 获取属性'y'
    y = getattr(obj,'y')
    print(y)
    # 试图获取不存在的属性，会抛出AttributeError的错误
    #z = getattr(obj,'z') # 'MyObject' object has no attribute 'Z'

    # 也可以获得对象的方法：
    print(hasattr(obj, 'power')) # True
    # 获取属性'power'
    print(getattr(obj, 'power')) #<bound method MyObject.power of <__main__.MyObject object at 0x7fb74003c890>>
    # 获取属性'power'并赋值到变量fn
    fn = getattr(obj, 'power')
    # 调用fn()与调用obj.power()是一样的
    fn()










