# --*-- coding:utf-8 --*--
"""
责任链模式
开发一个应用时，多数时候我们都能预先知道哪个方法能处理某个特定请求。然而，情况并非总是如此

责任链（Chain of Responsibility）模式
    用于让多个对象来处理单个请求时，或者用于预先不知道应该由哪个对象（来自某个对象链）来处理某个特定请求时。
其原则如下所示：
1: 存在一个对象链（链表、树或任何其他便捷的数据结构）
2: 我们一开始将请求发送给链中的第一个对象
3: 对象决定其是否要处理该请求
4: 对象将请求转发给下一个对象
5: 重复该过程，直到到达链尾
"""
"""
例子：
java 的 servlet 过滤器是在一个 HTTP 请求到达目标处理程序之前执行的一些代码片段。
在使用 servlet 过滤器时，有一个过滤器链，其中每个过滤器执行一个不同动作（用户身份验证、记日志、数据压缩等），
并且将请求转发给下一个过滤器直到链结束；如果发生错误（例如，连续三次身份验证失败）则跳出处理流程。
"""
"""
应用场景
通过使用责任链模式，我们能让许多不同对象来处理一个特定请求。在我们预先不知道应该由哪个对象来处理某个请求时，这是有用的
另一个责任链可以派上用场的场景是，在我们知道可能会有多个对象都需要对同一个请求进行处理之时。这在基于事件的编程中是常有的事情。
如果所有请求都能被单个处理程序处理，责任链就没那么有用了，除非确实不知道会是哪个程序处理请求
这一模式的价值在于解耦。客户端与所有处理程序（一个处理程序与所有其他处理程序之间也是如此）之间不再是多对多关系，
    客户端仅需要知道如何与链的起始节点（标头）进行通信。
"""
"""
使用 Python 实现责任链模式有许多种方式
Python 风格使用动态分发来处理请求。
参考实现一个简单的事件系统：
"""
# demo
class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

# 核心类
class Widget:
    # 注意parent=None 表明默认的集成关系为空
    def __init__(self, parent=None):
        self.parent = parent

    # Widget 与 Event 仅是关联关系，表明Widget类知道Event类，单对其没有严格的引用，只需要作为参数传递即可
    def handle(self, event):
        handler = 'handle_{}'.format(event)
        if hasattr(self, handler):
            method = getattr(self, handler)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, 'handle_default'):
            self.handle_default(event)

# 具有不同行为的控件 1
class MainWindow(Widget):
    def handle_close(self, event):
        print('MainWindow: {}'.format(event))

    def handle_default(self, event):
        print('MainWindow Dafault: {}'.format(event))

# 具有不同行为的控件 2
class SendDialog(Widget):
    def handle_paint(self, event):
        print('MainWindow Default: {}'.format(event))

# 具有不同行为的控件 3
class MsgText(Widget):
    def handle_down(self, event):
        print('MsgText: {}'.format(event))

def main():
    mw = MainWindow()
    sd = SendDialog(mw)
    msg = MsgText(sd)

    for e in ('down', 'paint', 'unhandled', 'close'):
        evt = Event(e)
        # print('\nSending event -{}- to MainWindow'.format(evt))
        # mw.handle(evt)
        # print('Sending event -{}- to SendDialog'.format(evt))
        sd.handle(evt)
        # print('Sending event -{}- to MsgText'.format(evt))
        # msg.handle(evt)

if __name__ == '__main__':
    main()



