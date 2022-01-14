# --*-- coding:utf-8 --*--
# 安装Pillow  如果遇到Permission denied安装失败，请加上sudo重试。
# $ pip install pillow
# 要详细了解PIL的强大功能，请请参考Pillow官方文档：
# https://pillow.readthedocs.org/

from PIL import Image, ImageFilter, ImageDraw, ImageFont
import random

if __name__ == '__main__':
    # 打开一个jpg图像文件，注意是当前路径:
    im = Image.open('/Users/huancui/project/Python_ch/python_test/picture/images.jpeg')
    # 获得图像尺寸:
    w, h = im.size
    print('image width is %s, height is %s' % (w, h))
    # 缩放到50%
    im.thumbnail((w/2, h/2))
    print('Resize image to: %sx%s' % (w / 2, h / 2))
    # 把缩放后的图像用jpeg格式保存:
    im.save('/Users/huancui/project/Python_ch/python_test/picture/thumbnail.jpg', 'jpeg')

    # 其他功能如切片、旋转、滤镜、输出文字、调色板等一应俱全。
    # 比如，模糊效果也只需几行代码：
    im2 = im.filter(ImageFilter.BLUR)
    im2.save('/Users/huancui/project/Python_ch/python_test/picture/filter.jpg', 'jpeg')

    # PIL的ImageDraw提供了一系列绘图方法，让我们可以直接绘图。
    # 比如要生成字母验证码图片

    # 随机字母
    def randChar():
        return chr(random.randint(65, 90))

    # 随机颜色1
    def randColor():
        return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

    # 随机颜色2
    def randColor2():
        return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

    width = 60 * 4
    height = 60

    image = Image.new('RGB', (width, height))
    # 创建Font对象:
    font = ImageFont.truetype('Arial.ttf', 36)
    # 创建Draw对象:
    draw = ImageDraw.Draw(image)

    # 填充每个像素:
    for x in range(width):
        for y in range(height):
            draw.point((x,y), fill=randColor())
        
    # 输出文字:
    for t in range(4):
        draw.text((60 * t + 10, 10), randChar(), font=font, fill=randColor2())

    # 模糊:
    image = image.filter(ImageFilter.BLUR)
    image.save('/Users/huancui/project/Python_ch/python_test/picture/code.jpg', 'jpeg')














