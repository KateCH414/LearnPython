# --*-- coding:utf-8 --*--
"""
命令设计模式帮助我们将一个操作（撤销、重做、复制、粘贴等）封装成一个对象。
简而言之，这意味着创建一个类，包含实现该操作所需要的所有逻辑和方法。
这样做的优势如下所述：
1: 我们并不需要直接执行一个命令。命令可以按照希望执行。
2: 调用命令的对象与知道如何执行命令的对象解耦。调用者无需知道命令的任何实现细节。
3: 如果有意义，可以把多个命令组织起来，这样调用者能够按顺序执行它们。
    例如，在实现一个多层撤销命令时，这是很有用的
"""
"""
例子
PyQt 是 QT 工具包的 Python 绑定。
PyQt 包含一个 QAction 类，将一个动作建模为一个命令。
对每个动作都支持额外的可选信息， 比如， 描述、工具提示、快捷键和其他。
"""
"""
应用场景：
许多开发人员以为撤销例子是命令模式的唯一应用案例。
撤销操作确实是命令模式的杀手级特性，然而命令模式能做的实际上还有很多
1：GUI 按钮和菜单项：前面提过的 PyQt 例子使用命令模式来实现按钮和菜单项上的动作。
2：其他操作：除了撤销，命令模式可用于实现任何操作。其中一些例子包括剪切、复制、粘贴、重做和文本大写。
3：事务型行为和日志记录：事务型行为和日志记录对于为变更记录一份持久化日志是很重要的。
  操作系统用它来从系统崩溃中恢复，关系型数据库用它来实现事务，文件系统用它来实现快照，而安装程序（向导程序）用它来恢复取消的安装
4：宏：在这里，宏是指一个动作序列，可在任意时间点按要求进行录制和执行。
    流行的编辑器（比如，Emacs 和 Vim）都支持宏。
"""
"""
简单例子实现
我们将使用命令模式实现最基本的文件操作工具：
1：创建一个文件，并随意写入一个字符串
2：读取一个文件的内容
3：重命名一个文件
4：删除一个文件
下面实现的创建文件和重命名文件支持撤销，删除文件不支持。但对于文件删除操作实际上是可以实现撤销的，
一种技术是使用一个特殊的垃圾箱/废物篓目录来存储所有被删除文件，这样在用户请求时可以恢复出来。
"""
import os

verbose = True  # 全局设定，默认提供详细交互信息

# 重命名文件，包含撤销操作
class RenameFile:
    def __init__(self, path_src, path_dest):
        self.src, self.dest = path_src, path_dest

    def execute(self):
        if verbose:
            print("[renaming '{}' to '{}']".format(self.src, self.dest))
        os.rename(self.src, self.dest)

    def undo(self):
        if verbose:
            print("[renaming '{}' back to '{}']".format(self.dest, self.src))
        os.rename(self.dest, self.src)

# 创建文件，包含撤销操作
class CreateFile:
    def __init__(self, path, text='hello world\n'):
        self.path, self.text = path, text

    def execute(self):
        if verbose:
            print("[creating file '{}']".format(self.path))
        with open(self.path, mode='w', encoding='utf-8') as out_file:
            out_file.write(self.text)

    def undo(self):
        delete_file(self.path)

# 读取文件内容，没有撤销操作
class ReadFile:
    def __init__(self, path):
        self.path = path
    def execute(self):
        if verbose:
            print("[reading file '{}']".format(self.path))
        with open(self.path, mode='r', encoding='utf-8') as in_file:
            print(in_file.read(), end='')

# 删除文件，没有撤销操作
def delete_file(path):
    if verbose:
        print("deleting file '{}'".format(path))
        os.remove(path)


def main():
    orig_name, new_name = 'file1', 'file2'

    commands = []
    for cmd in CreateFile(orig_name), ReadFile(orig_name), RenameFile(orig_name, new_name):
        commands.append(cmd)

    [c.execute() for c in commands]

    answer = input('reverse the executed commands? [y/n]')

    if answer not in 'yY':
        print("the result is {}".format(new_name))
        exit()

    for c in reversed(commands):
        try:
            c.undo()
        except AttributeError as e:  # 这里依赖于异常处理，并不合适
            pass


if __name__ == '__main__':
    main()

# 文件创建功能能使用默认文件权限来创建文件，默认文件权限具体什么样由文件系统决定


"""
总结
命令模式：这种设计模式，可以将一个操作（比如，复制/粘贴）封装为一个对象。
这样能提供很多好处，如下所述：
1：我们可以在任何时候执行一个命令，而并不一定是在命令创建时。 
2：执行一个命令的客户端代码并不需要知道命令的任何实现细节。
3：可以对命令进行分组，并按一定的顺序执行。

一般而言，要在运行时按照用户意愿执行的任何操作都适合使用命令模式。命令模式也适用于组合多个命令
这有助于实现宏、多级撤销以及事务。一个事务应该：要么成功，这意味着事务中所有操作应该都成功（提交操作）
要么如果至少一个操作失败，则全部失败（回滚操作）
如果希望进一步使用命令模式，可以实现一个例子，涉及将多个命令组合成一个事务。
"""

