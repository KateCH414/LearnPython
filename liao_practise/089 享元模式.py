# --*-- coding:utf-8 --*--
"""
享元模式
由于对象创建的开销，面向对象的系统可能会面临性能问题。性能问题通常在资源受限的嵌入式系统中出现，比如智能手机和平板电脑。大型复杂系统中也可能会出现同样的问题，因为要在其中创建大量对象（也可能是用户），这些对象需要同时并存
当我们创建一个新对象时，需要分配额外的内存。虽然虚拟内存理论上为我们提供了无限制的内存空间，但现实却并非如此。如果一个系统耗尽了所有的物理内存，就会开始将内存页替换到二级存储设备，通常是硬盘驱动器（Hard Disk Drive，HDD）。在多数情况下，由于内存和硬盘之间的性能差异，这是不能接受的。固态硬盘（Solid State Drive， SSD）的性能一般比硬盘更好，但并非人人都使用 SSD。
除内存使用之外，计算性能也是一个考虑点。图形软件，包括计算机游戏，应该能够极快地渲染 3D 信息（例如，有成千上万棵树的森林或满是士兵的村庄）。如果一个3D地带的每个对象都是单独创建，未使用数据共享，那么性能将是无法接受的

享元设计模式通过为相似对象引入数据共享来最小化内存使用，提升性能

一个享元（Flyweight）就是一个包含状态独立的不可变（又称固有的）数据的共享对象。
依赖状态的可变（又称非固有的）数据不应是享元的一部分，因为每个对象的这种信息都不同， 无法共享。
如果享元需要非固有的数据， 应该由客户端代码显式地提供。
"""
"""
应用场景
享元旨在优化性能和内存使用。所有嵌入式系统（手机、平板电脑、游戏终端和微控制器等）和性能关键的应用（游戏、3D 图形处理和实时系统等）都能从其获益。
若想要享元模式有效，需要满足 GoF 的《设计模式》一书罗列的以下几个条件。
1： 应用需要使用大量的对象
2：对象太多，存储/渲染它们的代价太大。一旦移除对象中的可变状态（因为在需要之时，应该由客户端代码显式地传递给享元），多组不同的对象可被相对更少的共享对象所替代。 
3：对象 ID 对于应用不重要。对象共享会造成 ID 比较的失败，所以不能依赖对象 ID（那些在客户端代码看来不同的对象，最终具有相同的 ID）。
"""
"""
稍稍解释一下 memoization 与享元模式之间的区别。memoization 是一种优化技术， 使用一个缓存来避免重复计算那些在更早的执行步骤中已经计算好的结果。
memoization 并不是只能应用于某种特定的编程方式， 比如面向对象编程（Object-Oriented Programming，OOP）
在 Python 中，memoization 可以应用于方法和简单的函数

享元则是一种特定于面向对象编程优化的设计模式，关注的是共享对象数据。
"""
"""
在 Python 中，享元可以以多种方式实现。
Python 规范并没有要求 id() 返回对象的内存地址， 只是要求 id() 为每个对象返回一个唯一性 ID，
 不过 CPython（Python 的官方实现）正好使用对象的内存地址作为对象唯一性 ID。
"""
# demo
import random
from  enum import Enum
TreeType = Enum('TreeType', 'apple_tree cherry_tree peach_tree')

# 产品类
class Tree:
    # pool 变量是一个对象池（缓存)，类属性
    pool = dict()

    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type, None)
        if not obj:
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj

    # 用于在屏幕上渲染一棵树（即享元不知道的所有可变信息都由客户端通过参数显式传递）
    def render(self, age, x, y):
        print('render a tree of type {} and age {} at ({}, {}) '.format(self.tree_type, age, x, y))


def main():
    # 以下仅分配了 3 棵树的内存
    rnd = random.Random()
    age_min, age_max = 1, 30  # 单位为年
    min_point, max_point = 0, 100
    tree_counter = 0
    for _ in range(10):
        t1 = Tree(TreeType.apple_tree)
        t1.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    for _ in range(3):
        t2 = Tree(TreeType.cherry_tree)
        t2.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    for _ in range(5):
        t3 = Tree(TreeType.peach_tree)
        t3.render(rnd.randint(age_min, age_max),
                  rnd.randint(min_point, max_point),
                  rnd.randint(min_point, max_point))
        tree_counter += 1

    print('trees rendered: {}'.format(tree_counter))
    print('trees actually created: {}'.format(len(Tree.pool)))

    t4 = Tree(TreeType.cherry_tree)
    t5 = Tree(TreeType.cherry_tree)
    t6 = Tree(TreeType.apple_tree)

    print('{} == {}? {}'.format(id(t4), id(t5), id(t4) == id(t5)))  # True
    print('{} == {}? {}'.format(id(t5), id(t6), id(t5) == id(t6)))  # False

if __name__ == '__main__':
    main()

"""
总结：
基于 GTK+ 的 Exaile 音乐播放器使用享元来避免对象复制，Peppy 文本编辑器则使用享元来共享状态栏的属性。
一般来说，在应用需要创建大量的计算代价大但共享许多属性的对象时，可以使用享元。
重点在于将不可变（可共享）的属性与可变的属性区分开。
"""



