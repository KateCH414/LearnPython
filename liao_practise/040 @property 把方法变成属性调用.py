# --*-- coding:utf-8 --*--
# 在绑定属性时，如果我们直接把属性暴露出去，虽然写起来很简单，但是，没办法检查参数，导致可以把成绩随便改
#这显然不合逻辑。为了限制score的范围，可以通过一个set_score()方法来设置成绩，再通过一个get_score()来获取成绩，这样，在set_score()方法里，就可以检查参数：
#@property广泛应用在类的定义中，可以让调用者写出简短的代码，同时保证对参数进行必要的检查，这样，程序运行时就减少了出错的可能性。
class Student(object):

    def get_score(self):
         return self._score

    def set_score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

#上面的调用方法又略显复杂，没有直接用属性这么直接简单
#还记得装饰器（decorator）可以给函数动态加上功能吗？对于类的方法，装饰器一样起作用。Python内置的@property装饰器就是负责把一个方法变成属性调用的：

class Student2(object):
    # @property的实现比较复杂，我们先考察如何使用。把一个getter方法变成属性，只需要加上@property就可以了，
    # 此时，@property本身又创建了另一个装饰器@score.setter，负责把一个setter方法变成属性赋值，于是，我们就拥有一个可控的属性操作：
    @property
    def score(self):
        return self._score

    @score.setter
    def score(self, value):
        if not isinstance(value, int):
            raise ValueError('score must be an integer!')
        if value < 0 or value > 100:
            raise ValueError('score must between 0 ~ 100!')
        self._score = value

    # 还可以定义只读属性，只定义getter方法，不定义setter方法就是一个只读属性：
    # 上面的birth是可读写属性，而age就是一个只读属性，因为age可以根据birth和当前时间计算出来。
    @property
    def birth(self):
        return self._birth

    @birth.setter
    def birth(self, value):
        self._birth = value

    @property
    def age(self):
        return 2015 - self._birth
    # 要特别注意：属性的方法名不要和实例变量重名。方法名为score 实例变量为self._score
    # 方法名称和实例变量均为birth:
    #@property
    #def birth(self):
        #return self.birth

    # 这是因为调用s.birth时，首先转换为方法调用，在执行return
    # self.birth时，又视为访问self的属性，于是又转换为方法调用，造成无限递归，最终导致栈溢出报错RecursionError。







if __name__ == '__main__':
    #现在，对任意的Student实例进行操作，就不能随心所欲地设置score了：
    s = Student()
    s.set_score(60)  # ok!
    try:
        s.set_score(101) # ValueError: score must between 0 ~ 100!
    except ValueError as e:
        print(e.args)

    s2 = Student2()
    s2.score = 60 # OK，实际转化为s.set_score(60)
    print(s2.score)  # OK，实际转化为s.get_score()
    try:
        s2.score = 9999 # ValueError: score must between 0 ~ 100!
    except ValueError as e:
        print(e.args)




