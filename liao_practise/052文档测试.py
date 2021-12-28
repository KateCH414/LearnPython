# --*-- coding:utf-8 --*--

# Python的官方文档，可以看到很多文档都有示例代码
# re模块就带了很多示例代码： https://docs.python.org/3/library/re.html
# >>> import re
# >>> m = re.search('(?<=abc)def', 'abcdef')
# >>> m.group(0)
# 'def'

# 自动执行写在注释中的这些代码
# 当我们编写注释时，如果写上这样的注释：明确地告诉函数的调用者该函数的期望输入和输出
def abs(n):
    '''
    Function to get absolute value of number.

    Example:

    >>> abs(1)
    1
    >>> abs(-1)
    1
    >>> abs(0)
    0
    '''

    return n if n >= 0 else (-n)

# Python内置的“文档测试”（doctest）模块可以直接提取注释中的代码并执行测试
# doctest严格按照Python交互式命令行的输入和输出来判断测试结果是否正确。只有测试异常的时候，可以用...表示中间一大段烦人的输出。
class Dict(dict):
    '''
    Simple dict but also support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    '''
    def __init__(self, **kw):
        super(Dict, self).__init__(**kw)

    # 注释__getattr_会报错
    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

def fact(n):
    '''
    Calculate 1*2*...*n

    >>> fact(1)
    1
    >>> fact(10)
    3628800
    >>> fact(-1)
    Traceback (most recent call last):
        ...
    ValueError
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n - 1)

if __name__=='__main__':
    import doctest  # 当模块正常导入时，doctest不会被执行。只有在命令行直接运行时，才执行doctest。所以，不必担心doctest会在非测试环境下执行。
    doctest.testmod()

# 文档测试输出
# File "/Users/huancui/project/Python_ch/python_test/liao_practise/052文档测试.py", line 36, in __main__.Dict
# Failed example:
#     d1.x
# Exception raised:
#     Traceback (most recent call last):
#       File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/doctest.py", line 1337, in __run
#         compileflags, 1), test.globs)
#       File "<doctest __main__.Dict[2]>", line 1, in <module>
#         d1.x
#     AttributeError: 'Dict' object has no attribute 'x'
# **********************************************************************
# File "/Users/huancui/project/Python_ch/python_test/liao_practise/052文档测试.py", line 42, in __main__.Dict
# Failed example:
#     d2.c
# Exception raised:
#     Traceback (most recent call last):
#       File "/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/doctest.py", line 1337, in __run
#         compileflags, 1), test.globs)
#       File "<doctest __main__.Dict[6]>", line 1, in <module>
#         d2.c
#     AttributeError: 'Dict' object has no attribute 'c'
# **********************************************************************
# 1 items had failures:
#    2 of   9 in __main__.Dict
# ***Test Failed*** 2 failures.


