# --*-- coding:utf-8 --*--
# “进程是资源分配的最小单位，线程是CPU调度的最小单位”
# 进程与线程的区别：https://blog.csdn.net/linraise/article/details/12979473
# 进程是由若干线程组成的，一个进程至少有一个线程。
# 由于线程是操作系统直接支持的执行单元，因此，高级语言通常都内置多线程的支持，
# Python也不例外，并且，Python的线程是真正的Posix Thread，而不是模拟出来的线程。
# Python的标准库提供了两个模块：_thread和threading，_thread是低级模块，threading是高级模块，对_thread进行了封装

# 启动一个线程就是把一个函数传入并创建Thread实例，然后调用start()开始执行
import  time, threading


def loop():
    print("%s is running" % threading.current_thread().name)
    n = 0
    while n < 5:
        n = n+1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)


if __name__ == '__main__':
    print('thread %s is running...' % threading.current_thread().name)
    t = threading.Thread(target=loop, name='loopThread')
    t.start()
    t.join()
    print('thread %s ended.' % threading.current_thread().name)
    # 由于任何进程默认就会启动一个线程，我们把该线程称为主线程，主线程又可以启动新的线程，
    # Python的threading模块有个current_thread()函数，它永远返回当前线程的实例。主线程实例的名字叫MainThread，
    # 子线程的名字在创建时指定，我们用LoopThread命名子线程。名字仅仅在打印时用来显示，完全没有其他意义，如果不起名字Python就自动给线程命名为Thread-1，Thread-2……

    # Lock
    # 多线程和多进程最大的不同在于，多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享
    # 所以，任何一个变量都可以被任何一个线程修改，因此，线程之间共享数据最大的危险在于多个线程同时改一个变量，把内容给改乱了。

    # 来看看多个线程同时操作一个变量怎么把内容给改乱了：
    # 假定这是你的银行存款:
    balance = 0  # 我们定义了一个共享变量balance，初始值为0

    def change_it(n):
        # 先存后取
        global balance
        balance = balance + n
        balance = balance - n

    def run_thread(n):
        for i in range(20000000):
            change_it(n)

    # 并且启动两个线程，先存后取，理论上结果应该为0
    t1 = threading.Thread(target=run_thread, args=(5,))
    t2 = threading.Thread(target=run_thread, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    # 由于线程的调度是由操作系统决定的，当t1、t2交替执行时，只要循环次数足够多，balance的结果就不一定是0了
    print(balance)  #  -8..

    # 原因是因为高级语言的一条语句在CPU执行时是若干条语句，即使一个简单的计算：
    #
    # balance = balance + n
    # 也分两步：
    # 计算balance + n，存入临时变量中；
    # 将临时变量的值赋给balance。
    # 也就是可以看成：
    # x = balance + n
    # balance = x

    # 因为修改balance需要多条语句，而执行这几条语句时，线程可能中断，从而导致多个线程把同一个对象的内容改乱
    # 两个线程同时一存一取，就可能导致余额不对，你肯定不希望你的银行存款莫名其妙地变成了负数，
    # 所以，我们必须确保一个线程在修改balance的时候，别的线程一定不能改。
    # 要确保balance计算正确，就要给change_it()上一把锁，
    # 当某个线程开始执行change_it()时，我们说，该线程因为获得了锁，因此其他线程不能同时执行change_it()，
    # 只能等待，直到锁被释放后，获得该锁以后才能改。
    # 由于锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，
    # 不会造成修改的冲突。创建一个锁就是通过threading.Lock()来实现：

    balance = 0
    lock = threading.Lock()
    def run_thread_lock(n):
        for i in range(20000):
            # 先取锁
            lock.acquire()
            try:
                # 操作共有数据
                change_it(n)
            finally:
                # 最后一定要释放锁
                lock.release()
                # 获得锁的线程用完后一定要释放锁，否则那些苦苦等待锁的线程将永远等待下去，成为死线程。所以我们用try...finally来确保锁一定会被释放。
    # 再尝试调用下
    t1 = threading.Thread(target=run_thread_lock, args=(5,))
    t2 = threading.Thread(target=run_thread_lock, args=(8,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print(balance)
    # 锁的好处：确保了某段关键代码只能由一个线程从头到尾完整地执行，
    # 坏处有很多:1.阻止了多线程并发执行，包含锁的某段代码实际上只能以单线程模式执行，效率就大大地下降了。
    #           2.由于可以存在多个锁，不同的线程持有不同的锁，并试图获取对方持有的锁时，可能会造成死锁，导致多个线程全部挂起，既不能执行，也无法结束，只能靠操作系统强制终止。

    # 一个死循环线程会100%占用一个CPU
    # 如果有两个死循环线程，在多核CPU中，可以监控到会占用200%的CPU，也就是占用两个CPU核心。
    # 用C、C++或Java来改写相同的死循环，直接可以把全部核心跑满，4核就跑到400%，8核就跑到800%，
    # Python：4核CPU上可以监控到CPU占用率仅有102%，也就是仅使用了一核。
    # 因为Python的线程虽然是真正的线程，但解释器执行代码时，有一个GIL锁：Global Interpreter Lock，
    # 任何Python线程执行前，必须先获得GIL锁，然后，每执行100条字节码，解释器就自动释放GIL锁，让别的线程有机会执行。
    # 这个GIL全局锁实际上把所有线程的执行代码都给上了锁，所以，多线程在Python中只能交替执行，即使100个线程跑在100核CPU上，也只能用到1个核。
    # GIL是Python解释器设计的历史遗留问题，通常我们用的解释器是官方实现的CPython，要真正利用多核，除非重写一个不带GIL的解释器。
    # 在Python中，可以使用多线程，但不要指望能有效利用多核。如果一定要通过多线程利用多核，那只能通过C扩展来实现，不过这样就失去了Python简单易用的特点。
    # Python虽然不能利用多线程实现多核任务，但可以通过多进程实现多核任务。多个Python进程有各自独立的GIL锁，互不影响。



