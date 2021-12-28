# --*-- coding：utf-8 --*--

# 正常情况下，当我们定义了一个class，创建了一个class的实例后，我们可以给该实例绑定任何属性和方法，这就是动态语言的灵活性

from types import MethodType

class Student(object):
    pass

def set_age(self, age): # 定义一个函数作为实例方法
    self.age = age


class Student2(object):
    # 如果我们想要限制实例的属性怎么办？比如，只允许对Student实例添加name和age属性。
    # 为了达到限制的目的，Python允许在定义class的时候，定义一个特殊的__slots__变量，来限制该class实例能添加的属性：
    __slots__ = ('name', 'age') # 用tuple定义允许绑定的属性名称

# 使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：
class GraduateStudent(Student2):
    pass

if __name__ == '__main__':
    s = Student()
    s.name = "cuihuan"
    s.set_age = MethodType(set_age, s) # 给实例绑定一个方法
    s.set_age(25)
    print(s.age)

    # 给一个实例绑定的方法，对另一个实例是不起作用的：
    _s = Student()
    try:
        _s.set_age(23) # AttributeError: 'Student' object has no attribute 'set_age'
    except AttributeError as e:
        print(e.args)

    # 给class绑定方法后，所有实例均可调用：
    Student.set_age = MethodType(set_age, Student)
    _s.set_age(13)
    print(_s.age)  # 通常情况下，上面的set_score方法可以直接定义在class中，但动态绑定允许我们在程序运行的过程中动态给class加上功能，这在静态语言中很难实现。

    s2 = Student2()  # 创建新的实例
    s2.name = 'Michael'  # 绑定属性'name'
    s2.age = 25  # 绑定属性'age'
    try:
        s2.score = 99  # 绑定属性'score'  #报错 AttributeError: 'Student' object has no attribute 'score'
        # 由于'score'没有被放到__slots__中，所以不能绑定score属性，试图绑定score将得到AttributeError的错误。
    except AttributeError as e:
        print(e.args)

    # 使用__slots__要注意，__slots__定义的属性仅对当前类实例起作用，对继承的子类是不起作用的：

    S3 = GraduateStudent()
    S3.score = 99
    print(S3.score)
    # 除非在子类中也定义__slots__，这样，子类实例允许定义的属性就是自身的__slots__加上父类的__slots__。








