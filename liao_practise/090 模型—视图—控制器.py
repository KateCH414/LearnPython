# --*-- coding:utf-8 --*--
"""
控制器模式
关注点分离（Separation of Concerns，SoC）原则是软件工程相关的设计原则之一
SoC 原则背后的思想是将一个应用切分成不同的部分，每个部分解决一个单独的关注点。
分层设计中的层次（数据访问层、业务逻辑层和表示层等）即是关注点的例子。
使用 SoC 原则能简化软件应用的开发和维护。

模型—视图—控制器（Model-View-Controller，MVC）模式是应用到面向对象编程的 Soc 原则
模式的名称来自用来切分软件应用的三个主要部分，即模型部分、视图部分和控制器部分。
MVC 被认为是一种架构模式而不是一种设计模式。架构模式与设计模式之间的区别在于前者比后者的范畴更广。

模型是核心的部分，代表着应用的信息本源，包含和管理（业务）逻辑、数据、状态以及应用的规则
视图是模型的可视化表现。视图的例子有，计算机图形用户界面、计算机终端的文本输出、智能手机的应用图形界面、PDF 文档、饼图和柱状图等。
    视图只是展示数据，并不处理数据
控制器是模型与视图之间的链接/粘附。模型与视图之间的所有通信都通过控制器进行。

对于将初始屏幕渲染给用户之后使用 MVC 的应用，其典型使用方式如下所示。
1。用户通过单击（键入、触摸等）某个按钮触发一个视图
2。视图把用户操作告知控制器
3。控制器处理用户输入，并与模型交互
4。模型执行所有必要的校验和状态改变，并通知控制器应该做什么
5。控制器按照模型给出的指令，指导视图适当地更新和显示输出


控制器部分提供的一大优势：无需修改模型就能使用多个视图的能力（甚至可以根据需要同时使用多个视图）。
为了实现模型与其表现之间的解耦，每个视图通常都需要属于它的控制器。
如果模型直接与特定视图通信，我们将无法对同一个模型使用多个视图（或者至少无法以简洁模块化的方式实现）。
"""

"""
Web 框架 web2py 是一个支持 MVC 模式的轻量级 Python 框架。
Django 也是一个 MVC 框架，但是它使用了不同的命名约定。
    在此约定下，控制器被称为视图，视图被称为模板。Django使用名称模型—模板—视图（Model-Template-View，MTV）来替代 MVC。
    依据 Django 的设计者所言，视图是描述哪些数据对用户可见。因此，Django 把对应一个特定 URL 的 Python 回调函数称为视图。
    Django 中的“模板”用于把内容与其展现分开，其描述的是用户看到数据的方式，而不是哪些数据可见。
"""

"""
应用场景
所有流行的 Web 框架（Django、Rails 和 Yii）和应用框架（iPhone SDK、Android 和 QT）都使用了 MVC 或者其变种，
其变种包括模式—视图—适配器（Model-View-Adapter，MVA）、模型—视图—演示者（Model-View-Presenter，MVP） 等。
有这么一些好处：
1：视图与模型的分离允许美工一心搞 UI 部分，程序员一心搞开发，不会相互干扰。
2：由于视图与模型之间的松耦合，每个部分可以单独修改/扩展，不会相互影响。
    例如，添加一个新视图的成本很小，只要为其实现一个控制器就可以了。
3：因为职责明晰，维护每个部分也更简单。

在从头开始实现 MVC 时， 请确保创建的模型很智能， 控制器很瘦， 视图很傻瓜。
可以将具有以下功能的模型视为智能模型。
1：包含所有的校验/业务规则/逻辑
2：处理应用的状态
3：访问应用数据（数据库、云或其他）
4：不依赖 UI

可以将符合以下条件的控制器视为瘦控制器。
1：在用户与视图交互时，更新模型
2：在模型改变时，更新视图
3：如果需要，在数据传递给模型/视图之前进行处理
4：不展示数据
5：不直接访问应用数据
6：不包含校验/业务规则/逻辑

可以将符合以下条件的视图称为傻瓜视图
1：展示数据
2：允许用户与其交互
3：仅做最小的数据，通常由一种模版语言提供处理能力（例如，使用简单的变量和循环控制） 
4：不存储任何数据
5：不直接访问应用数据
6：不包含校验/业务规则/逻辑

如果你正在从头实现 MVC，并且想弄清自己做得对不对，可以尝试回答以下两个关键问题。
1：如果你的应用有 GUI，那它可以换肤吗？易于改变它的皮肤/外观以及给人的感受吗？可以为用户提供运行期间改变应用皮肤的能力吗？如果这做起来并不简单，那就意味着你的 MVC 实现在某些地方存在问题
2：如果你的应用没有 GUI（例如，是一个终端应用），为其添加 GUI 支持有多难？或者，如果添加 GUI 没什么用，那么是否易于添加视图从而以图表（饼图、柱状图等）或文档（PDF、 电子表格等）形式展示结果？如果因此而作出的变更不小（小的变更是，在不变更模型的情况下，创建控制器并绑定到视图），那你的 MVC 实现就有些不对了。
"""

# demo 示例是名人名言打印机
# 用户输入一个数字，然后就能看到与这个数字相关的名人名言。
# 名人名言存储在一个 quotes 元组中。这种数据通常是存储在数据库、文件或其他地方，只有模型能够直接访问它。

# 数据，通常是存储在数据库，文件或其他地方，只要模型能够访问
quotes = ('A man is not complete until he is married. then he is finished',
          'As I said before, I never repeat myself',
          'Behind a successful man is an exhausted woman',
          'Black holes really suck...',
          'Facts are stubborn things')

# 模型
class QuoteModel:
    # 访问数据的操作
    def get_quote(self, n):
        try:
            value = quotes[n]
        except IndexError as err:
            value = 'Not found!'
        return value

# 视图
class QuoteTerminaView:
    def show(self, quote):
        print('And the quote is : {}'.format(quote))

    def error(self, msg):
        print('Error:{}'.format(msg))

    def selct_quote(self):
        return input('Which quote number would you like to see?')

# 控制器，负责协调
class QuoteTerminalController:
    # 初始化模型和视图
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteTerminaView()
    # 从模型中获取名言，并返回给视图展示
    def run(self):
        valid_input = False
        while not valid_input:
            n = self.view.selct_quote()
            try:
                n = int(n)
            except ValueError as err:
                self.view.error("Incorrect index '{}'".format(n))
            else:
                valid_input =True
        quote = self.model.get_quote(n)
        self.view.show(quote)


# 初始化并触发控制器
def main():
    controller = QuoteTerminalController()
    while True:
        controller.run()

if __name__ == '__main__':
    main()

"""
每个部分都有明确的职责。
模型负责访问数据，管理应用的状态
视图是模型的外在表现。视图并非必须是图形化的；文本输出也是一种好视图
控制器是模型与视图之间的连接

MVC 的恰当使用能确保最终产出的应用易于维护、易于扩展。
"""
