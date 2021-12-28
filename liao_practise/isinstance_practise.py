class Animal(object):
    def run(self):
        print('Animal is running...')


class Dog(Animal):
    def run(self):
        print('dog is running...')


class Cat(Animal):
    def run(self):
        print('cat is running...')

if __name__ == '__main__':
    a = Animal()
    a.run()
    b = Dog()
    b.run()
    c = Cat()
    c.run()

    # isinstance()就可以告诉我们，一个对象是否是某种类型
    # 类的实例的类型是类自己
    print(isinstance(a, Animal)) # true
    # 类的子类的实例也可以是该类
    print(isinstance(b, Animal)) # true
    # 类的父类的实例不是该类
    print( isinstance(a, Dog))  #flase



