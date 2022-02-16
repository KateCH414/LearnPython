# --*-- coding:utf-8 --*--
"""
functools模块提供了一系列的高阶函数以及对可调用对象的操作，
其中为人熟知的有reduce，partial，wraps等。

为了保证被装饰器装饰后的函数还拥有原来的属性，wraps通过partial以及update_wrapper来实现。
先来了解一下partial
partial用于部分应用一个函数，它基于一个函数创建一个可调用对象，把原函数的某些参数固定，调用时只需要传递未固定的参数即可。
"""
# partial如何使用：
import functools


def add(a, b):
    print(a + b)


add = functools.partial(add, 1)  # 把原函数的某些参数固定
print(add(2))  # 3
# add函数原本接收两个参数a和b，经过partial包装之后，a参数的值被固定为了1，
# 新的add对象（注意此处add已经是一个可调用对象，而非函数，下文分析源码会看到）只需要接收一个参数即可。
# 总结：partial 就是把原函数的部分参数固定了初始值，新的调用只需要传递其它参数。


# 下面来分析partial的源码（Python3.7），只摘录了核心部分：
class partial:
    """New function with partial application of the given arguments
    and keywords.
    """

    __slots__ = "func", "args", "keywords", "__dict__", "__weakref__"

    def __new__(*args, **keywords):
        if not args:
            raise TypeError("descriptor '__new__' of partial needs an argument")
        if len(args) < 2:
            raise TypeError("type 'partial' takes at least one argument")
        cls, func, *args = args
        if not callable(func):
            raise TypeError("the first argument must be callable")
        args = tuple(args)

        if hasattr(func, "func"):
            args = func.args + args
            tmpkw = func.keywords.copy()
            tmpkw.update(keywords)
            keywords = tmpkw
            del tmpkw
            func = func.func

        self = super(partial, cls).__new__(cls)

        self.func = func
        self.args = args
        self.keywords = keywords
        return self

    def __call__(*args, **keywords):
        if not args:
            raise TypeError("descriptor '__call__' of partial needs an argument")
        self, *args = args
        newkeywords = self.keywords.copy()
        newkeywords.update(keywords)
        return self.func(*self.args, *args, **newkeywords)


"""
通过重写“_new__”方法，自定义对象实例化过程。
1、元组拆包，获取到传入的原函数（func）和需要固定的参数（args）
cls, func, *args = args

2、主要是为了支持嵌套调用，即add=partial(partial(add,1),2)这种情况，可先看第三步，回过头再来看
if hasattr(func, "func"):
    args = func.args + args
    tmpkw = func.keywords.copy()
    tmpkw.update(keywords)
    keywords = tmpkw
    del tmpkw
    func = func.func
    
3、实例化partial对象，将传入的函数和参数设置为当前对象的属性
self = super(partial, cls).__new__(cls)
self.func = func
self.args = args
self.keywords = keywords
return self

到这里我们已经明白了partial是怎么保存原函数和固定参数的了，下面来看一下调用的时候是如何执行的。
先简单了解一下可调用对象：当一个类实现了"__call__"方法后，这个类的对象就能够像函数一样被调用。
class Callable:
    def __call__(self, a, b):
        return a + b


func = Callable()  
result = func(2, 3) # 像函数一样调用
print(result)  # 输出：5

我们看下partial的"__call__"是如何实现的：
def __call__(*args, **keywords):
        if not args:
            raise TypeError("descriptor '__call__' of partial needs an argument")
        self, *args = args
        newkeywords = self.keywords.copy()
        newkeywords.update(keywords)
        return self.func(*self.args, *args, **newkeywords)

1、元组拆包，获取到传入的非固定参数args
self, *args = args

2、拷贝当前对象的keywords参数，并且合并传入的非固定参数字典
newkeywords = self.keywords.copy()
newkeywords.update(keywords)

3。调用当前对象的func属性，func即被partial包装的原函数，同时传入暂存的固定参数self.args以及新传入的其它参数。

总结：partial通过实现"__new__"和"__call__"生成一个可调用对象，
这个对象内部保存了被包装函数以及固定参数，这个对象可以像函数一样被调用，
调用时，其实是执行了对象内部持有的被包装函数，其参数由固定参数和新传入的参数组合而来。
"""

