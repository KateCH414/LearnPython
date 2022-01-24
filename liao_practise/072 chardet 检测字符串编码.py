# --*-- coding:utf-8 --*--
# 对于未知编码的bytes，要把它转换成str
# 需要先“猜测”编码。猜测的方式是先收集各种编码的特征字符，根据特征字符判断，就能有很大概率“猜对”
# chardet这个第三方库可以检测编码

# 安装chardet
# pip install chardet
import chardet

if __name__ == '__main__':
    # 使用chardet 检测编码
    print(chardet.detect(b'Hello, world!'))
    # {'encoding': 'ascii', 'confidence': 1.0, 'language': ''}
    # 检测出是 ascii 编码， confidence字段，表示检测的概率是1.0（即100%）

    # 试试检测GBK编码的中文
    char = '好好学习，天天向上'.encode('GBK')
    print(chardet.detect(char))
    # {'encoding': 'GB2312', 'confidence': 0.99, 'language': 'Chinese'}
    # 检测的编码是GB2312，注意到GBK是GB2312的超集，两者是同一种编码，检测正确的概率是74%，language字段指出的语言是'Chinese'。

    # 对UTF-8编码进行检测
    char2 = '离离原上草，一岁一枯荣'.encode('utf-8')
    print(chardet.detect(char2))
    # {'encoding': 'utf-8', 'confidence': 0.99, 'language': ''}

    # 用chardet检测编码，使用简单。获取到编码后，再转换为str，就可以方便后续处理。
    # chardet支持检测的编码列表请参考官方文档: https://chardet.readthedocs.io/en/latest/supported-encodings.html


