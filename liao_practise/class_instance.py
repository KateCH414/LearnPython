# -*- coding:utf-8 -*-

# 实例属性和类属性
class Student():
    # 如果Student类本身需要绑定一个属性呢？可以直接在class中定义属性，这种属性是类属性，归Student类所有：
    name = "student"
    def __init__(self):
        # 由于Python是动态语言，根据类创建的实例可以任意绑定属性。给实例绑定属性的方法是通过实例变量，或者通过self变量：
        self.age = 90
        pass

if __name__ == '__main__':
    s = Student() # 创建实例s
    print(s.name)  # 打印name属性，因为实例并没有name属性，所以会继续查找class的name属性
    print(Student.name)  # 打印类的name属性
    s.name = 'Michael'  # 给实例绑定name属性
    print(s.name)  # 由于实例属性优先级比类属性高，因此，它会屏蔽掉类的name属性
    print(Student.name)  # 但是类属性并未消失，用Student.name仍然可以访问
    del s.name  # 如果删除实例的name属性
    print(s.name)  # 再次调用s.name，由于实例的name属性没有找到，类的name属性就显示出来了
