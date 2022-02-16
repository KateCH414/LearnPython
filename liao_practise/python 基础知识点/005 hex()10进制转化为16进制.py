# --*-- coding:utf-8 --*--
"""
hex() 函数用于将10进制整数转换成16进制，以字符串形式表示。
hex 语法：
    hex(x)
参数说明
    x -- 10进制整数
返回值
返回16进制数，以字符串形式表示。

hex 的使用方法：如下
"""
print(hex(255))  # '0xff'
print(hex(-42))  # '-0x2a'
print(type(hex(12)))  # <class 'str'>      # 字符串
