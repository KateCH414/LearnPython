# --*-- coding:utf-8 --*--
# 《Mastering Python Design Patterns》的读书笔记，涵盖大部分设计模式(力求pythonic实现)，有兴趣可以参考下，
# 代码示例版本为python3.5.2。

# 创建型设计模式处理对象创建相关的问题，目标是当直接创建对象不太方便时，提供更好的方式
# 在工厂设计模式中，客户端可以请求一个对象，而无需知道这个对象来自哪里；也就是，使用哪个类来生成这个对象。
# 工厂背后的思想是简化对象的创建
# 工厂通常有两种形式，
#   第一种是工厂方法（Factory Method），它是一个方法，对不同的输入参数返回不同的对象
#   第二种是抽象工厂，它是一组用于创建一系列相关事物对象的工厂方法

# 下面来说【工厂方法】
# 适应场景：如果因为应用创建对象的代码分布在多个不同的地方，而不是仅在一个函数/方法中，你发现没法跟踪这些对象，那么应该考虑使用工厂方法模式。
#          创建多个工厂方法也完全没有问题，实践中通常也这么做，对相似的对象创建进行逻辑分组，每个工厂方法负责一个分组。
#          需要将对象的创建和使用解耦，工厂方法也能派上用场。

# 使用举例：Django 框架使用工厂方法模式来创建表单字段。
#         Django 的 forms 模块支持不同种类字段（CharField、EmailField）的创建和定制（max_length、required）

# 工厂方法优点：在必要时创建新的对象，从而提高性能和内存使用率


# Method(工厂方法)：执行单独的函数，通过传参提供需要的对象信息
# 使用工厂方法，demo 如下
# 解析 XML 和 JSON。 文件
import json
import xml.etree.ElementTree as etree


# 负责json 解析
class JSONConnector:
    def __init__(self, filepath):
        self.data = dict()
        with open(filepath, mode='r', encoding='utf-8') as f:
            self.data = json.load(f)

    # 使用 property 修饰器使其看上去像是一个变量而不是函数
    @property
    def parse_data(self):
        return self.data


# 负责XML解析
class XMLConnector:
    def __init__(self, filepath):
        self.tree = etree.parse(filepath)

    @property
    def parse_data(self):
        return self.tree


# 工厂方法
def connection_factory(filepath):
    """工厂方法"""
    # 根据文件后缀判断使用哪一种解析方式
    if filepath.endswith('json'):
        connector = JSONConnector
    elif filepath.endswith('xml'):
        connector = XMLConnector
    else:
        raise ValueError('Cannot connect to {}'.format(filepath))
    return connector(filepath)


# 增加异常处理的工厂方法
def connect_to(filepath):
    factory = None
    try:
        factory = connection_factory(filepath)
    except ValueError as ve:
        print(ve)
    return factory


if __name__ == '__main__':
    # 测试异常
    sqlite_factory = connect_to('/Users/huancui/project/Python_ch/python_test/liao_practise/dump.txt')

    # 测试解析 xml
    xml_factory = connect_to('/Users/huancui/project/Python_ch/python_test/liao_practise/test_xml.xml')
    xml_data = xml_factory.parse_data
    liars = xml_data.findall(".//{}[{}='{}']".format('person',
                                                     'lastName', 'Liar'))
    print('found: {} persons'.format(len(liars)))

    # 测试解析 json
    json_factory = connect_to('/Users/huancui/project/Python_ch/python_test/liao_practise/test_json.json')
    json_data = json_factory.parse_data
    print('found: {} donuts'.format(len(json_data)))