# 探索wraps的源码
def wraps(wrapped, assigned = WRAPPER_ASSIGNMENTS,updated = WRAPPER_UPDATES):
    """
        Decorator factory to apply update_wrapper() to a wrapper function

       Returns a decorator that invokes update_wrapper() with the decorated
       function as the wrapper argument and the arguments to wraps() as the
       remaining arguments. Default arguments are as for update_wrapper().
       This is a convenience function to simplify applying partial() to
       update_wrapper().
    """

    return partial(update_wrapper, wrapped=wrapped,
                   assigned=assigned, updated=updated)
"""
入参解读：

wrapped：指被装饰器装饰的原函数，我们的装饰器便是要拷贝它的属性。

assigned：要被重新赋值的属性列表，默认为WRAPPER_ASSIGNMENTS，可自定义传入
WRAPPER_ASSIGNMENTS = ('__module__', '__name__', '__qualname__', '__doc__',
                       '__annotations__')

updated：要被合并的属性列表，默认为WRAPPER_UPDATES，可自定义传入
WRAPPER_UPDATES = ('__dict__',)

返回值：返回了一个partial对象，这个对象对update_wrapper进行了包装，固定了wrapped，assigned，updated三个参数。

wraps本省就是一个装饰器，因为它返回的是一个“函数”即partial对象，这个对象接收函数作为参数，同时以函数作为返回值。

"""

def update_wrapper(wrapper,
                   wrapped,
                   assigned = WRAPPER_ASSIGNMENTS,
                   updated = WRAPPER_UPDATES):
    """Update a wrapper function to look like the wrapped function

       wrapper is the function to be updated
       wrapped is the original function
       assigned is a tuple naming the attributes assigned directly
       from the wrapped function to the wrapper function (defaults to
       functools.WRAPPER_ASSIGNMENTS)
       updated is a tuple naming the attributes of the wrapper that
       are updated with the corresponding attribute from the wrapped
       function (defaults to functools.WRAPPER_UPDATES)
    """
    for attr in assigned:
        try:
            value = getattr(wrapped, attr)
        except AttributeError:
            pass
        else:
            setattr(wrapper, attr, value)
    for attr in updated:
        getattr(wrapper, attr).update(getattr(wrapped, attr, {}))
    # Issue #17482: set __wrapped__ last so we don't inadvertently copy it
    # from the wrapped function when updating __dict__
    wrapper.__wrapped__ = wrapped
    # Return the wrapper so this can be used as a decorator via partial()
    return wrapper

"""
这个便是解析@functools.wraps(func)时最底层执行的逻辑，代码很简洁，
就是把wrapped函数的属性拷贝到wrapper函数中。
wrapped是被装饰的原函数
wrapper是被装饰器装饰后的新函数。
"""
# 通过下面的例子对执行过程和参数进行对号入座
def outer(func):
    @functools.wraps(func)
    def inner(*args, **kwargs):
        print(f"before...")
        func(*args, **kwargs)
        print("after...")

    return inner

@outer
def add(a, b):
    """
    求和运算
    """
    print(a + b)

"""
1、原函数为add。
2，@outer会去执行outer装饰器，传入add函数，返回一个inner函数
3，执行outer函数时，加载inner函数，此时会直接执行functools.wraps(func)返回一个可调用对象，即partial对象。
4、此时inner的装饰器实际上是@partial，partial会被调用，传入inner函数，
   执行partial内部的update_wrapper函数，将func的相应属性拷贝给inner函数，
   最后返回inner函数。这一步并没有生成新的函数，仅仅是改变了inner函数的属性。
5、把add指向inner函数。
6、调用add实际调用的是inner函数，inner函数内部持有原add函数的引用即func。

update_wrapper函数参数对应：
wrapper指的是inner函数
wrapped指的是func即原始的add函数
"""
"""
整体总结：
1）functools.wraps 旨在消除装饰器对原函数造成的影响，即对原函数的相关属性进行拷贝，已达到装饰器不修改原函数的目的。
2）wraps内部通过partial对象和update_wrapper函数实现。
3）partial是一个类，通过实现了双下方法new，自定义实例化对象过程，使得对象内部保留原函数和固定参数，通过实现双下方法call，使得对象可以像函数一样被调用，再通过内部保留的原函数和固定参数以及传入的其它参数进行原函数调用。
"""


