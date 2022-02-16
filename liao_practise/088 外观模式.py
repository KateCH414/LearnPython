# --*-- coding:utf-8 --*--
"""
外观设计模式有助于隐藏 系统的内部复杂性
通过一个简化的接口向客户端暴露必要的部分。本质上，外观（Facade）是在已有复杂系统之上实现的一个抽象层。

使用场景：
使用外观模式的最常见理由是为一个复杂系统提供单个简单的入口点。
如果你的系统包含多层，外观模式也能派上用场。你可以为每一层引入一个外观入口点，并让所有层级通过它们的外观相互通信。这提高了层级之间的松耦合性，尽可能保持层级独立。
"""

"""
假设我们想使用多服务进程方式实现一个操作系统，类似于 MINIX 3或 GNU Hurd 那样
多服务进程的操作系统有一个极小的内核，称为微内核（microkernel）
它在特权模式下运行。系统的所有其他服务都遵从一种服务架构（驱动程序服务器、进程服务器、文件服务器等）
每个服务进程属于一个不同的内存地址空间，以用户模式在微内核之上运行。
这种方式的优势是操作系统更能容错、更加可靠、更加安全
例如，由于所有驱动程序都以用户模式在一个驱动服务进程之上运行，所以某个驱动程序中的一个 bug 并不能让整个系统崩溃，也无法影响到其他服务进程。
其劣势则是性能开销和系统编程的复杂性，因为服务进程和微内核之间，还有独立的服务进程之间，使用消息传递方式进行通信。 消息传递比宏内核（如 Linux）所使用的共享内存模型更加复杂。

用 abc 模块，请记住以下几个重要事项：
我们需要使用 metaclass 关键字来继承 ABCMeta。
使用 @abstractmethod 修饰器来声明 Server 的所有子类都应（强制性地）实现哪些方法。
"""
# demo
from enum import Enum
from abc import ABCMeta, abstractmethod

# 抽象基类，用#abstrcatclassmethod 修饰的 表示该方法强制要求子类失信
class Server(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self, restart=True):
        pass

# 需要隐藏的服务之一
class FileServer(Server):
    def __init__(self):
        pass

    def boot(self):
        pass

    def kill(self, restart=True):
        pass

    def create_file(self, user, name, permissions):
        pass

# 需要隐藏的服务之一
class ProcessServer(Server):
    def __init__(self):
        pass
    def boot(self):
        pass
    def kill(self, restart=True):
        pass
    def create_process(self, user, name):
        pass

# 外观实现，提供接口给外部
class OperatingSystem:
    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()

    def start(self):
        [i.boot() for i in (self.fs, self.ps)]

    def create_file(self, user, name, permissions):
        return  self.fs.create_file(user, name, permissions)

    def create_process(self, user, name):
        return self.ps.create_process(user, name)


def main():
    os = OperatingSystem()
    os.start()
    os.create_file('foo', 'hello', '-rw-r-r')
    os.create_process('bar', 'ls/tmp')


if __name__ == '__main__':
    main()


