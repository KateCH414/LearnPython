# --*-- coding:utf-8 --*--
"""
解释器模式
对每个应用来说，至少有以下两种不同的用户分类：
1：基本用户：这类用户只希望能够凭直觉使用应用。他们不喜欢花太多时间配置或学习应用的内部。对他们来说，基本的用法就足够了
2：高级用户：这些用户，实际上通常是少数，不介意花费额外的时间学习如何使用应用的高级特性。如果知道学会之后能得到以下好处，他们甚至会去学习一种配置（或脚本）语言。
    能够更好地控制一个应用
    以更好的方式表达想法
    提高生产力
解释器（Interpreter）模式仅能引起应用的高级用户的兴趣。
    这是因为解释器模式背后的主要思想是让非初级用户和领域专家使用一门简单的语言来表达想法。
想要创建的是一种领域特定语言（Domain Specific Language，DSL）。
DSL 是一种针对一个特定领域的有限表达能力的计算机语言
很多不同的事情都使用 DSL，比如，战斗模拟、记账、可视化、配置、通信协议等

DSL 分为内部 DSL 和外部 DSL
内部 DSL 构建在一种宿主编程语言之上。内部 DSL 的一个例子是，使用 Python 解决线性方程组的一种语言
    使用内部 DSL 的优势是我们不必担心创建、编译及解析语法，因为这些已经被宿主语言解决掉了
    劣势是会受限于宿主语言的特性。如果宿主语言不具备这些特性，构建一种表达能力强、简洁而且优美的内部 DSL 是富有挑战性的
外部 DSL 不依赖某种宿主语言。
    优势：DSL 的创建者可以决定语言的方方面面（语法、句法等
    劣势：但也要负责为其创建一个解析器和编译器。为一种新语言创建解析器和编译器是一个非常复杂、长期而又痛苦的过程。

解释器模式仅与内部 DSL 相关。
因此，我们的目标是使用宿主语言提供的特性构建一种简单但有用的语言，在这里，宿主语言是 Python。
注意，解释器根本不处理语言解析，它假设我们已经有某种便利形式的解析好的数据，可以是抽象语法树（abstract syntax tree，AST）或任何其他好用的数据结构
"""
"""
例子
PyT 是一个用于生成 (X)HTML 的 Python DSL。PyT 关注性能，并声称能与 Jinja2 的速度相媲美。
"""
"""
应用场景
希望为领域专家和高级用户提供一种简单语言来解决他们的问题时，可以使用解释器模式
不过要强调的第一件事情是，解释器模式应仅用于实现简单的语言
我们的目标是为专家提供恰当的编程抽象，使其生产力更高
这些专家通常不是程序员。理想情况下，他们使用我们的 DSL 并不需要了解高级 Python 知识，当然了解一点 Python 基础知识会更好，因为我们最终生成的是 Python 代码，但不应该要求了解 Python 高级概念。
此外，DSL 的性能通常不是一个重要的关注点。重点是提供一种语言，隐藏宿主语言的独特性，并提供人类更易读的语法。
"""
"""
demo
创建一种内部 DSL 控制一个智能屋。
用户能够使用一种非常简单的事件标记来控制他们的房子
一个事件的形式为 command -> receiver -> arguments
参数部分是可选的。并不是所有事件都要求参数。不要求任何参数的事件例子如下所示：open -> gate
要求参数的事件例子如下所示：increase -> boiler temperature -> 3 degrees
-> 符号用于标记事件一个部分的结束,并声明下一个部分的开始
实现一种内部 DSL 有多种方式
我们可以使用普通的正则表达式、字符串处理、操作符重载的组合以及元编程，或者一个能帮我们完成困难工作的库/工具
虽然在正规情况下，解释器不处理解析，但这里的例子想要覆盖解析工作
作者决定使用一个工具来完成解析工作。该工具名为 Pyparsing
    可以参考 Paul McGuire 编写的迷你书 Getting Started with Pyparsing
安装：pip3 install pyparsing
为我们的语言定义一种简单语法是一个好做法。
我们可以使用巴科斯-诺尔形式（Backus-Naur Form，BNF）表示法来定义语法：
event ::= command token receiver token arguments
command ::= word+
word ::= a collection of one or more alphanumeric characters
token ::= ->
receiver ::= word+
arguments ::= word+

这个语法告诉我们的是一个事件具有 command -> receiver -> arguments 的形式
并且命令、接收者及参数也具有相同的形式，即一个或多个字母数字字符的组合
包含数字部分是为了让我们能够在命令 increase -> boiler temperature -> 3 degrees 中传递 3 degrees 这样的参数
既然定义了语法，那么接着将其转变成实际的代码。以下是代码的样子。

word = Word(alphanums)
command = Group(OneOrMore(word))
token = Suppress("->")
device = Group(OneOrMore(word))
argument = Group(OneOrMore(word))
event = command + token + device + Optional(token + argument)

代码和语法定义基本的不同点是，代码需要以自底向上的方式编写。
例如，如果不先为 word 赋一个值，那就不能使用它。Suppress 用于声明我们希望解析结果中省略 -> 符号。
"""
# 一个锅炉的默认温度为 83 摄氏度。类有两个方法来分别提高和降低当前的温度。
class Boiler:
    def __init__(self):
        self.temperature = 83  #摄氏度

    def __str__(self):
        return 'boiler temperature: {}'.format(self.temperature)

    def increase_temperature(self, amount):
        print("increasing the boiler's temperature by {} degrees".format(amount))
        self.temperature += amount

    def decrease_temperature(self, amount):
        print("decreasing the boiler's temperature by {} degrees".format(amount))
        self.temperature -= amount

