# -*- coding:utf-8 -*-
# -*- coding: UTF-8 -*-

import types

class Animal(object):
    def run(self):
        print('Animal is running...')


class Dog(Animal):
    def run(self):
        print('dog is running...')


class Cat(Animal):
    def run(self):
        print('cat is running...')

if __name__ == '__main__':
    a = Animal()
    a.run()
    b = Dog()
    b.run()
    c = Cat()
    c.run()
    # type() 方法判断对象类型
    print(type(a)) # <class '__main__.Animal'>

    n1 = 123
    n2 = 456
    print(type(n1)==type(n2)) # Ture

    print(type(a.run)) # <class 'method'>

    def fn():
        print('fn ing...')

    print(type(fn)) # <class 'function'>

    #types() 模块中定义python数据类型常量
    print(type(fn) == types.FunctionType)
    print(type(abs)) # <class 'builtin_function_or_method'>
    print(type(abs) == types.BuiltinFunctionType)
    print(type(lambda x: x) == types.LambdaType)
    print(type((x for x in range(10)))==types.GeneratorType)
