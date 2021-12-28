# -*- coding: UTF-8 -*-

import sys
from tkinter import Button,mainloop
import  functools,time
import re


def triangles():
    a = [1]
    while True:
        yield a
        a = [sum(i) for i in zip([0]+a, a+[0])]


n = 0

def createCounter():
    def counter():
        global n
        n = n+1
        return n
    return counter

def createCounter1():
    s = [0]
    def counter():
        s[0] = s[0]+1
        return s[0]
    return counter


def log(text):
    def decorator(func):
        def wrapper(*args, **kw):
            print('%s %s():' % (text, func.__name__))
            return func(*args, **kw)
        return wrapper
    return decorator


def logA(func):
    def wrapper(*args, **kw):
        print('call %s():' % func.__name__)
        return func(*args, **kw)
    return wrapper


def metric(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kw):
        print('%s executed in %s ms' % (fn.__name__, time.localtime()))
        return fn(*args, **kw)
    return wrapper



@metric
def now():
    print('2015-3-25')


if __name__ == '__main__':

    # now()


    line = "frag_stage_one"

    matchObj = re.match(r'^frag_stage_', line)
    print(matchObj)

    # n = 0
    # try:
    #     for t in triangles():
    #         print(t)
    #         n = n+1
    #         if n > 10:
    #             break
    # except:
    #     print("over")

    # x = Button(text='Press me', command=(lambda: sys.stdout.write('Hello,World\n')))
    # x.pack()
    # x.mainloop()

    # counterA = createCounter()
    # print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
    #
    # c = createCounter1()
    # print(c(),c())
    #
    # c1 = createCounter1()
    # print(c1(),c1())
