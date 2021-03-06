# --*-- coding:utf-8 --*--
"""
模版模式
编写优秀代码的一个要素是避免冗余。在面向对象编程中，方法和函数是我们用来避免编写冗余代码的重要工具。

sorted() 这样的函数属于理想的案例
现实中，我们没法始终写出 100% 通用的代码。许多算法都有一些（但并非全部）通用步骤
广度优先搜索（Breadth-First Search，BFS）深度优先搜索（Depth-First Search，DFS）是其中不错的例子，
这两个流行的算法应用于图搜索问题

我们提出独立实现两个算法，函数 bfs() 和 dfs()
在 start 和 end 之间存在一条路径时返回一个元组 (True, path)；
如果路径不存在，则返回 (False, path)（此时， path 为空）。
"""
def bfs(graph, start, end):
    path = []
    visited = [start]
    while visited:
        current = visited.pop(0)
        if current not in path:
            path.append(current)
            if current == end:
                print(path)
                return (True, path)
            if current not in graph:
                continue
        visited = visited + graph[current]  # 仅有该行不同
    return (False, path)

def dfs(graph, start, end):
    path = []
    visited = [start]
    while visited:
        current = visited.pop(0)
        if current not in path:
            path.append(current)
            if current == end:
                print(path)
                return (True, path)
                # 两个顶点不相连，则跳过
            if current not in graph:
                continue
        visited = graph[current] + visited  # 仅有该行不同
    return (False, path)

"""
使用列表的字典结构来表示这个有向图
每个城市是字典中的一个键，列表的内容是从该城市始发的所有可能目的地
叶子顶点的城市（例如，Erfurt）使用一个空列表即可（无目的地）。
"""

def main():
    graph = {
        'Frankfurt': ['Mannheim', 'Wurzburg', 'Kassel'],
        'Mannheim': ['Karlsruhe'],
        'Karlsruhe': ['Augsburg'],
        'Augsburg': ['Munchen'],
        'Wurzburg': ['Erfurt', 'Nurnberg'],
        'Nurnberg': ['Stuttgart', 'Munchen'],
        'Kassel': ['Munchen'],
        'Erfurt': [],
        'Stuttgart': [],
        'Munchen': []
    }

    bfs_path = bfs(graph, 'Frankfurt', 'Nurnberg')
    dfs_path = dfs(graph, 'Frankfurt', 'Nurnberg')

    print('bfs Frankfurt-Nurnberg: {}'.format(bfs_path[1] if bfs_path[0] else 'Not found'))
    print('dfs Frankfurt-Nurnberg: {}'.format(dfs_path[1] if dfs_path[0] else 'Not found'))

    bfs_nopath = bfs(graph, 'Wurzburg', 'Kassel')
    print('bfs Wurzburg-Kassel: {}'.format(bfs_nopath[1] if bfs_nopath[0] else 'Not found'))

    dfs_nopath = dfs(graph, 'Wurzburg', 'Kassel')
    print('dfs Wurzburg-Kassel: {}'.format(dfs_nopath[1] if dfs_nopath[0] else 'Not found'))


"""
从性质来看，结果并不能表明什么，因为 DFS 和 BFS 不能很好地处理加权图（权重完全被忽略了）
处理加权图更好的算法是（Dijkstra 的）最短路径优先算法、Bellman-Ford 算法和 A* 算法等。

模板设计模式（Template design pattern），这个模式关注的是消除代码冗余，
其思想是我们应该无需改变算法结构就能重新定义一个算法的某些部分。为了避免重复而进行必要的重构之后，
我们来看看代码会变成什么样子：
"""

def traverse(graph, start, end, action):
    path = []
    visited = [start]
    while visited:
        current = visited.pop(0)
        if current not in path:
            path.append(current)
            if current == end:
                return (True, path)

            # 两个顶点不相连，则跳过
            if current not in graph:
                continue
        visited = action(visited, graph[current])  # 调用区别函数

    return (False, path)

