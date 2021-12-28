# --*-- coding:utf-8 --*--

# “测试驱动开发”（TDD：Test-Driven Development）
# 单元测试是用来对一个模块、一个函数或者一个类来进行正确性检验的测试工作。

# 比如对函数abs()，我们可以编写出以下几个测试用例：
# 输入正数，比如1、1.2、0.99，期待返回值与输入相同；
# 输入负数，比如-1、-1.2、-0.99，期待返回值与输入相反；
# 输入0，期待返回0；
# 输入非数值类型，比如None、[]、{}，期待抛出TypeError。
# 把上面的测试用例放到一个测试模块里，就是一个完整的单元测试。
# 如果单元测试通过，说明我们测试的这个函数能够正常工作。如果单元测试不通过，要么函数有bug，要么测试条件输入不正确，总之，需要修复使单元测试能够通过。
# 单元测试通过后有什么意义呢？
# 如果我们对abs()函数代码做了修改，只需要再跑一遍单元测试，如果通过，说明我们的修改不会对abs()函数原有的行为造成影响，
# 如果测试不通过，说明我们的修改与原有行为不一致，要么修改代码，要么修改测试。
# 以测试为驱动的开发模式最大的好处：确保一个程序模块的行为符合我们设计的测试用例。在将来修改的时候，可以极大程度地保证该模块行为仍然是正确的。

# 单元测试实践
# 我们来编写一个Dict类，这个类的行为和dict一致，但是可以通过属性来访问，用起来就像下面这样：

class MyDict(dict):

    def __init__(self, **kw):
        super().__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


if __name__ == '__main__':
    d = MyDict(a=1, b=2)
    print(d['a'])
    print(d.a)

# 编写单元测试，我们需要引入Python自带的unittest模块，编写mydict_test.py如下：
import unittest

class TestDict(unittest.TestCase):
    # 编写单元测试时，我们需要编写一个测试类，从unittest.TestCase继承。

    # 以test开头的方法就是测试方法，不以test开头的方法不被认为是测试方法，测试的时候不会被执行
    def test_init(self):
        d = MyDict(a=1, b='test')
        self.assertEqual(d.a, 1)
        # 由于unittest.TestCase提供了很多内置的条件判断，我们只需要调用这些方法就可以断言输出是否是我们所期望的。最常用的断言就是assertEqual()
        self.assertEqual(d.b, 'test')
        self.assertTrue(isinstance(d, dict))

    def test_key(self):
        d = MyDict()
        d['key'] = 'value'
        self.assertEqual(d.key, 'value')

    def test_attr(self):
        d = MyDict()
        d.key = 'value'
        self.assertTrue('key' in d)
        self.assertEqual(d['key'], 'value')

    def test_keyerror(self):
        d = MyDict()
        # 另一种重要的断言就是期待抛出指定类型的Error
        # 比如通过d['empty']访问不存在的key时，断言会抛出KeyError
        with self.assertRaises(KeyError):
            value = d['empty']

    def test_attrerror(self):
        d = MyDict()
        with self.assertRaises(AttributeError):
            value = d.empty


# 运行单元测试
# 第一种 做正常的python脚本
# $ python mydict_test.py

# 第二种
# if __name__ == '__main__':
#     unittest.main()

# 第三种 命令行通过参数-m unittest直接运行单元测试
# python -m unittest mydict_test

# setUp与tearDown
# 单元测试中编写两个特殊的setUp()和tearDown()方法。这两个方法会分别在每调用一个测试方法的前后分别被执行。
# setUp()和tearDown()方法有什么用呢？设想你的测试需要启动一个数据库，
# 这时，就可以在setUp()方法中连接数据库，在tearDown()方法中关闭数据库，这样，不必在每个测试方法中重复相同的代码：
class TestDict(unittest.TestCase):

    def setUp(self):
        print('setUp...')

    def tearDown(self):
        print('tearDown...')


class Student(object):
    def __init__(self, name, score):
        self.name = name

        self.score = score

    def get_grade(self):
        if self.score < 0 or self.score > 100:
            raise ValueError('input error!')
        if self.score >= 80:
            return 'A'
        if self.score >= 60:
            return 'B'

        return 'C'

class TestStudent(unittest.TestCase):

    def test_80_to_100(self):
        s1 = Student('Bart', 80)
        s2 = Student('Lisa', 100)
        self.assertEqual(s1.get_grade(), 'A')
        self.assertEqual(s2.get_grade(), 'A')

    def test_60_to_80(self):
        s1 = Student('Bart', 60)
        s2 = Student('Lisa', 79)
        self.assertEqual(s1.get_grade(), 'B')
        self.assertEqual(s2.get_grade(), 'B')

    def test_0_to_60(self):
        s1 = Student('Bart', 0)
        s2 = Student('Lisa', 59)
        self.assertEqual(s1.get_grade(), 'C')
        self.assertEqual(s2.get_grade(), 'C')

    def test_invalid(self):
        s1 = Student('Bart', -1)
        s2 = Student('Lisa', 101)
        with self.assertRaises(ValueError):
            s1.get_grade()
        with self.assertRaises(ValueError):
            s2.get_grade()










