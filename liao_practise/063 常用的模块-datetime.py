# --*--coding:utf-8--*--
# datetime是Python处理日期和时间的标准库
# 注意到datetime是模块，datetime模块还包含一个datetime类
from datetime import datetime
from datetime import timedelta


if __name__ == '__main__':
    # 获取当前日期和时间
    now = datetime.now()  # datetime.now()返回当前日期和时间，其类型是datetime
    print(now)  # 2021-12-28 17:14:05.267045
    print(type(now))  # <class 'datetime.datetime'>

    # 获取指定日期和时间
    dt = datetime(2021, 4, 19, 12, 20)  # 用指定日期时间创建datetime
    print(dt)  # 2021-04-19 12:20:00
    print(type(dt))  # <class 'datetime.datetime'>

    # datetime转换为timestamp
    # 在计算机中，时间实际上是用数字表示的
    # 我们把1970年1月1日 00:00:00 UTC+00:00时区的时刻称为epoch time，记为0（1970年以前的时间timestamp为负数），
    # 当前时间就是相对于epoch time的秒数，称为timestamp
    # timestamp的值与时区毫无关系，
    # 因为timestamp一旦确定，其UTC时间就确定了，转换到任意时区的时间也是完全确定的，
    # 这就是为什么计算机存储的当前时间是以timestamp表示的，因为全球各地的计算机在任意时刻的timestamp都是完全相同的（假定时间已校准）。
    dt_tt = dt.timestamp()  # 把datetime转换为timestamp
    print(dt_tt)  # 1618806000.0 Python的timestamp是一个浮点数，整数位表示秒
    print(type(dt_tt))  # <class 'float'>
    # 某些编程语言（如Java和JavaScript）的timestamp使用整数表示毫秒数，这种情况下只需要把timestamp除以1000就得到Python的浮点表示方法。

    # timestamp转换为datetime
    print(datetime.fromtimestamp(dt_tt))  # 2021-04-19 12:20:00

    # 注意到timestamp是一个浮点数，它没有时区的概念，而datetime是有时区的
    # 上述转换是在timestamp和本地时间做转换。本地时间是指当前操作系统设定的时区
    # timestamp也可以直接被转换到UTC标准时区的时间
    print(datetime.fromtimestamp(dt_tt))  # 本地时间
    print(datetime.utcfromtimestamp(dt_tt))  # UTC时间

    # str转换为datetime
    cday = datetime.strptime('2021-6-1 18:19:59', '%Y-%m-%d %H:%M:%S')
    print(cday)  # 2021-06-01 18:19:59
    # 字符串'%Y-%m-%d %H:%M:%S'规定了日期和时间部分的格式。详细的说明请参考
    # Python文档：https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
    # 注意转换后的datetime是没有时区信息的

    # datetime转换为str
    print(now.strftime('%a, %b %d %H:%M'))  # Tue, Dec 28 17:25 格式可以根据规则自定义

    # datetime加减
    # 对日期和时间进行加减实际上就是把datetime往后或往前计算，得到新的datetime。加减可以直接用+和-运算符，
    # 不过需要导入timedelta这个类
    print(now + timedelta(hours=10))  # 当前时间向后推10个小时 2021-12-29 03:31:11.341913
    print(now - timedelta(days=1))   # 当前时间往前推1天  2021-12-27 17:31:11.341913







