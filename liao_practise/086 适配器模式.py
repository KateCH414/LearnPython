# --*-- coding:utf-8 --*--
"""
结构设计模式
处理一个系统中不同实体（比如，类和对象）之间的关系
关注的是提供一种简单的对象组合方式来创造新功能。
"""
"""
适配器模式（Adapter pattern）
是一种结构型设计模式，帮助我们实现两个不兼容接口之间的兼容
解释一下不兼容接口的真正含义。如果我们希望把一个老组件用于一个新系统中， 或者把一个新组件用于一个老系统中，
不对代码进行任何修改两者就能够通信的情况很少见。但又并非总是能修改代码。
可以编写一个额外的代码层，该代码层包含让两个接口之间能够通信需要进行的所有修改。这个代码层就叫适配器。
"""
"""
应用案例
修改一个老旧组件的实现以满足我们的需求，不仅是不切实际的，而且也违反了开放/封闭原则。
开放/封闭原则（open/close principle）是面向对象设计的基本原则之一（SOLID中的O），
声明一个软件实体应该对扩展是开放的，对修改则是封闭的。
本质上这意味着我们应该无需修改一个软件实体的源代码就能扩展其行为。
适配器模式遵从开放/封闭原则。
"""


# demo
# 旧的产品类
class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} computer'.format(self.name)

    def execute(self):
        return 'executes a program'


# 适配器
class Adapter:
    def __init__(self, obj, adapted_methods):
        self.obj = obj
        # 通过内部字典实现适配
        self.__dict__.update(adapted_methods)

    def __str__(self):
        return str(self.obj)


# 待适配的类 1
class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'the {} synthesizer'.format(self.name)

    # 需要与 execute 适配的方法
    def play(self):
        return 'is playing an electronic song'


# 待适配的类 2
class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '{} the human'.format(self.name)

    # 需要与 execute 适配的方法
    def speak(self):
        return 'says hello'


def main():
    objects = [Computer('A')]
    synth = Synthesizer('m')
    # 要适配的是 execute 方法，于是直接通过内部字典替换
    objects.append(Adapter(synth, dict(execute=synth.play)))
    human = Human('b')
    objects.append(Adapter(human, dict(execute=human.speak)))

    for i in objects:
        print('{} {}'.format(str(i), i.execute()))


if __name__ == "__main__":
    main()
"""
虽然在 Python 中我们可以沿袭传统方式使用子类（继承）来实现适配器模式，
但使用内部字典这个技术是一种很棒的替代方案
"""