# 下一步是添加语法，之前已学习过。我们也创建一个 boiler 实例，并输出其默认状态。
"""
获取 Pyparsing 解析结果的最简单方式是使用 parseString() 方法
该方法返回的结果是一个 ParseResults 实例，它实际上是一个可视为嵌套列表的解析树
例如，执行 print(event. parseString('increase -> boiler temperature -> 3 degrees')) 
得到的结果如下所示：
[['increase'], ['boiler', 'temperature'], ['3', 'degrees']]

实际上我们可以解开 ParseResults 实例，从而可以直接访问事件的这三个部分。
可直接访问意味着我们可以匹配模式找到应该执行哪个方法。
cmd, dev, arg = event.parseString('increase -> boiler temperature -> 3 degrees')
if 'increase' in ' '.join(cmd):
    if 'boiler' in ' '.join(dev):
        boiler.increase_temperature(int(arg[0]))
print(boiler)
"""
from pyparsing import  Word, OneOrMore, Optional, Group, Suppress, alphanums

class Gate:  # 门
    def __init__(self):
        self.is_open = False

    def __str__(self):
        return 'open' if self.is_open else 'closed'

    def open(self):
        print('opening the gate')
        self.is_open = True

    def close(self):
        print('closing the gate')
        self.is_open = False

class Garage:  # 车库
    def __init__(self):
        self.is_open = False

    def __str__(self):
        return 'open' if self.is_open else 'closed'

    def open(self):
        print('opening the garage')
        self.is_open = True

    def close(self):
        print('closing the garage')
        self.is_open = False

class Aircondition:  # 冷气机
    def __init__(self):
        self.is_on = False

    def __str__(self):
        return 'on' if self.is_on else 'off'

    def turn_on(self):
        print('turning on the aircondition')
        self.is_on = True

    def turn_off(self):
        print('turning off the aircondition')
        self.is_on = False


class Heating:  # 采暖

    def __init__(self):
        self.is_on = False

    def __str__(self):
        return 'on' if self.is_on else 'off'

    def turn_on(self):
        print('turning on the heating')
        self.is_on = True

    def turn_off(self):
        print('turning off the heating')
        self.is_on = False


class Fridge:  # 冰箱

    def __init__(self):
        self.temperature = 2  # 单位为摄氏度

    def __str__(self):
        return 'fridge temperature: {}'.format(self.temperature)

    def increase_temperature(self, amount):
        print("increasing the fridge's temperature by {} degrees".format(amount))
        self.temperature += amount

    def decrease_temperature(self, amount):
        print("decreasing the fridge's temperature by {} degrees".format(amount))
        self.temperature -= amount


def main():
    word = Word(alphanums)
    command = Group(OneOrMore(word))
    token = Suppress("->")
    device = Group(OneOrMore(word))
    argument = Group(OneOrMore(word))
    event = command + token + device + Optional(token + argument)

    gate = Gate()
    garage = Garage()
    airco = Aircondition()
    heating = Heating()
    boiler = Boiler()
    fridge = Fridge()

    tests = ('open -> gate',
             'close -> garage',
             'turn on -> aircondition',
             'turn off -> heating',
             'increase -> boiler temperature -> 5 degrees',
             'decrease -> fridge temperature -> 2 degrees')

    open_actions = {'gate': gate.open,
                    'garage': garage.open,
                    'aircondition': airco.turn_on,
                    'heating': heating.turn_on,
                    'boiler temperature': boiler.increase_temperature,
                    'fridge temperature': fridge.increase_temperature}

    close_actions = {'gate': gate.close,
                     'garage': garage.close,
                     'aircondition': airco.turn_off,
                     'heating': heating.turn_off,
                     'boiler temperature': boiler.decrease_temperature,
                     'fridge temperature': fridge.decrease_temperature}

    for t in tests:
        if len(event.parseString(t)) == 2: # 没有参数
            cmd, dev = event.parseString(t)
            cmd_str, dev_str = ''.join(cmd), ''.join(dev)
            if 'open' in cmd_str or 'turn on' in cmd_str:
                open_actions[dev_str]()
            elif 'close' in cmd_str or 'turn off' in cmd_str:
                close_actions[dev_str]()
        elif len(event.parseString(t)) == 3: # 有参数
            cmd, dev, arg = event.parseString(t)
            cmd_str, dev_str, arg_str = ' '.join(cmd), ' '.join(dev), ' '.join(arg)
            num_arg = 0
            try:
                num_arg = int(arg_str.split()[0])  # 抽取数值部分
            except ValueError as err:
                print("expected number but got: '{}'".format(arg_str[0]))
            if 'increase' in cmd_str and num_arg > 0:
                open_actions[dev_str](num_arg)
            elif 'decrease' in cmd_str and num_arg > 0:
                close_actions[dev_str](num_arg)

if __name__ == '__main__':
    main()





