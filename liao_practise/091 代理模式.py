# --*-- coding:utf-8 --*--
"""
代理模式
延迟初始化：我们想要把一个计算成本较高的对象的创建过程延迟到用户首次真正使用它时才进行。
这类操作通常使用代理设计模式（Proxy design pattern）来实现。该模式因使用代理（又名替代，surrogate）
对象在访问实际对象之前执行重要操作而得其名。
以下是四种不同的知名代理类型。
1：远程代理：实际存在于不同地址空间（例如，某个网络服务器）的对象在本地的代理者。
2：虚拟代理：用于懒初始化，将一个大计算量对象的创建延迟到真正需要的时候进行。
3：保护/防护代理：控制对敏感对象的访问
4：智能（引用）代理：在对象被访问时执行额外的动作。此类代理的例子包括引用计数和线程安全检查。

使用 Python 来创建虚拟代理存在很多方式，但我始终喜欢地道的/符合 Python 风格的实现。
为避免混淆，我先说明一下，在本节中，术语特性（property）、变量、属性（attribute）可相互替代使用

我们先创建一个 LazyProperty 类，用作一个修饰器。当它修饰某个特性时，LazyProperty 惰性地（首次使用时）加载特性，而不是立即进行。
描述符（descriptor） 是 Python 中重写类属性访问方法（__get__()、__set__() 和 __delete__()）的默认行为要使用的一种推荐机制。
"""
# lazyProperty 类 实际上是一个描述符
class LazyProperty:
    def __init__(self, method):
        # method 变量是一个实际方法的别名
        # method_name 变量则是该方法名称的别名
        self.method =method
        self.method_name = method.__name__
        # print('function overriden: {}'.format(self.method))
        # print("function's name: {}".format(self.method_name))

    # LazyProperty 类仅重写了 __get__(), 因为这是其需要重写的唯一访问方法
    def __get__(self, obj, cls):
        # __get__() 使用值来替代方法，这意味着不仅特性是惰性加载的，而且仅可以设置一次
        if not obj:
            return None
        value = self.method(obj)
        # print('value {}'.format(value))
        setattr(obj, self.method_name, value)
        return value


class Test:
    def __init__(self):
        self.x = 'foo'
        self.y = 'bar'
        # 我们想懒加载 _resource 变量，因此将其初始化为 None
        self._resource = None

    @LazyProperty
    def resource(self):
        print('initializing self._resource which is: {}'.format(self._resource))
        self._resource = tuple(range(5))  # 假设这一行的计算成本比较大
        return self._resource


def main():
    t = Test()
    print(t.x)
    print(t.y)
    # 注意，__get__() 访问方法的重写使得可以将 resource() 方法当作一个变量
    print(t.resource)
    print(t.resource)

"""
1: _resource 变量实际不是在 t 实例创建时初始化的，而是在我们首次使用 t.resource 时
2: 第二次使用 t.resource 之时， 并没有再次初始化变量。 
    这就是为什么初始化字符串 initializing self._resource which is: 仅出现一次的原因

在 OOP 中有两种基本的、不同类型的懒初始化，如下所示：
1: 在实例级：这意味着会一个对象的特性进行懒初始化，但该特性有一个对象作用域。同一个类的每个实例（对象）都有自己的（不同的）特性副本。
2: 在类级或模块级：在这种情况下，我们不希望每个实例都有一个不同的特性副本，而是所有实例共享同一个特性，而特性是懒初始化的。
"""

"""
应用场景
因为存在至少四种常见的代理类型，所以代理设计模式有很多应用案例，如下所示：
1：在使用私有网络或云搭建一个分布式系统时。在分布式系统中，一些对象存在于本地内存中，一些对象存在于远程计算机的内存中。
    如果我们不想本地代码关心两者之间的区别，那么可以创建一个远程代理来隐藏/封装，使得应用的分布式性质透明化。
2：因过早创建计算成本较高的对象导致应用遭受性能问题之时。使用虚拟代理引入懒初始化，
    仅在真正需要对象之时才创建，能够明显提高性能。
3：用于检查一个用户是否有足够权限来访问某个信息片段。如果应用要处理敏感信息（例如，医疗数据），
    我们会希望确保用户在被准许之后才能访问/修改数据。一个保护/防护代理可以处理所有安全相关的行为。
4：应用（或库、工具集、框架等）使用多线程，而我们希望把线程安全的重任从客户端代码转移到应用。
    这种情况下，可以创建一个智能代理，对客户端隐藏线程安全的复杂性。
5：对象关系映射（Object-Relational Mapping，ORM）API 也是一个如何使用远程代理的例子。
    包括 Django 在内的许多流行 Web 框架使用一个 ORM 来提供类 OOP 的关系型数据库访问。
    ORM 是关系型数据库的代理，数据库可以部署在任意地方，本地或远程服务器都可以。
"""

"""
demo 实现
为演示代理模式，我们将实现一个简单的保护代理来查看和添加用户。该服务提供以下两个选项。
1：查看用户列表：这一操作不要求特殊权限
2：添加新用户：这一操作要求客户端提供一个特殊的密码。
# 现实中，永远不要执行以下操作：
1：在源代码中存储密码
2：以明文形式存储密码
3：使用一种弱（例如，MD5）或自定义加密形式
"""
class SensitiveInfo:
    def __init__(self):
        self.users = ['nick', 'tom', 'ben', 'mike']

    def read(self):
        print('There are {} users: {}'.format(len(self.users), ''.join(self.users)))

    def add(self, user):
        self.users.append(user)
        print('Added user {}'.format(user))

# SensitiveInfo的保护代理
class Info:
    def __init__(self):
        self.protected = SensitiveInfo()
        self.secret = '0xdeadbeef'

    def read(self):
        self.protected.read()

    def add(self, user):
        sec = input('what is the secret?')
        self.protected.add(user) if sec == self.secret else print("That is wrong!")

def main2():
    info = Info()
    while True:
        print('1. read list |==| 2. add user |==| 3. quit')
        key = input('choose option: ')
        if key == '1':
            info.read()
        elif key == '2':
            name = input('choose username:')
            info.add(name)
        elif key == '3':
            exit()
        else:
            print('unknown option: {}'.format(key))

"""
这个代理示例中存在可以改进的缺陷或缺失特性，有如下一些建议：
1: 该示例有一个非常大的安全缺陷。没有什么能阻止客户端代码通过直接创建一个 SensitveInfo 实例来绕过应用的安全设置。
   优化示例来阻止这种情况。一种方式是使用 abc 模块来禁止直接实例化 SensitiveInfo。
2: 一个基本的安全原则是，我们绝不应该存储明文密码。只要我们知道使用哪个库，安全地存储密码并不是一件难事。
   参考加盐密码哈希可以尝试实现一种外部存储密码的安全方式（例如，在一个文件或数据库中）
"""

if __name__ == '__main__':
    main()
    main2()

"""
总结：
存在四种不同的代理类型
1. 远程代理，代表一个活跃于远程位置（例如，我们自己的远程服务器或云服务）的对象。
2. 虚拟代理，将一个对象的初始化延迟到真正需要使用时进行。
3. 保护/防护代理，用于对处理敏感信息的对象进行访问控制。
4. 当我们希望通过添加帮助信息（比如，引用计数）来扩展一个对象的行为时，可以使用 智能（引用）代理。
"""












