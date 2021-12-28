# --*-- coding:utf-8 --*--

# 数据读写不一定是文件，也可以在内存中读写。

# StringIO:在内存中读写str
# 创建一个StringIO
from io import StringIO
f = StringIO()
# 把str写入StringIO
f.write("hello")
# getvalue()方法用于获得写入后的str
print(f.getvalue())
# 读取StringIO，可以用一个str初始化StringIO，然后，像读文件一样读取
f = StringIO('Hello!\nHi!\nGoodbye!')
while True:
    s = f.readline()
    if s == '':
        break
    print(s.strip())

# BytesIO:操作二进制数据
from io import BytesIO
f =  BytesIO
f.write('中文'.encode('utf-8'))  # 注意，写入的不是str，而是经过UTF-8编码的bytes。
print(f.getvalue())  # b'\xe4\xb8\xad\xe6\x96\x87'
# 可以用一个bytes初始化BytesIO，然后，像读文件一样读取
f = BytesIO(b'\xe4\xb8\xad\xe6\x96\x87')
print(f.read())
