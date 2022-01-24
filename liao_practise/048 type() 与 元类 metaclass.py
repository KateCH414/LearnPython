# --*-- coding:utf-8 --*--

# 动态语言和静态语言最大的不同，就是函数和类的定义，不是编译时定义的，而是运行时动态创建的
# 定义一个Hello的class，就写一个hello.py模块
class Hello(object):
    def hello(self, name='world'):
        print('Hello, %s.' % name)

# 控制类的创建行为，还可以使用metaclass
# metaclass，直译为元类：释疑如下
# 当我们定义了类以后，就可以根据这个类创建出实例，所以：先定义类，然后创建实例。
# 但是如果我们想创建出类呢？那就必须根据metaclass创建出类，所以：先定义metaclass，然后创建类。
# 连接起来就是：先定义metaclass，就可以创建类，最后创建实例。
# 所以，metaclass允许你创建类或者修改类。换句话说，你可以把类看成是metaclass创建出来的“实例”。

# 一个简单的例子，这个metaclass可以给我们自定义的MyList增加一个add方法
# 定义ListMetaclass，按照默认习惯，metaclass的类名总是以Metaclass结尾，以便清楚地表示这是一个metaclass
# metaclass是类的模板，所以必须从`type`类型派生：
class ListMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs['add'] = lambda self, value: self.append(value)
        return type.__new__(cls, name, bases, attrs)

# 有了ListMetaclass，我们在定义类的时候还要指示使用ListMetaclass来定制类，传入关键字参数metaclass
class MyList(list, metaclass=ListMetaclass):
    pass

# 当我们传入关键字参数metaclass时，魔术就生效了，它指示Python解释器在创建MyList时，要通过ListMetaclass.__new__()来创建，
# 在此，我们可以修改类的定义，比如，加上新的方法，然后，返回修改后的定义。
# __new__()方法接收到的参数依次是：
# 1. 当前准备创建的类的对象；
# 2. 类的名字；
# 3. 类继承的父类集合
# 4. 类的方法集合

if __name__ == '__main__':
    # 当Python解释器载入hello模块时，就会依次执行该模块的所有语句，执行结果就是动态创建出一个Hello的class对象
    h = Hello()
    h.hello()
    print(type(Hello))  # <class 'type'>
    print(type(h))  # <class 'hello.Hello'>
    # type()函数可以查看一个类型或变量的类型，Hello是一个class，它的类型就是type，而h是一个实例，它的类型就是class Hello。
    # 我们说class的定义是运行时动态创建的，而创建class的方法就是使用type()函数。

    # type()函数既可以返回一个对象的类型，又可以创建出新的类型，
    # 比如，我们可以通过type() 函数创建出Hello类，而无需通过class Hello(object)...的定义

    def fn(self, name='world'):  # 先定义函数
        print('Hello, %s.' % name)

    Hello1 = type('Hello1', (object,), dict(hello=fn))  # 创建Hello class

    h1 = Hello1() # 使用 Hello1 创建对象 h1
    h1.hello()
    print(type(Hello1))  # <class 'type'>
    print(type(h1))  # <class 'hello.Hello'>

    # 要创建一个class对象，type()函数依次传入3个参数：
    # 1. class的名称；
    # 2. 继承的父类集合，注意Python支持多重继承，如果只有一个父类，别忘了tuple的单元素写法；
    # 3. class的方法名称与函数绑定，这里我们把函数fn绑定到方法名hello上。

    # 通过type()函数创建的类和直接写class是完全一样的，因为Python解释器遇到class定义时，仅仅是扫描一下class定义的语法，然后调用type()函数创建出class。
    # 正常情况下，我们都用class Xxx...来定义类，但是，type()函数也允许我们动态创建出类来，
    # 也就是说，动态语言本身支持运行期动态创建类，这和静态语言有非常大的不同，要在静态语言运行期创建类，必须构造源代码字符串再调用编译器，或者借助一些工具生成字节码实现，本质上都是动态编译，会非常复杂。


    # 使用MyList 的 add 方法
    L = MyList()
    L.add(1)
    L.add(2)
    print(L)  # [1, 2]

    # 普通的list没有add()方法
    l = list()
    try:
        l.add(1)
    except AttributeError as e:
        print(e)