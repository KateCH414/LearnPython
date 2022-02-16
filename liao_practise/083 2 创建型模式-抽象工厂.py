# --*-- coding:utf-8 --*--
# Abstract Factory 抽象工厂：解决复杂对象的创建问题
# 一个抽象工厂是（逻辑上的）一组工厂方法，其中的每个工厂方法负责产生不同种类的对象。
# 使用举例：程序包 django_factory 是一个用于在测试中创建 Django 模型的抽象工厂实现，可用来为支持测试专有属性的模型创建实例。
# 优点：抽象工厂模式是工厂方法模式的一种泛化，所以它能提供相同的好处。
# 适用场景：通常一开始时使用工厂方法，因为它更简单。如果后来发现应用需要许多工厂方法，那么将创建一系列对象的过程合并在一起更合理，从而最终引入抽象工厂。
# 抽象工厂能够通过改变激活的工厂方法动态地（运行时）改变应用行为。

# demo:

# 类别一：青蛙
class Frog:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        """不同类型玩家遇到的障碍不同"""
        print('{} the Frog encounters {} and {}!'.format(
            self, obstacle, obstacle.action()))
# 类别一：虫子
class Bug:
    def __str__(self):
        return 'a bug'

    def action(self):
        return 'eats it'
# 类别一：工厂方法
class Frogworld:
    def __init__(self, name):
        print(self)
        self.play_name = name

    def __str__(self):
        return '\n\n\t----Frog World -----'
    # 创建角色：返回青蛙
    def make_character(self):
        return Frog(self.play_name)
    # 创建障碍：返回虫子
    def make_obstacle(self):
        return Bug()

# 类别二：巫师
class Wizard:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def interact_with(self, obstacle):
        print('{} the Wizard battles against {} and {}!'.format(
            self, obstacle, obstacle.action()
        ))

# 类别二：兽人
class Ork:
    def __str__(self):
        return 'an evil ok'

    def action(self):
        return 'kill it'

# 类别二：工厂方法
class WizardWorld:
    def __init__(self, name):
        print(self)
        self.player_name = name

    def __str__(self):
        return '\n\n\t-------Wizard World---------'

    def make_character(self):
        return Wizard(self.player_name)

    def make_obstacle(self):
        return Ork()

# 与设计模式无关的判断
def adults_age(age):
    if age > 18:
        return True
    else:
        return False

# 抽象工厂方法
class GameEnvironment:
    """ 抽象工厂， 根据不同的玩家类型创建不同的角色和障碍（游戏环境）"""
    """ 这里可以根据年龄判断，成年人返回【巫师】， 小孩返回【青蛙过河】"""
    def __init__(self, age):
        if adults_age(age):
            self.hero = WizardWorld('adults').make_character()
            self.obstacle = WizardWorld('adults').make_obstacle()
        else:
            self.hero = WizardWorld('minor').make_character()
            self.obstacle = WizardWorld('minor').make_obstacle()

    def play(self):
        self.hero.interact_witch(self.obstacle)


if __name__ == '__main__':
    # 参数设置

    environment = GameEnvironment(12)
    environment.play()

# 类别一和二都得对不同种类的对象进行实例化
# 于是封装抽象工厂模式，使得两种类别都可以凭这个抽象工厂方法创建各自的对象。

# 两种模式都可以用于以下几种场景：(a)想要追踪对象的创建时，(b)想要将对象的创建与使用解耦时，(c)想要优化应用的性能和资源占用时
# 工厂方法设计模式的实现是一个不属于任何类的单一函数，负责单一种类对象（一个形状、 一个连接点或者其他对象）的创建。
# 抽象工厂设计模式的实现是同属于单个类的许多个工厂方法用于创建一系列种类的相关对象（一辆车的部件、一个游戏的环境，或者其他对象）。

