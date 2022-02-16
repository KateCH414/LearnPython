# --*-- coding:utf-8 --*--
# Python中的协程大概经历了如下三个阶段：
# 1. 最初的生成器变形yield/send
# 2. 引入@asyncio.coroutine和yield from
# 3. 在最近的Python3.5版本中引入async/await关键字

# 生成器变形yield/send
# 普通函数如果出现yield 关键字，那么该函数就不再是普通函数，而是一个生成器
from random import randint


def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        yield alist.pop(c)


a = ['aa', 'bb', 'cc']
c = mygen(a)
print(c)
# 上面代码中 c 就是一个生成器，生成器是一种迭代器，可以使用for进行迭代
# 生成器的特点是可以接收外部传入的一个变量，并本根据变量内容极速三结果之后返回
# 这一且都是依靠生成器内部的send()函数实现的


def gen():
    value = 0
    while True:
        receive = yield value
        if receive == 'e':
            break
        value = 'got: %s' % receive


g = gen()
print(g.send(None))
print(g.send('hello'))
print(g.send(123456))
try:
    print(g.send('e'))
except Exception as e:
    print(e)

# 上面最关键也是最难理解的是 receive = yield value
# 其实receive=yield value包含了3个步骤：
# 1.向函数外抛出（返回）value
# 2.暂停（pause）,等待next()或是send()恢复
# 3.赋值receive=MockGetValue()，这个MockGetValue()是个假象函数，用来接收send()发送进来的值

# 执行流程
# 通过g.send(None)或者next(g)启动生成器函数，并执行到第一个yield语句结束的位置。
#   这里是关键，很多人就是在这里搞糊涂的。运行receive=yield value语句时，我们按照开始说的拆开来看，
#   实际程序只执行了1，2两步，程序返回了value值，并暂停(pause)，并没有执行第3步给receive赋值。因此yield value会输出初始值0。
#   这里要特别注意：在启动生成器函数时只能send(None),如果试图输入其它的值都会得到错误提示信息。
# 通过g.send('hello')，会传入hello，从上次暂停的位置继续执行，
#   那么就是运行第3步，赋值给receive。然后计算出value的值，
#   并回到while头部，遇到yield value，程序再次执行了1，2两步，程序返回了value值，并暂停(pause)。
#   此时yield value会输出”got: hello”，并等待send()激活。
# 通过g.send(123456)，会重复第2步，最后输出结果为”got: 123456″。
# 当我们g.send(‘e’)时，程序会执行break然后推出循环，最后整个函数执行完毕，所以会得到StopIteration异常。

# 在第一次send(None)启动生成器（执行1–>2，通常第一次返回的值没有什么用）
# 之后，对于外部的每一次send()，生成器的实际在循环中的运行顺序是3–>1–>2，也就是先获取值，然后dosomething，然后返回一个值，再暂停等待


# --------------------------
# yield from
def g1():
    yield range(5)


def g2():
    yield from range(5)


it1 = g1()
it2 = g2()
for x in it1:
    print(x)

for x in it2:
    print(x)

# 输出：
# range(0, 5)
# 0
# 1
# 2
# 3
# 4
# 说明yield 是将range这个可迭代对象直接返回了
# 而yield from解析了range对象，将其中每一个item返回了。
#   yield from iterable本质上等于for item in iterable: yield item的缩写版


# 例子
# 假设我们已经编写好一个斐波那契数列函数
def fab(max):
    n, a, b = 0, 0, 1
    while n < max:
        yield b
        a, b = b, a+b
        n = n + 1


# fab不是一个普通函数，而是一个生成器。因此fab(5)并没有执行函数，而是返回一个生成器对象(生成器一定是迭代器iterator，迭代器一定是可迭代对象iterable)
# 假设要在fab()的基础上实现一个函数，调用起始都要记录日志
def f_wrapper(fun_iterable):
    print('start')
    for item in fun_iterable:
        yield item
        print('end')


wrap = f_wrapper(fab(5))
for i in wrap:
    print(i, end='')


import logging


# 现在使用yield from代替for循环
def f_wrapper2(fun_iterable):
    print('start')
    yield from fun_iterable  # 注意此处必须是一个可生成对象
    print('end')


wrap2 = f_wrapper2(fab(5))
for i in wrap2:
    print(i, end='')

# 上面两种方式输出如下
# 第一种
# start
# 1end
# 1end
# 2end
# 3end
# 5end
# 第二种
# start
# 11235end

# ------------------------------
# asyncio.coroutine和yield from
# yield from在asyncio模块中得以发扬光大。
# 之前都是我们手工切换协程，现在当声明函数为协程后，我们通过事件循环来调度协程。
# 示例代码
import asyncio, random


