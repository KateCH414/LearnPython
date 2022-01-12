# --*--coding:utf-8--*--
# datetime是Python处理日期和时间的标准库
# 注意到datetime是模块，datetime模块还包含一个datetime类
from datetime import datetime
from datetime import timedelta
from datetime import timezone
import re
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
    # 不过需要导入timedelta这个类 from datetime import timedelta
    print(now + timedelta(hours=10))  # 当前时间向后推10个小时 2021-12-29 03:31:11.341913
    print(now - timedelta(days=1))   # 当前时间往前推1天  2021-12-27 17:31:11.341913

    # 本地时间转换为UTC时间
    # 本地时间是指系统设定时区的时间，例如北京时间是UTC+8:00时区的时间，而UTC时间指UTC+0:00时区的时间。
    # datetime类型有一个时区属性tzinfo，但是默认为None，所以无法区分这个datetime到底是哪个时区，
    # 但是可以强行给datetime设置一个时区：
    # from datetime import timezone
    tz_utc_8 = timezone(timedelta(hours=8))  # 创建时区UTC+8:00
    dt_n = now.replace(tzinfo=tz_utc_8)  # 强制设置为UTC+8:00  # 系统时区恰好是UTC+8:00，才可以设置，否则，不能强制设置为UTC+8:00时区
    print(dt_n) # 2021-12-28 17:43:47.438007+08:00

    # 时区转换
    # 我们可以先通过utcnow()拿到当前的UTC时间，再转换为任意时区的时间
    # # 拿到UTC时间，并强制设置时区为UTC+0:00:
    utc_dt = datetime.utcnow().replace(tzinfo=timezone.utc)
    print(utc_dt)  # 2021-12-28 09:47:01.411120+00:00
    # astimezone()将转换时区为北京时间:
    bj_dt = utc_dt.astimezone(timezone(timedelta(hours=8)))
    print(bj_dt)  # 2021-12-28 17:48:57.884370+08:00

    # astimezone()将转换时区为东京时间:
    okyo_dt = utc_dt.astimezone(timezone(timedelta(hours=9)))
    print(okyo_dt)  # 2021-12-28 19:16:10.411324+09:00

    # astimezone()将bj_dt转换时区为东京时间
    tokyo_dt2 = bj_dt.astimezone(timezone(timedelta(hours=9)))
    print(tokyo_dt2)  # 2021-12-28 19:16:10.411324+09:00


    # 练习：假设你获取了用户输入的日期和时间如2015-1-21 9:01:30，以及一个时区信息如UTC+5:00，均是str，请编写一个函数将其转换为timestamp：
    def to_timestamp(dt_str, tz_str):
        tz = 0
        User_tz = re.match(r'UTC([+|-][\d]{1,2}):00', tz_str)
        if User_tz:
            tz = int(User_tz.group(1))
        dt = datetime.strptime(dt_str, '%Y-%m-%d %H:%M:%S')
        print(dt)
        user_dt = dt.replace(tzinfo=timezone(timedelta(hours=tz)))
        print("to_timestamp")
        print(user_dt)
        return user_dt.timestamp()


    t1 = to_timestamp('2015-6-1 08:10:30', 'UTC+7:00')
    print("t1:")
    print(t1)
    assert t1 == 1433121030.0
    t2 = to_timestamp('2015-5-31 16:10:30', 'UTC-09:00')
    print("t2:")
    print(t2)
    assert t2 == 1433121030.0

    print('ok')








