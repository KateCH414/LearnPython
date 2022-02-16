# --*-- coding:utf-8 --*--
"""
python2.x range() 函数可创建一个整数列表，一般用在 for 循环中。
注意：Python3 range() 返回的是一个可迭代对象（类型是对象），而不是列表类型， 所以打印的时候不会打印列表，具体可查阅 Python3 range() 用法说明。

语法
    range(start, stop[, step])
参数说明
    start: 计数从 start 开始。默认是从 0 开始。例如range（5）等价于range（0， 5）;
    stop: 计数到 stop 结束，但不包括 stop。例如：range（0， 5） 是[0, 1, 2, 3, 4]没有5
    step：步长，默认为1。例如：range（0， 5） 等价于 range(0, 5, 1)
"""
print(range(10))      # 从 0 开始到 9 [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

print(range(1, 11))    # 从 1 开始到 10 [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

print(range(0, 30, 5))  # 步长为 5 [0, 5, 10, 15, 20, 25]

print(range(0, -10, -1))  # 负数[0, -1, -2, -3, -4, -5, -6, -7, -8, -9]

range(0)  # []
range(1, 0)  # []

x = 'sadhai'
for i in range(len(x)):
    print(x[i])


