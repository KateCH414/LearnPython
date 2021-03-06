# --*-- coding:utf-8 --*--
"""
策略模式
大多数问题都可以使用多种方法来解决。通常来说，没有公认最适合所有场景的算法。
一些不同的评判标准能帮助我们为不同的场景选择不同的排序算法，其中应该考虑的有以下几个：
1：需要排序的元素数量：
    这被称为输入大小。当输入较少时，几乎所有排序算法的表现都很好，但对于大量输入，只有部分算法具有不错的性能。
2：算法的最佳/平均/最差时间复杂度
    时间复杂度是算法运行完成所花费的（大致）时间长短，不考虑系数和低阶项 ① 。这是选择算法的最常见标准，但这个标准并不总是那么充分。
3：算法的空间复杂度
    空间复杂度是充分地运行一个算法所需要的（大致）物理内存量。在我们处理大数据或在嵌入式系统（通常内存有限）中工作时，这个因素非常重要。
4：算法的稳定性
    在执行一个排序算法之后，如果能保持相等值元素原来的先后相对次序，则认为它是稳定的。
5：算法的代码实现复杂度
    如果两个算法具有相同的时间/空间复杂度，并且都是稳定的，那么知道哪个算法更易于编码实现和维护也是很重要的。

策略模式（Strategy pattern）鼓励使用多种算法来解决一个问题，
其杀手级特性是能够在运行时透明地切换算法（客户端代码对变化无感知）
"""
"""
软件中的例子
Python 的 sorted() 和 list.sort() 函数是策略模式的例子。
两个函数都接受一个命名参数 key，这个参数本质上是实现了一个排序策略的函数的名称

pprint 模块用于美化输出一个数据结构
attrgetter 用于通过属性名访问 class 或 namedtuple 的属性
也可以使用一个 lambda 函数来替代使用 attrgetter，但作者觉得 attrgetter 的可读性更高。

import pprint
from collections import namedtuple
from operator import attrgetter
if __name__ == '__main__':
    ProgrammingLang = namedtuple('ProgrammingLang', 'name ranking')
    stats = (('Ruby', 14), ('Javascript', 8), ('Python', 7),
             ('Scala', 31), ('Swift', 18), ('Lisp', 23))
    lang_stats = [ProgrammingLang(n, r) for n, r in stats]
    pp = pprint.PrettyPrinter(indent=5)
    pp.pprint(sorted(lang_stats, key=attrgetter('name')))
    print()
    pp.pprint(sorted(lang_stats, key=attrgetter('ranking')))
"""
"""
在函数非一等公民的语言中，每个策略都要用一个不同的类来实现。
在 Python 中，我们可以把函数看作是普通的变量，这就简化了策略模式的实现。

假设我们要实现一个算法来检测在一个字符串中是否所有字符都是唯一的。
"""
import time
SLOW = 3  # 单位秒
LIMIT = 5  # 字符数
WARNING = 'too bad, you picked the slow algorithm :('

# 算法一的子方法，返回所有相邻字符对的一个序列 seq
def pairs(seq):
    n = len(seq)
    for i in range(n):
        yield seq[i], seq[(i + 1) % n]

# 算法一， 它接收一个字符串参数 s, 如果该字符串中所有字符都是唯一的，则返回 True
def allUniqueSort(s):
    if len(s) > LIMIT:   # 假设该算法在大于 LIMIT 个字符时效率低
        print(WARNING)
        time.sleep(SLOW)

    strStr = sorted(s)
    for(c1, c2) in pairs(strStr):
        if c1 == c2:
            return False
    return True

# 算法二
def allUniqueSet(s):
    if len(s) < LIMIT:
        print(WARNING)
        time.sleep(SLOW)    # 假设该算法在小于 LIMIT 个字符时效率低
    return True if len(set(s)) == len(s) else False

# 接受一个输入字符串 s 和一个策略函数 strategy
def allUnique(s, strategy):
    return strategy(s)

# 输入待检字符唯一性的单词，选择要使用的策略
def main():
    while True:
        word = None
        while not word:
            word = input('Insert word (type quit to exit)> ')
            if word == 'quit':
                print('bye')
                return

            strategy_picked = None
            strategies = {'1': allUniqueSet, '2': allUniqueSort}
            while strategy_picked not in strategies.keys():
                strategy_picked = input("Choose strategy: [1] Use a set, [2] Sort and pair>")

                try:
                    strategy = strategies[strategy_picked]
                    print('allUnique({}): {}'.format(word, allUnique(word, strategy)))
                except KeyError as err:
                    print('Incorrect option: {}'.format(strategy_picked))


if __name__ == "__main__":
    main()


"""
总结 
通常，我们想要使用的策略不应该由用户来选择。策略模式的要点是可以透明地使用不同的算法。
我们的代码有两种常见用户。
一种是最终用户，他们不应该关心代码中发生的事情
另一类用户是其他开发人员

假设我们想创建一个供其他开发人员使用的 API。如何做到让他们不用关心策略模式
一个提示是考虑在一个公用类（例如，AllUnique）中封装两个函数
这样，其他开发人员只需要创建一个 AllUnique 类实例，并执行单个方法，例如 test()。
"""

