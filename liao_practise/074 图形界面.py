# --*-- coding:utf-8 --*--
# Python支持多种图形界面的第三方库，包括：Tk，wxWidgets，Qt，GTK，等等。
# 但是Python自带的库是支持Tk的Tkinter，使用Tkinter，无需安装任何包，就可以直接使用。

# 本章简单介绍如何使用Tkinter进行GUI编程。
# 我们编写的Python代码会调用内置的Tkinter，Tkinter封装了访问Tk的接口；
# Tk是一个图形库，支持多个操作系统，使用Tcl语言开发；
# Tk会调用操作系统提供的本地GUI接口，完成最终的GUI。
# 所以，我们的代码只需要调用Tkinter提供的接口就可以了。

# 第一步是导入Tkinter包的所有内容：
from tkinter import *
import tkinter.messagebox as messagebox


# 第二步是从Frame派生一个Application类，这是所有Widget的父容器：
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLabel = Label(self, text='Hello, world!')
        self.helloLabel.pack()
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.pack()
        # 在GUI中，每个Button、Label、输入框等，都是一个Widget。Frame则是可以容纳其他Widget的Widget，所有的Widget组合起来就是一棵树。
        # pack()方法把Widget加入到父容器中，并实现布局。pack()是最简单的布局，grid()可以实现更复杂的布局。
        # 在createWidgets()方法中，我们创建一个Label和一个Button，当Button被点击时，触发self.quit()使程序退出。


class Application2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWigets()

    def createWigets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()

    # 加入一个文本框，让用户可以输入文本，然后点按钮后，弹出消息对话框。
    def hello(self):
        name = self.nameInput.get() or 'world'
        messagebox.showinfo('Message', 'hello, %s' % name)


if __name__ == '__main__':
    # # 第三步，实例化Application，并启动消息循环：
    # app = Application()
    # # 设置窗口标题:
    # app.master.title('Hello World')
    # # 主消息循环:
    # app.mainloop()

    app2 = Application2()
    app2.master.title('hello world')
    app2.mainloop()



