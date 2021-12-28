# --*-- coding:utf-8 --*--
# 在磁盘上读写文件的功能都是由操作系统提供的，现代操作系统不允许普通的程序直接操作磁盘，
# 读写文件就是请求操作系统打开一个文件对象（通常称为文件描述符）
# 通过操作系统提供的接口从这个文件对象中读取数据（读文件），或者把数据写入这个文件对象（写文件）
# Python内置了读写文件的函数，用法和C是兼容的

# 读文件
# 第一步：打开文件
# 以读文件的模式打开一个文件对象,使用Python内置的open()函数，传入文件名和标示符:
f = open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r')
# 标示符'r'表示读
# 如果文件不存在，open()函数就会抛出一个IOError的错误，并且给出错误码和详细的信息告诉你文件不存在：
# FileNotFoundError: [Errno 2] No such file or directory: '/Users/michael/notfound.txt'

# 第二步：读文件
# 调用read()方法可以一次读取文件的全部内容，Python把内容读到内存，用一个str对象表示
str = f.read()

# 第三步：关闭文件
# 调用close()方法关闭文件。文件使用完毕后必须关闭，因为文件对象会占用操作系统的资源，并且操作系统同一时间能打开的文件数量也是有限的：
f.close()

# 由于文件读写时都有可能产生IOError，一旦出错，后面的f.close()就不会调用。所以，为了保证无论是否出错都能正确地关闭文件，我们可以使用try ... finally来实现：

try:
    f = open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r')
    str = f.read()
    print(str)
except IOError as e:
    print(e)
finally:
    if f:
        f.close()

# 每次都这么写实在太繁琐，所以，Python引入了with语句来自动帮我们调用close()方法：
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r') as f:
    print(f.read())

# read()会一次性读取文件的全部内容，如果文件有10G，内存就爆了
# 调用read(size)方法，每次最多读取size个字节的内容
# 调用readline()可以每次读取一行内容，
# 调用readlines()一次读取所有内容并按行返回list
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r') as f:
    for line in f.readlines():
        print(line.strip())  # 把末尾的'\n'删掉

# file-like Object
# open()函数返回的这种有个read()方法的对象，在Python中统称为file-like Object
# 除了file外，还可以是内存的字节流，网络流，自定义流等等。
# file-like Object不要求从特定类继承，只要写个read()方法就行。
# StringIO就是在内存中创建的file-like Object，常用作临时缓冲。

# 读二进制文件
# 前面讲的默认都是读取文本文件，并且是UTF-8编码的文本文件。要读取二进制文件，比如图片、视频等等，
# 用'rb'模式打开文件即可：
with open('/Users/huancui/project/Python_ch/python_test/picture/images.jpeg', 'rb') as f:
    f.read()  # b'\xff\xd8\xff\xe1\x00\x18Exif\x00\x00...' # 十六进制表示的字节

# 字符编码
# 读取非UTF-8编码的文本文件，需要给open()函数传入encoding参数
# 读取GBK编码的文件
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r', encoding='gbk') as f:
    f.read()
# 遇到有些编码不规范的文件，你可能会遇到UnicodeDecodeError，因为在文本文件中可能夹杂了一些非法编码的字符
# 遇到这种情况，open()函数还接收一个errors参数，表示如果遇到编码错误后如何处理。最简单的方式是直接忽略
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'r', encoding='gbk', errors='ignore') as f:
    f.read()


# 写文件
# 写文件和读文件是一样的，唯一区别是调用open()函数时，传入标识符'w'或者'wb'表示写文本文件或写二进制文件：
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'w'):
    f.write("Hello, world!")

# 当我们写文件时，操作系统往往不会立刻把数据写入磁盘，而是放到内存缓存起来，空闲的时候再慢慢写入。
# 只有调用close()方法时，操作系统才保证把没有写入的数据全部写入磁盘。忘记调用close()的后果是数据可能只写了一部分到磁盘，剩下的丢失了
# 所以，还是用with语句来得保险

# 要写入特定编码的文本文件，请给open()函数传入encoding参数，将字符串自动转换成指定编码
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'w', encoding='gbk'):
    f.write("Hello, world!")

# 细心的童鞋会发现，以'w'模式写入文件时，如果文件已存在，会直接覆盖（相当于删掉后新写入一个文件）。
# 如果我们希望追加到文件末尾怎么办？可以传入'a'以追加（append）模式写入
with open('/Users/huancui/project/Python_ch/python_test/cuihuan.py', 'a', encoding='gbk'):
    f.write("Hello, world!")

# 关于open()的mode参数：
#
# ‘r’：读
#
# ‘w’：写
#
# ‘a’：追加
#
# ‘r+’ == r+w（可读可写，文件若不存在就报错(IOError)）
#
# ‘w+’ == w+r（可读可写，文件若不存在就创建）
#
# ‘a+’ ==a+r（可追加可写，文件若不存在就创建）
#
# 对应的，如果是二进制文件，就都加一个b就好啦：
#
# ‘rb’　　‘wb’　　‘ab’　　‘rb+’　　‘wb+’　　‘ab+’

