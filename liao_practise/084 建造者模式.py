# --*-- coding:utf-8 --*--
# 建造者模式
# 两个参与者：建造者（builder）和指挥者（director）
# 建造者：负责创建复杂对象的各个组成部分
# 指挥者：使用一个建造者实例控制建造过程
# 建造者模式可以解决HTML 页面生成问题，使用不同的建造者实例让我们可以创建不同的HTML页面，而无需变更指挥者的代码。

# 软件的例子
# django-widgy 是一个 Django 的第三方树编辑器扩展，可用作内容管理系统（Content Management System，CMS）。它包含一个网页构建器，用来创建具有不同布局的 HTML 页面。
# django-query-builder 是另一个基于建造者模式的 Django 第三方扩展库，该扩展库可用于动态地构建 SQL 查询。
# 使用它，我们能够控制一个查询的方方面面，并能创建不同种类的查询，从简单的到非常复杂的都可以。

# 应用案例
# 什么情况下使用建造者模式：
#   如果我们知道一个对象必须经过多个步骤来创建，并且要求同一个构造过程可以产生不同的表现
#   举例：这种需求存在于许多应用中
#       1: 页面生成器（本章提到的HTML 页面生成器之类）
#       2: 文档转换器
#       3: 用户界面（User Interface， UI）表单创建工具。
#  建造者模式也可用于解决可伸缩构造函数问题
#   为支持不同的对象创建方式而不得不创建一个新的构造函数时，可伸缩构造函数问题就发生了，这种情况最终产生许多构造函数和长长的形参列表，难以管理。
#   这个问题在 Python 中并不存在，因为至少有以下两种方式可以解决这个问题。
#       1:使用命名形参
#       2:使用实参列表展开

# 区别于工厂模式
#   工厂模式以单个步骤创建对象,而建造者模式以多个步骤创建对象
#   建造者模式几乎始终会使用一个指挥者
#       一些有针对性的建造者模式实现并未使用指挥者，如 Java 的 StringBuilder
#   在工厂模式下，会立即返回一个创建好的对象；而在建造者模式下，仅在需要时客户端代码才显式地请求指挥者返回最终的对象


# demo1
# 实现一个定制 PC 的建造者模式。
# 最后要创建的实例
class Computer:
    def __init__(self, serial_nember):
        self.serial = serial_nember
        self.memory = None   # 单位为GB
        self.hdd = None   # 单位为GB
        self.gpu = None

    def __str__(self):
        info = ('Memory: {}GB'.format(self.memory),
                'Hard Disk: {}GB'.format(self.hdd),
                'Graphics Card:{}'.format(self.gpu))
        return '\n'.join(info)


# 建造者
class ComputerBuilder:
    def __init__(self):
        self.computer = Computer('AG23385193')

    def configure_memory(self, amount):
        self.computer.memory = amount

    def configure_hdd(self, amount):
        self.computer.hdd = amount

    def configure_gpu(self, gpu_model):
        self.computer.gpu = gpu_model


# 指挥者
class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_computer(self, memory, hdd, gpu):
        self.builder = ComputerBuilder()
        [step for step in (self.builder.configure_memory(memory),
                           self.builder.configure_hdd(hdd),
                           self.builder.configure_gpu(gpu))]

    @property
    def computer(self):
        return self.builder.computer


# 执行创建
def mainForHardwareEngineer():
    engineer = HardwareEngineer()
    engineer.construct_computer(hdd=500, memory=8, gpu='GeForce GTX 650 Ti')
    computer = engineer.computer
    print(computer)


# demo2: 披萨为例的建造者模式：
from enum import Enum
import time

# 以空格为分隔，比如 PizzaProgress.queued=1, PizzaProgress.preparation=2
PizzaProgress = Enum('PizzaProgress', 'queued preparation baking ready')  # 下单，排队，预备，烤， 准备好
PizzaDough = Enum('PizzaDough', 'thin thick')  # 披萨面团，薄的，厚的
PizzaSauce = Enum('PizzaSauce', 'tomato creme_fraiche')  # 披萨酱汁  西红柿，奶油
PizzaTopping = Enum('PizzaTopping', 'mozzarella double_mozzarella bacon ham mushrooms red_onion oregano')
#                  披萨配料 马苏里奶酪， 两倍马苏里奶酪，熏猪肉，火腿，蘑菇，红色洋葱，牛至
STEP_DELAY = 3          # 考虑是示例，单位为秒


# 产品类
class Pizza:
    def __init__(self, name):
        self.name = name
        self.dough = None
        self.sauce = None
        self.topping = []

    def __str__(self):
        return self.name

    def prepare_dough(self, dough):
        # 准备面团
        self.dough = dough
        print('preparing the {} dough of your {}...'.format(self.dough.name, self))
        time.sleep(STEP_DELAY)
        print('done with the {} dough'.format(self.dough.name))


