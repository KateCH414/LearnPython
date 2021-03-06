# --*-- coding:utf-8 --*--
"""
观察着模式
我们希望在一个对象的状态改变时更新另外一组对象
在 MVC 模式中有这样一个非常常见的例子，假设在两个视图
（例如，一个饼图和一个电子表格）中使用同一个模型的数据，无论何时更改了模型， 都需要更新两个视图
就是观察者设计模式要处理的问题。

观察者模式描述单个对象（发布者，又称为主持者或可观察者）
与一个或多个对象（订阅者，又称为观察者）之间的发布—订阅关系
在 MVC 例子中，发布者是模型，订阅者是视图
MVC 并非是仅有的发布—订阅例子。信息聚合订阅（比如，RSS 或 Atom）是另一种例子。
许多读者通常会使用一个信息聚合阅读器订阅信息流，每当增加一条新信息时，他们就能自动地获取到更新。

观察者模式背后的思想等同于 MVC 和关注点分离原则背后的思想
即降低发布者与订阅者之间的耦合度，从而易于在运行时添加/删除订阅者
发布者不关心它的订阅者是谁。它只是将通知发送给所有订阅者。
"""
"""
应用场景
当我们希望在一个对象（主持者/发布者/可观察者）发生变化时通知/更新另一个或多个对象的时候，
通常会使用观察者模式。观察者的数量以及谁是观察者可能会有所不同，也可以（在运行时）动态地改变。

事件驱动系统是另一个可以使用（通常也会使用）观察者模式的例子。
在这种系统中，监听者被用于监听特定事件。监听者正在监听的事件被创建出来时，就会触发它们。这个事件可以是键入（键盘的）某个特定键、移动鼠标或者其他。事件扮演发布者的角色，监听者则扮演观察者的角色。在这里，关键点是单个事件（发布者）可以关联多个监听者（观察者）。
"""
"""
demo
实现一个数据格式化程序。要求如下
默认格式化程序是以十进制格式展示一个数值,可以添加/注册更多的格式化程序
这个例子中将添加一个十六进制格式化程序和一个二进制格式化程序
每次更新默认格式化程序的值时，已注册的格式化程序就会收到通知，并采取行动
    在这里，行动就是以相关的格式展示新的值。
    
观察者模式使用继承能
我们可以实现一个基类 Publisher，包括添加、删除及通知观察者这些公用功能
DefaultFormatter 类继承自 Publisher，并添加格式化程序特定的功能
我们可以按需动态地添加删除观察者。
"""
# 发布者基类
class Publisher:
    def __init__(self):
        self.observers = []  # 观察者们

    # 通过该方法注册一个新的观察者
    def add(self, observer):
        if observer not in self.observers:
            self.observers.append(observer)
        else:
            print('Failed to add: {}'.format(observer))

    # 注销一个已有的观察者
    def remove(self, observer):
        try:
            self.observers.remove(observer)
        except ValueError:
            print('Failed to remove: {}'.format(observer))

    # 在变化发生时通知所有观察者
    def notify(self):
        [o.notify(self) for o in self.observers]

# 发布者具体实现
class DefaultFormatter(Publisher):
    def __init__(self, name):
        Publisher.__init__(self)
        self.name = name  # 设置其自己的名字，方便跟踪其状态
        self._data = 0  # 使用名称改编使其不能直接访问该变量

    # type(self).__name 是一种获取类名的方便技巧，避免硬编码类名
    def __str__(self):
        return "{}: '{}' has data = {}".format(type(self).__name__, self.name, self._data)

    # 提供 data 变量的读访问方式
    @property
    def data(self):
        return self._data

    # 使用了 @setter 修饰器，会在每次使用赋值操作符时被调用
    @data.setter
    def data(self, new_value):
        try:
            self._data = int(new_value)
        except ValueError as e:
            print('Error: {}'.format(e))
        else:
            self.notify()


# 观察者 1
class HexFormatter:
    # 通知方式有所不同
    def notify(self, publisher):
        print("{}: '{}' has now hex data = {}".format(type(self).__name__,
                                                      publisher.name, hex(publisher.data)))


# 观察者 2
class BinaryFormatter:
    # 通知方式有所不同
    def notify(self, publisher):
        print("{}: '{}' has now bin data = {}".format(type(self).__name__,
                                                      publisher.name, bin(publisher.data)))


def main():
    df = DefaultFormatter('test1')
    print(df)

    print("-------HexFormatter-----------")
    hf = HexFormatter()
    df.add(hf)  # 关联可用的观察者
    df.data = 3
    print(df)

    print("----BinaryFormatter------")
    bf = BinaryFormatter()
    df.add(bf)  # 关联可用的观察者
    df.data = 21
    print(df)

    print()
    df.remove(hf)
    df.data = 40
    print(df)

    print()
    df.data = 15.8
    print(df)


if __name__ == '__main__':
    main()

"""
总结
大体上，所有利用 MVC 模式的系统都是基于事件的。作为具体的例子，我们提到了以下两项：
django-observer，一个第三方 Django 库，用于注册在模型字段变更时执行的观察者。 
RabbitMQ 的 Python 绑定。我们介绍了一个 RabbitMQ 的具体例子，用于实现发布—订阅（即观察者）模式。
"""

