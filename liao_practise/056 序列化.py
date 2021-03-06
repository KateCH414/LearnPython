# --*-- coding:utf-8 --*--

# 把变量从内存中变成可存储或传输的过程称之为序列化
# 在Python中叫pickling，在其他语言中也被称之为serialization，marshalling，flattening等等
# 序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上
# 把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling
import pickle


if __name__ == '__main__':
    d = dict(name='Bob', age=20, score=88)
    d_pickle = pickle.dumps(d)
    # b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
    print(d_pickle)
    # pickle.dumps()方法把任意对象序列化成一个bytes，然后可以把这个bytes写入文件。
    # 或者用另一个方法pickle.dump()直接把对象序列化后写入一个file-like Object：
    with open('dump.txt', 'wb') as f:
        pickle.dump(d, f)

    # 当我们要把对象从磁盘读到内存时，可以先把内容读到一个bytes，然后用pickle.loads()方法反序列化出对象，
    # 也可以直接用pickle.load()方法从一个file-like Object中直接反序列化出对象
    with open('dump.txt', 'rb') as f:
        d = pickle.load(f)
    print(d)

    # Pickle的问题和所有其他编程语言特有的序列化问题一样，就是它只能用于Python，
    # 并且可能不同版本的Python彼此都不兼容，因此，只能用Pickle保存那些不重要的数据，不能成功地反序列化也没关系。

    # 要在不同的编程语言之间传递对象，就必须把对象序列化为标准格式
    # XML,JSON,PB 等等
    # JSON:JSON表示的对象就是标准的JavaScript语言的对象
    # JSON和Python内置的数据类型对应如下:
    # JSON类型	    Python类型
    # {}	        dict
    # []	        list
    # "string"	    str
    # 1234.56	    int或float
    # true/false	True/False
    # null	        None

    # Python内置的json模块提供了非常完善的Python对象到JSON格式的转换
    import json
    d = dict(name='Bob', age=20, score=88)
    d_json = json.dumps(d)
    print(d_json)
    # dumps()方法返回一个str，内容就是标准的JSON。类似的，dump()方法可以直接把JSON写入一个file-like Object。
    # 要把JSON反序列化为Python对象，用loads()或者对应的load()方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化：
    d_ = json.loads(d_json)
    # JSON标准规定JSON编码是UTF-8，能够正确地在Python的str与JSON的字符串之间转换。

    # Python的dict对象可以直接序列化为JSON的{}，不过，很多时候，我们更喜欢用class表示对象，比如定义Student类，然后序列化：
    class Student(object):
        def __init__(self, name, age, score):
            self.name = name
            self.age = age
            self.score = score


    s = Student('Bob', 20, 88)

    # dumps()方法的参数列表，可以发现，除了第一个必须的obj参数外，dumps()方法还提供了一大堆的可选参数：
    # https://docs.python.org/3/library/json.html#json.dumps

    # 可选参数default就是把任意一个对象变成一个可序列为JSON的对象，我们只需要为Student专门写一个转换函数，再把函数传进去即可：
    # json转换函数
    def student2dict(std):
        return {
            'name': std.name,
            'age': std.age,
            'score': std.score
        }
    s_json = json.dumps(s, default=student2dict)
    print(s_json)

    # 下次如果遇到一个Teacher类的实例，照样无法序列化为JSON。我们可以偷个懒，把任意class的实例变为dict：
    print(json.dumps(s, default=lambda obj: obj.__dict__))
    # 因为通常class的实例都有一个__dict__属性，它就是一个dict，用来存储实例变量。也有少数例外，比如定义了__slots__的class

    # 要把JSON反序列化为一个Student对象实例，loads()方法首先转换出一个dict对象，然后，我们传入的object_hook函数负责把dict转换为Student实例：
    def dict2student(d):
        return Student(d['name'], d['age'], d['score'])


    json_str = '{"age": 20, "score": 88, "name": "Bob"}'
    print(json.loads(json_str, object_hook=dict2student)) # 打印出的是反序列化的Student实例对象。
    s = json.loads(json_str, object_hook=dict2student)
    print(s.name)

    # 对中文进行JSON序列化时，json.dumps()提供了一个ensure_ascii参数，观察该参数对结果的影响











