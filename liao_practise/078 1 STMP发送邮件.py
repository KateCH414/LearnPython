# --*-- coding:utf-8 --*--
# SMTP是发送邮件的协议，Python内置对SMTP的支持，可以发送纯文本邮件、HTML邮件以及带附件的邮件。
# Python对SMTP支持有smtplib和email两个模块，email负责构造邮件，smtplib负责发送邮件。

# 首先，我们来构造一个最简单的纯文本邮件：
from email.mime.text import MIMEText
import smtplib

msg = MIMEText('hello, send by python...', 'plain', 'utf--8')
# 构造MIMEText对象时，第一个参数就是邮件正文，第二个参数是MIME的subtype，传入'plain'表示纯文本，最终的MIME就是'text/plain'，最后一定要用utf-8编码保证多语言兼容性。

# 通过SMTP发出去
#  输入 Email 地址与口令：
# from_addr = input('From: ')
# password = input('Password: ')
# # 输入收件人地址：
# to_addr = input('To: ')
# # 输入SMTP服务器地址
# smtp_server = input('SMTP server: ')
#
# server = smtplib.SMTP(smtp_server, 25)  # SMTP协议默认端口是25
# server.set_debuglevel(1)  # set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息
# server.login(from_addr, password)  # login()方法用来登录SMTP服务器
# server.sendmail(from_addr, [to_addr], msg.as_string())
# # sendmail()方法就是发邮件
# # 可以一次发给多个人，所以收件人传入一个list
# # as_string()把MIMEText对象变成str。
# server.quit()

# 仔细观察，发现如下问题：
# 邮件没有主题；
# 收件人的名字没有显示为友好的名字，比如Mr Green <green@example.com>；
# 明明收到了邮件，却提示不在收件人中。
# 这是因为邮件主题、如何显示发件人、收件人等信息并不是通过SMTP协议发给MTA，而是包含在发给MTA的文本中的
# 必须把From、To和Subject添加到MIMEText中，才是一封完整的邮件：

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

from_addr = input('From: ')
password = input('Password: ')
to_addr = input('To: ')
smtp_server = input('SMTP server: ')

msg = MIMEText('hello, send by Python...', 'plain', 'utf-8')
msg['From'] = _format_addr('python %s' % from_addr)
msg['To'] = _format_addr('管理员 %s' % to_addr)
msg['Subjeck'] = Header('来自。。的问候', 'utf-8').encode()

server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()
# 编写了一个函数_format_addr()来格式化一个邮件地址。注意不能简单地传入name <addr@example.com>，因为如果包含中文，需要通过Header对象进行编码。
# msg['To']接收的是字符串而不是list，如果有多个邮件地址，用,分隔即可。

# 你看到的收件人的名字很可能不是我们传入的管理员，因为很多邮件服务商在显示邮件时，会把收件人名字自动替换为用户注册的名字，但是其他收件人名字的显示不受影响。
# 查看Email的原始内容，可以看到如下经过编码的邮件头：
# From: =?utf-8?b?UHl0aG9u54ix5aW96ICF?= <xxxxxx@163.com>
# To: =?utf-8?b?566h55CG5ZGY?= <xxxxxx@qq.com>
# Subject: =?utf-8?b?5p2l6IeqU01UUOeahOmXruWAmeKApuKApg==?=
# 这就是经过Header对象编码的文本，包含utf-8编码信息和Base64编码的文本。如果我们自己来手动构造这样的编码文本，显然比较复杂。

# 发送html邮件
# 构造MIMEText对象时，把HTML字符串传进去，
# 再把第二个参数由plain变为html
msg =  MIMEText('<html><body><h1>Hello</h1>' +
    '<p>send by <a href="http://www.python.org">Python</a>...</p>' +
    '</body></html>', 'html', 'utf-8')

# 发送附件发送附件
# 带附件的邮件可以看做包含若干部分的邮件：文本和各个附件本身
# 构造一个MIMEMultipart对象代表邮件本身，
# 然后往里面加上一个MIMEText作为邮件正文，
# 再继续往里面加上表示附件的MIMEBase对象
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
msg = MIMEMultipart()
# 邮件正文是MIMEText:
msg.attach(MIMEText('send with file...', 'plain', 'utf-8'))
# 添加附件就是加上一个MIMEBase，从本地读取一个图片:
with open('/Users/huancui/project/Python_ch/python_test/pciture/images.jpeg', 'rb') as f:
    # 设置附件的MIME和文件名称
    mime = MIMEBase('image', 'jpeg', filename='images.jpeg')
    # 加上头信息
    mime.add_header('Content-Disposition', 'attachment', filename='images.jpeg')
    mime.add_header('Content-ID', '<0>')
    mime.add_header('X-Attachment-Id', '0')
    # 把附件内容读进来
    mime.set_payload(f.read())
    # 编码
    encoders.encode_base64(mime)
    msg.attach(mime)

# 发送图片:把一个图片嵌入到邮件正文中
# 要把图片嵌入到邮件正文中，我们只需按照发送附件的方式，先把邮件作为附件添加进去，
# 然后，在HTML中通过引用src="cid:0"就可以把附件作为图片嵌入了。
# 如果有多个图片，给它们依次编号，然后引用不同的cid:x即可。
# 把上面代码加入MIMEMultipart的MIMEText从plain改为html，然后在适当的位置引用图片
msg.attach(MIMEText('<html><body><h1>Hello</h1>' +
    '<p><img src="cid:0"></p>' +
    '</body></html>', 'html', 'utf-8'))


# 同时支持HTML和Plain格式
# 在发送HTML的同时再附加一个纯文本，
# 如果收件人无法查看HTML格式的邮件，就可以自动降级查看纯文本邮件
# 利用MIMEMultipart就可以组合一个HTML和Plain，要注意指定subtype是alternative：
msg = MIMEMultipart('alternative')
msg.attach(MIMEText('hello', 'plain', 'utf-8'))
msg.attach(MIMEText('<html><body><h1>Hello</h1></body></html>', 'html', 'utf-8'))

# 加密SMTP
# 使用标准的25端口连接SMTP服务器时，使用的是明文传输，发送邮件的整个过程可能会被窃听
# 加密SMTP会话，实际上就是先创建SSL安全连接，然后再使用SMTP协议发送邮件。
# 某些邮件服务商，例如Gmail，提供的SMTP服务必须要加密传输。Gmail的SMTP端口是587
smtp_server = 'smtp.gmail.com'
smtp_port = 587
server = smtplib.SMTP(smtp_server, smtp_port)
server.starttls()
# 剩下的代码和前面的一模一样:
server.set_debuglevel(1)
# 只需要在创建SMTP对象后，立刻调用starttls()方法，就创建了安全连接。后面的代码和前面的发送邮件代码完全一样。

# 构造一个邮件对象就是一个Messag对象，
# 如果构造一个MIMEText对象，就表示一个文本邮件对象，
# 如果构造一个MIMEImage对象，就表示一个作为附件的图片，
# 要把多个对象组合起来，就用MIMEMultipart对象，
# 而MIMEBase可以表示任何对象。
# 它们的继承关系如下：
# Message
# +- MIMEBase
#    +- MIMEMultipart
#    +- MIMENonMultipart
#       +- MIMEMessage
#       +- MIMEText
#       +- MIMEImage


