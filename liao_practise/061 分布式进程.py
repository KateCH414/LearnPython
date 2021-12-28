# --*-- coding:utf-8 --*--


# Python的multiprocessing模块不但支持多进程，其中managers子模块还支持把多进程分布到多台机器上
# 一个服务进程可以作为调度者，将任务分布到其他多个进程中，依靠网络通信。
# 由于managers模块封装很好，不必了解网络通信的细节，就可以很容易地编写分布式多进程程序。

# 插入一个话题：什么是分布式系统
# 分布式系统是由一组通过网络进行通信、为了完成共同的任务而协调工作的计算机节点组成的系统。
# 分布式系统的出现是为了用廉价的、普通的机器完成单个计算机无法完成的计算、存储任务。其目的是利用更多的机器，处理更多的数据
# 分布式系统要解决的问题本身就是和单机系统一样的，而由于分布式系统多节点、通过网络通信的拓扑结构，会引入很多单机系统没有的问题，
# 为了解决这些问题又会引入更多的机制、协议，带来更多的问题。。。

# 举个例子：如果我们已经有一个通过Queue通信的多进程程序在同一台机器上运行，
# 现在，由于处理任务的进程任务繁重，希望把发送任务的进程和处理任务的进程分布到两台机器上。怎么用分布式进程实现？
# 原有的Queue可以继续使用，但是，通过managers模块把Queue通过网络暴露出去，就可以让其他机器的进程访问Queue

# 我们先看服务进程，服务进程负责启动Queue，把Queue注册到网络上，然后往Queue里面写入任务
import time, random, queue
from multiprocessing.managers import BaseManager

# 发送任务的队列
task_queue = queue.Queue()
# 接受结果的队列
result_queue = queue.Queue()


# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass


if __name__ == '__main__':
    # 把两个Queue都注册到网络上，callable 参数关联了Queue对象
    QueueManager.register("get_task_queue", callable=lambda: task_queue)
    QueueManager.register("get_result_queue", callable=lambda: result_queue)
    # 绑定端口 5000 设置验证码abc
    manager = QueueManager(address=('', 5000), authkey=b'abc')
    # 启动queue
    manager.start()
    # 获取通过网络获取的queue对象
    task = manager.get_task_queue()
    result = manager.get_result_queue()

    # 放几个任务进去
    for i in range(10):
        n = random.randint(0, 10000)
        print('Put task %d...' % n)
        task.put(n)

    # 从result队列读取结果:
    print('Try get results...')
    for i in range(10):
        r = result.get(timeout=10)
        print('Result: %s' % r)

    # 关闭:
    manager.shutdown()
    print('master exit.')


# 请注意，当我们在一台机器上写多进程程序时，创建的Queue可以直接拿来用，
# 在分布式多进程环境下，添加任务到Queue不可以直接对原始的task_queue进行操作，那样就绕过了QueueManager的封装，
# 必须通过manager.get_task_queue()获得的Queue接口添加。
# 然后，在另一台机器上启动任务进程（本机上启动也可以: 0611分布式任务进程）：
# 任务进程要通过网络连接到服务进程，所以要指定服务进程的IP。
# 可以试试分布式进程的工作效果了。
# 先启动task_master.py服务进程
# 再启动0611分布式任务进程
# 观察主进程输出，可以看到任务执行结果

# 这个简单的Master/Worker模型，就是一个简单但真正的分布式计算
# 把代码稍加改造，启动多个worker，就可以把任务分布到几台甚至几十台机器上
# Queue对象存储在哪？注意到task_worker.py中根本没有创建Queue的代码，所以，Queue对象存储在task_master.py进程中
# 而Queue之所以能通过网络访问，就是通过QueueManager实现的。由于QueueManager管理的不止一个Queue，所以，要给每个Queue的网络调用接口起个名字，比如get_task_queue