# 建造者 1
class MargaritaBuilder:
    """玛丽苏披萨制作流程"""
    def __init__(self):
        self.pizza = Pizza('margarita')  # 制作披萨是玛丽苏披萨
        self.progress = PizzaProgress.queued  # 流程-排队
        self.baking_time = 5  # 烤制时间 考虑是示例，单位为秒

    def prepare_dough(self):
        # 准备面团
        self.progress = PizzaProgress.preparation  # 流程-准备
        self.pizza.prepare_dough(PizzaDough.thin)  # 需要薄面团

    def add_sauce(self):
        # 添加酱汁
        print('adding the tomato sauce to your margarita...')
        self.pizza.sauce = PizzaSauce.tomato  # 番茄味酱汁
        time.sleep(STEP_DELAY)  # 等待时间
        print('done with the tomato sauce')

    def add_topping(self):
        # 添加原料
        print('adding the topping (double mozzarella, oregano) to your margarita')
        self.pizza.topping.append([i for i in
                                   (PizzaTopping.double_mozzarella, PizzaTopping.oregano)])
        # 向披萨依次添加原料为 两倍马苏里奶酪， 牛至
        time.sleep(STEP_DELAY)  # 等待时间

    def bake(self):
        self.progress = PizzaProgress.baking  # 流程-烤制中
        print('baking your margarita for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)  # 烤制时间
        self.progress = PizzaProgress.ready  # 流程-披萨完成
        print('your margarita is ready')


# 建造者2
class CreamyBaconBuilder:
    def __init__(self):
        self.pizza = Pizza('creamy bacon')
        self.progress = PizzaProgress.queued
        self.baking_time = 7

    def prepare_dough(self):
        self.progress = PizzaProgress.preparation
        self.pizza.prepare_dough(PizzaDough.thick)

    def add_sauce(self):
        print('adding the crème fraîche sauce to your creamy bacon')
        self.pizza.sauce = PizzaSauce.creme_fraiche
        time.sleep(STEP_DELAY)
        print('done with the crème fraîche sauce')

    def add_topping(self):
        print('adding the topping (mozzarella, bacon, ham, mushrooms, red onion, oregano) to your creamy bacon')
        self.pizza.topping.append([t for t in (PizzaTopping.mozzarella, PizzaTopping.bacon,
                                               PizzaTopping.ham, PizzaTopping.mushrooms,
                                               PizzaTopping.red_onion, PizzaTopping.oregano)])
        time.sleep(STEP_DELAY)
        print('done with the topping (mozzarella, bacon, ham, mushrooms, red onion, oregano)')

    def bake(self):
        self.progress = PizzaProgress.baking
        print('baking your creamy bacon for {} seconds'.format(self.baking_time))
        time.sleep(self.baking_time)
        self.progress = PizzaProgress.ready
        print('your creamy bacon is ready')


# 指挥者
class Waiter:
    def __init__(self):
        self.builder = None

    def consturct_pizza(self, builder):
        # 指挥者获取要指挥的建造者
        self.builder = builder
        # 依次执行建造者的步骤方法
        [step() for step in (builder.prepare_dough, builder.add_sauce,
                             builder.add_topping, builder.bake)]

    @property
    def pizza(self):
        return self.builder.pizza


def validate_style(builder):
    # 建造者模式中的顾客
    try:
        pizza_style = input("你喜欢什么披萨，[m]玛丽苏味 or [c]奶油 [b]咸肉？")
        builder = builder[pizza_style]()
        # 根据字典健值 builders[m]() 类实例化 并生成对象builder
        # 将顾客选择好的披萨（建造者）返回给指挥者
        valid_input = True
    except KeyError as Err:
        print("对不起没有这个味道")
        return (False, None)
    return (True, builder)


def mainForPizzaBilder():
    builders = dict(m=MargaritaBuilder, c=CreamyBaconBuilder)
    valid_input = False
    while not valid_input:
        valid_input, builder = validate_style(builders)
    print()
    waiter = Waiter()
    waiter.consturct_pizza(builder)
    pizza = waiter.pizza
    print("请享受你的{}".format(pizza))


"""
demo3 流利的建造者
一种有趣的建造者模式变体
这种变体会链式地调用建造者方法，
通过将建造者本身定义为内部类并从其每个设置器方法返回自身来实现。
方法 build() 返回最终的对象。
"""


# 产品类
class Pizza2:
    def __init__(self, builder):
        self.garlic = builder.garlic
        self.extra_cheese = builder.extra_cheese

    def __str__(self):
        garlic = 'yes' if self.garlic else 'no'
        cheese = 'yes' if self.extra_cheese else 'no'
        info = ('Garlic:{}'.format(garlic), 'Extra cheese: {}'.format(cheese))
        return '\n'.join(info)

    # 建造者
    # 将建造者本身定义为内部类，并从其每个设置器方法返回自身来实现。
    class PizzaBuilder:
        def __init__(self):
            self.extra_cheese = False
            self.garlic = False

        def add_garlic(self):
            self.garlic = True
            return self

        def add_extra_cheese(self):
            self.extra_cheese = True
            return self

        def build(self):
            return Pizza2(self)


if __name__ == '__main__':
    # mainForHardwareEngineer()
    # mainForPizzaBilder()

    pizza = Pizza2.PizzaBuilder().add_garlic().add_extra_cheese().build()
    print(pizza)




"""
和工厂模式不一样，工厂模式是直接返回一个产品（或工厂），输入输出直接，
建造者模式，需要指挥者指挥建造者工作之后，才能获得产品，
所以建造者模式需要指挥者和建造者两个角色
建造者
    就是搬砖干活的，所以他应该有各种干活能力，这样指挥者才好指挥他们干活
指挥者
    指挥者毫无疑问是指挥人干活的，虽然不用每事亲力亲为，但他需要了解干活步骤，
开始干活
    把建造者给指挥者，指挥开始指挥建造者干活，最终得到产品
"""















