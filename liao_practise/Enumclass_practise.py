# --*-- coding:utf-8 --*--

# 当我们需要定义常量时，更好的方法是为这样的枚举类型定义一个class类型，然后，每个常量都是class的一个唯一实例。Python提供了Enum类来实现这个功能：

from enum import Enum, unique


#  下面程序演示了如何定义一个枚举类：如果想将一个类定义为枚举类，只需要令其继承自 enum 模块中的 Enum 类即可
class Color(Enum):
    # 为序列值指定value值
    red = 1
    green = 2
    blue = 3
    # 在 Color 枚举类中，red、green、blue 都是该类的成员（可以理解为是类变量
    # 注意，枚举类的每个成员都由 2 部分组成，分别为 name 和 value，
    # 其中 name 属性值为该枚举值的变量名（如 red），value 代表该枚举值的序号（序号通常从 1 开始）。
    # 和普通类的用法不同，枚举类不能用来实例化对象，但这并不妨碍我们访问枚举类中的成员

# Python 枚举类中各个成员必须保证 name 互不相同，但 value 可以相同
class Color2(Enum):
    # 为序列值指定value值
    red = 1
    green = 1
    blue = 3

# Color 枚举类中 red 和 green 具有相同的值（都是 1），Python 允许这种情况的发生，它会将 green 当做是 red 的别名，因此当访问 green 成员时，最终输出的是 red。
print(Color2['green'])

# 在实际编程过程中，如果想避免发生这种情况，可以借助 @unique 装饰器，这样当枚举类中出现相同值的成员时，程序会报 ValueError 错误
@unique
class Color3(Enum):
    # 为序列值指定value值
    red = 1
    green = 1
    blue = 3
print(Color3['green']) # 运行程序会报错：ValueError: duplicate values found in <enum 'Color'>: green -> red

# 除了通过继承 Enum 类的方法创建枚举类，还可以使用 Enum() 函数创建枚举类
# Enum() 函数可接受 2 个参数，第一个用于指定枚举类的类名，第二个参数用于指定枚举类中的多个成员。
# value属性则是自动赋给成员的int常量，默认从1开始计数。
Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))



if __name__ == '__main__':
    # 访问枚举类成员的方式有多种：
    # 调用枚举成员的 3 种方式
    print(Color.red)
    print(Color['red'])
    print(Color(1))
    # 调取枚举成员中的 value 和 name
    print(Color.red.value)
    print(Color.red.name)
    # #遍历枚举类中所有成员 2种方式
    for color in Color:
        print(color)
    # 该枚举类还提供了一个 __members__ 属性，该属性是一个包含枚举类中所有成员的字典，通过遍历该属性，也可以访问枚举类中的各个成员
    for name, member in Color.__members__.items():
        print(name, "->", member)

    # 枚举类成员之间不能比较大小，但可以用 == 或者 is 进行比较是否相等
    print(Color.red == Color.green)  # Flase
    print(Color.red.name is Color.green.name)  # Flase

    # 枚举类中各个成员的值，不能在类的外部做任何修改
    try:
        Color.red = 4
    except AttributeError as e:
        print(e)


    for a, b in Month.__members__.items():
        print(a, '=>',b,"name",b.value)