# 区别部分
def extend_bfs_path(visited, current):
    return visited + current

def extend_dfs_path(visited, current):
    return current + visited


# 还有一种不推荐的方案
def traverse2(graph, start, end, algorithm):
    path = []
    visited = [start]
    while visited:
        current = visited.pop(0)
        if current not in path:
            path.append(current)
            if current == end:
                return (True, path)
            # 顶点不相连，则跳过
            if current not in graph:
                continue
        if algorithm == "BFS":    # 通过 if-else 实现
            visited = extend_bfs_path(visited, graph[current])
        elif algorithm == "DFS":
            visited = extend_dfs_path(visited, graph[current])
        else:
            raise ValueError("No such algorithm")
    return (False, path)

"""
不推荐理由如下
1：它使得 traverse() 难以维护。如果添加第三种方式来延伸路径，就需要扩展 traverse() 的代码，
   再添加一个条件来检测是否使用新的路径延伸动作。
   更好的方案是 traverse() 能发挥作用却好像根本不知道应该执行哪个 action，
   因为这样在 traverse() 中不要求什么特殊逻辑。
2：它仅对只有一行区别的算法有效。
   如果存在更多区别，那么与让本应归属 action 的具体细节污染 traverse() 函数相比，创建一个新函数会好得多。

3：它使得 traverse() 更慢。这是因为每次 traverse() 执行时，都需要显式地检测应该执行哪个遍历函数。
"""

"""
软件的例子
Python 在 cmd 模块中使用了模板模式，该模块用于构建面向行的命令解释器
cmd.Cmd.cmdloop() 实现了一个算法，持续地读取输入命令并将命令分发到动作方法。
每次循环之前、之后做的事情以及命令解析部分始终是相同的。这也称为一个算法的不变部分。
变化的是实际的动作方法（易变的部分）。

Python 的 asyncore 模块也使用了模板模式，该模块用于实现异步套接字服务客户端/服务器
其中诸如 asyncore.dispatcher.handle_connect_event 和 asyncore.dispatcher. handle_write_event() 之类的方法仅包含通用代码。
要执行特定于套接字的代码，这两个方法会执行 handle_connect() 方法。注意，执行的是一个特定于套接字的 handle_connect()， 
不是 asyncore.dispatcher.handle_connect()。后者仅包含一条警告。可以使用 inspect 模块来查看

>>> python3
import inspect
import asyncore
inspect.getsource(asyncore.dispatcher.handle_connect)
" def handle_connect(self):\n self.log_info('unhandled connect event', 'warning')\n"

"""

"""
demo
实现一个横幅生成器
将一段文本发送给一个函数，该函数要生成一个包含该文本的横幅
横幅有多种风格，比如点或虚线围绕文本。
横幅生成器有一个默认风格，但应该能够使用我们自己提供的风格。
"""
from cowpy import cow

# 风格 1
def dots_style(msg):
    msg = msg.capitalize()
    msg = '.' * 10 + msg + '.' * 10
    return msg

# 风格 2
def admire_style(msg):
    msg = msg.upper()
    return '!'.join(msg)

# 风格 3，使用 cowpy 模块生成随机 ASCII 码艺术字符，夸张地表现文本
def cow_style(msg):
    msg = cow.milk_random_cow(msg)
    return msg

# 模板函数，参数为：横幅包含文本、希望使用的风格
def generate_banner(msg, style=dots_style):
    print("-- start of banner --")
    print(style(msg))
    print('-- end of banner --\n\n')

def main2():
    msg = 'happy coding'
    [generate_banner(msg, style) for style in (dots_style, admire_style, cow_style)]

if __name__ == '__main__':
    main()
    main2()

"""
总结：
在实现结构相近的算法时，可以使用模板模式来消除冗余代码。
具体实现方式是使用动作/钩子方法/函数来完成代码重复的消除，
它们是 Python 中的一等公民。
"""