@asyncio.coroutine
def smart_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.2)
        yield from asyncio.sleep(sleep_secs)  # 通常yield from后面都是接耗时操作
        print('smart one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a+b
        index += 1


@asyncio.coroutine
def stupid_fib(n):
    index = 0
    a = 0
    b = 1
    while index < n:
        sleep_secs = random.uniform(0, 0.4)
        yield from asyncio.sleep(sleep_secs)  # 通常yield from后面都是接耗时操作
        print('stupid one think {} secs to get {}'.format(sleep_secs, b))
        a, b = b, a + b
        index += 1


loop = asyncio.get_event_loop()
tasks = [smart_fib(10), stupid_fib(10)]
loop.run_until_complete(asyncio.wait(tasks))
print('all fib finished')
loop.close()

# yield from语法可以让我们方便地调用另一个generator。
# 本例中yield from后面接的asyncio.sleep()是一个coroutine(里面也用了yield from)，
# 所以线程不会等待asyncio.sleep()，而是直接中断并执行下一个消息循环。
# 当asyncio.sleep()返回时，线程就可以从yield from拿到返回值（此处是None），然后接着执行下一行语句。

# asyncio是一个基于事件循环的实现异步I/O的模块
# 通过yield from，我们可以将协程asyncio.sleep的控制权交给事件循环，然后挂起当前协程；
# 之后，由事件循环决定何时唤醒asyncio.sleep,接着向后执行代码。

# 协程之间的调度都是由事件循环决定。
# yield from asyncio.sleep(sleep_secs) 这里不能用time.sleep(1)因为time.sleep()返回的是None，
# 它不是iterable，还记得前面说的yield from后面必须跟iterable对象(可以是生成器，迭代器)。所以会报错：

# 一些概念
# 1.Event loop 事件循环复用 I/O，
#   利用 selectors 工作，序列化事件处理。 程序开启一个无限的循环，把一些函数注册到事件循环上。当满足事件发生的时候，调用相应的协程函数
# 2.coroutine 协程对象，
#   指一个使用async def 关键字定义的函数，它的调用不会立即执行函数，而是会返回一个协程对象。 协程不能直接运行, 需要把协程对象注册到事件循环，由事件循环调用。
# 3.Futures 这是那些延迟生产者的抽象
#   asyncio.Future 类与 Python3.2 中引入的 Future 类似。即，concurrent.futures.Future类。
#   但是，在这种情况下，Future 适用于协程。该 asyncio 模块不适用现有的concurrent.futures.Future类，
#   因为它被设计用于线程工作。 该模块鼓励在协程中使用 await 锁住当前的任务来等待结果，从而避免阻塞你的应用。
#   你的协程代码块；也就是说，你的协程被挂起，直到产生了结果，但是事件循环却没有被阻塞。
#   若同一个 event loop 还有其他的任务序列，他们可能会运行。 当协程产生结果的时候，暂停的协程会恢复，
#   你可以编写同顺序执行一样的代码。 你可以阅读代码，无需考虑 await 的存在。当你使用在函数中使用 await 返回一个 await 对象，
#   你可以忘记 Future 执行的特殊的细节和它特定的 API。 如果产生异常，比如你调用了函数，它没有返回 Future，却做了顺序执行，那么异常会被抛出。
#   所以，编写异步代码同编写同步代码一样，除了添加 await。
# 4.Tasks 每个 Task 是一个被 Future 包裹的协程
#   随着 event loop 的运行而运行。 asyncio.Task 类是 asyncio.Future 的子类。tasks 也与 await 一起工作。


# ----------------
# async 和 await

# 在Python3.5中引入的async和await就不难理解了：
#   可以将他们理解成asyncio.coroutine/yield from的完美替身。
# 从Python设计的角度来说，async/await让协程表面上独立于生成器而存在，
#   将细节都隐藏于asyncio模块之下，语法更清晰明了。

# 加入新的关键字 async ，可以将任何一个普通函数变成协程
import time, random


async def mygen(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        print(alist.pop(c))

a = ['aa', 'bb', 'cc']
c = mygen(a)
print(c)
# 输出： <coroutine object mygen at 0x02c6BED0>

# 在上面程序中，我们在前面加上async，该函数就变成一个协程了。
# 但是async对生成器是无效的。async无法将一个生成器转换成协程。
# 还是刚才那段代码，我们把print改成yield

async def mygen2(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        yield alist.pop(c)

a = ['aa', 'bb', 'cc']
c = mygen2(a)
print(c)
# 输出： <async_generator object mygen2 at 0x02c6BED0>
# 并不是协程对象
# 协程代码应该这样写
async def mygen3(alist):
    while len(alist) > 0:
        c = randint(0, len(alist)-1)
        print(alist.pop(c))
        await asyncio.sleep(1)

a = ['aa', 'bb', 'cc']
c = mygen3(a)
print(c)

# 要运行上述代码，需要使用时间循环
loop2 = asyncio.get_event_loop()
tasks = [c]
loop2.run_until_complete(asyncio.wait(tasks))
loop2.close()