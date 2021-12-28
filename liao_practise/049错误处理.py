# -*- coding:utf-8 -*-

if __name__ == '__main__':
    # 高级语言通常都内置了一套try...except...finally...的错误处理机制，Python也不例外
    # 当我们认为某些代码可能会出错时，就可以用try来运行这段代码，
    # 如果执行出错，则后续代码不会继续执行，而是直接跳转至错误处理代码，即except语句块，
    # 如果有finally语句块，则执行finally语句块，至此，执行完毕。
    try:
        print('try...')
        r = 10 / 0
        print('result:', r)
    except ZeroDivisionError as e:
        print('except:', e)
    finally:
        print('finally...')
    print('END')

    # 上面的代码在计算10 / 0时会产生一个除法运算错误
    # try...
    # except: division by zero
    # finally...
    # END
    # 后续语句print('result:', r)不会被执行

    # 错误应该有很多种类，如果发生了不同类型的错误，应该由不同的except语句块处理。没错，可以有多个except来捕获不同类型的错误
    try:
        print('try...')
        r = 10 / int('2')
        print('result:', r)
    except ValueError as e:  # int()函数可能会抛出ValueError，所以我们用一个except捕获ValueError，用另一个except捕获ZeroDivisionError。
        print('ValueError:', e)
    except ZeroDivisionError as e:
        print('ZeroDivisionError:', e)
    else:  # 如果没有错误发生，可以在except语句块后面加一个else，当没有错误发生时，会自动执行else语句
        print('no error!')
    finally:
        print('finally...')
    print('END')

    # Python的错误其实也是class，所有的错误类型都继承自BaseException，
    # 常见的错误类型和继承关系看这里：https://docs.python.org/3/library/exceptions.html#exception-hierarchy
    # 所以在使用except时需要注意的是，它不但捕获该类型的错误，还把其子类也“一网打尽”。
    try:
        a = 1
        print(a)
    except ValueError as e:
        print('ValueError')
    except UnicodeError as e:  # except永远也捕获不到UnicodeError，因为UnicodeError是ValueError的子类，如果有，也被第一个except给捕获了。
        print('UnicodeError')
    # 使用try...except捕获错误还有一个巨大的好处，就是可以跨越多层调用，
    # 比如函数main()调用bar()，bar()调用foo()，结果foo()出错了，这时，只要main()捕获到了，就可以处理：
    # 也就是说，不需要在每个可能出错的地方去捕获错误，只要在合适的层次去捕获错误就可以了。这样一来，就大大减少了写try...except...finally的麻烦。
    def foo(s):
        return 10 / int(s)

    def bar(s):
        return foo(s) * 2

    def main1():
        try:
            bar('0')
        except Exception as e:
            print('Error:', e)
        finally:
            print('finally...')

    # 如果错误没有被捕获，它就会一直往上抛，最后被Python解释器捕获，打印一个错误信息，然后程序退出。来看看
    main1()  # 执行结果如下
    # Traceback (most recent call last):         解读错误信息是定位错误的关键。我们从上往下可以看到整个错误的调用函数链：第1行告诉我们这是错误的跟踪信息
    #   File "err.py", line 11, in <module>      在代码文件err.py的第11行代码， 调用main()出错了，
    #     main()
    #   File "err.py", line 9, in main           原因是第9行，调用bar('0')出错了
    #     bar('0')
    #   File "err.py", line 6, in bar            原因是第6行， 原因是return foo(s) * 2这个语句出错了
    #     return foo(s) * 2
    #   File "err.py", line 3, in foo            原因是return 10 / int(s)这个语句出错了，
    #     return 10 / int(s)
    # ZeroDivisionError: division by zero        这是错误产生的源头，因为下面打印了:ZeroDivisionError: integer division or modulo by zero
    # 分析报错：根据错误类型ZeroDivisionError，我们判断，int(s)本身并没有出错，但是int(s)返回0，在计算10 / 0时出错，至此，找到错误源头。

    # 既然我们能捕获错误，就可以把错误堆栈打印出来，然后分析错误原因，同时，让程序继续执行下去。
    # Python内置的logging模块可以非常容易地记录错误信息
    import logging

    def main2():
        try:
            bar('0')
        except Exception as e:
            logging.exception(e)  # 通过配置，logging还可以把错误记录到日志文件里，方便事后排查。

    main2()
    print('END')
    # 同样是出错，但程序打印完错误信息后会继续执行，并正常退出

    # 抛出错误
    # 错误是class，捕获一个错误就是捕获到该class的一个实例。因此，错误并不是凭空产生的，而是有意创建并抛出的。
    # Python的内置函数会抛出很多类型的错误，我们自己编写的函数也可以抛出错误
    # 要抛出错误，首先根据需要，可以定义一个错误的class，选择好继承关系，然后，用raise语句抛出一个错误的实例：
    class FooError(ValueError):
        pass

    def foo1(s):
        n = int(s)
        if n == 0:
            raise FooError('invalid value: %s' % s)
        return 10 / n
    try:
        foo1('0') # 执行，可以最后跟踪到我们自己定义的错误：
    except Exception as e:
        print(e)
    # Traceback (most recent call last):
    #   File "err_throw.py", line 11, in <module>
    #     foo('0')
    #   File "err_throw.py", line 8, in foo
    #     raise FooError('invalid value: %s' % s)
    # __main__.FooError: invalid value: 0


    # 错误处理的方式：捕获了错误，再把错误通过raise语句抛出去
    # 捕获错误目的只是记录一下，便于后续追踪。但是，由于当前函数不知道应该怎么处理该错误，所以，最恰当的方式是继续往上抛，让顶层调用者去处理。
    # 好比一个员工处理不了一个问题时，就把问题抛给他的老板，如果他的老板也处理不了，就一直往上抛，最终会抛给CEO去处理。
    def bar1():
        try:
            foo('0')
        except ValueError as e:
            print('ValueError!')
            raise
    try:
        bar1()
    except Exception as e:
        print(e)

    # raise语句如果不带参数，就会把当前错误原样抛出。此外，在except中raise一个Error，还可以把一种类型的错误转化成另一种类型：
    try:
        10 / 0
    except ZeroDivisionError:
        raise ValueError('input error!')




