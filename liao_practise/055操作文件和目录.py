# --*-- coding:utf-8 --*--

# 我们要操作文件、目录，可以在命令行下面输入操作系统提供的各种命令来完成。比如dir、cp等命令
# Python内置的os模块也可以直接调用操作系统提供的接口函数。

# os模块的基本功能
import os
import shutil

# 利用os模块编写一个能实现dir -l输出的程序。

# 编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
def searchpath(str, path = '.'):
    aimpath = []
    for x in os.listdir(path):
        if os.path.isdir(os.path.join(path, x)):
            aimpath.extend(searchpath(str, os.path.join(path, x)))
        if str in x and os.path.isfile(os.path.join(path, x)): # os.path.join 需要是基于当前路径的相对路径
            aimpath.append(os.path.join(path, x))
        else:
            continue
    return aimpath


if __name__ == '__main__':
    # 编写一个程序，能在当前目录以及当前目录的所有子目录下查找文件名包含指定字符串的文件，并打印出相对路径。
    print(searchpath('test'))


    # 操作系统类型
    print(os.name)  # posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统

    # 获取详细的系统信息，可以调用uname()函数：
    print(os.uname())
    # posix.uname_result(sysname='Darwin', nodename='MacBook-Pro.local', release='20.5.0', version='Darwin Kernel Version 20.5.0: Sat May  8 05:10:33 PDT 2021; root:xnu-7195.121.3~9/RELEASE_X86_64', machine='x86_64')
    # 注意uname()函数在Windows上不提供，也就是说，os模块的某些函数是跟操作系统相关的。

    # 环境变量
    # 操作系统中定义的环境变量，全部保存在os.environ这个变量中，可以直接查看：
    print(os.environ)
    # 获取某个环境变量的值，可以调用os.environ.get('key')：
    print(os.environ.get('PATH'))

    # 操作文件和目录
    # 操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下
    # 查看当前目录的绝对路径:
    print(os.path.abspath('.'))

    # 在某个目录下创建一个新目录
    # 首先把新目录的完整路径表示出来:
    os.path.join(os.path.abspath('.'), "newtest")
    # 然后创建一个目录:
    os.makedirs(os.path.join(os.path.abspath('.'), "newtest"))
    # 删除一个目录
    os.rmdir(os.path.join(os.path.abspath('.'), "newtest"))

    # 把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符
    print(os.path.join(os.path.abspath('.'), "newtest"))
    # 拆分路径时，要通过os.path.split()函数
    print(os.path.split(os.path.abspath('.')))
    # 得到文件扩展名
    print(os.path.splitext('/Users/huancui/project/Python_ch/python_test/picture/images.jpeg'))

    # 复制文件
    # 复制文件的函数居然在os模块中不存在,原因是复制文件并非由操作系统提供的系统调用,shutil模块提供了copyfile()的函数
    # 还可以在shutil模块中找到很多实用函数，它们可以看做是os模块的补充
    shutil.copy('/Users/huancui/project/Python_ch/python_test/picture/images.jpeg', '/Users/huancui/project/Python_ch/python_test/picture/copy_images.jpeg')
    # 对文件重命名:
    os.rename('/Users/huancui/project/Python_ch/python_test/picture/copy_images.jpeg', '/Users/huancui/project/Python_ch/python_test/picture/images.jpg')
    # 删除文件
    os.remove('/Users/huancui/project/Python_ch/python_test/picture/images.jpg')

    # 列出当前目录下的所有目录
    dirlist = [x for x in os.listdir('.') if os.path.isdir(x)]
    print(dirlist)

    # 列出所有的.py文件，也只需一行代码
    pyfiles = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1] == '.py']
    print(pyfiles)
















