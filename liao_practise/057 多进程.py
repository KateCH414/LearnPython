# --*-- coding:utf-8 --*--

# Python程序实现多进程（multiprocessing）

# 小结
# 在Unix/Linux下，可以使用fork()调用实现多进程。
#
# 要实现跨平台的多进程，可以使用multiprocessing模块。
#
# 进程间通信是通过Queue、Pipes等实现的。

import os


if __name__ == '__main__':
    # os.fork()
    # Unix/Linux操作系统提供了一个fork()系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是fork()调用一次，返回两次，
    # 因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回
    # 父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，父进程要记下每个子进程的ID，
    # 子进程永远返回0，子进程只需要调用getppid()就可以拿到父进程的ID。

    # Python的os模块封装了常见的系统调用，其中就包括fork，可以在Python程序中轻松创建子进程
    print('Process (%s) start...' % os.getpid())
    # Only works on Unix/Linux/Mac:
    # 由于Windows没有fork调用，上面的代码在Windows上无法运行。而Mac系统是基于BSD（Unix的一种）内核，所以，在Mac下运行是没有问题的，推荐大家用Mac学Python！
    # 有了fork调用，一个进程在接到新任务时就可以复制出一个子进程来处理新任务，常见的Apache服务器就是由父进程监听端口，每当有新的http请求时，就fork出子进程来处理新的http请求。
    pid = os.fork()
    if pid == 0:
        print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
    else:
        print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
    pass
    print('-------------------------------')

    # multiprocessing 模块
    # Python是跨平台的，自然也应该提供一个跨平台的多进程支持。multiprocessing模块就是跨平台版本的多进程模块。
    # multiprocessing模块提供了一个Process类来代表一个进程对象
    # 下面的例子演示了启动一个子进程并等待其结束
    from multiprocessing import Process
    # 先定义子进程所要执行方法

    def run_proc(name):
        print('child process %s(%s) is runing' % (name, os.getpid()))

    print('parent process %s(%s) is running' % (os.name, os.getpid()))
    p1 = Process(target=run_proc, args=('test',))  # 创建子进程时，需要传入一个执行函数和函数的参数，创建一个Process实例
    print('child process will start')
    p1.start()  # start()方法启动子进程
    p1.join()  # join()方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步
    print('child process end')

    print('-------------------------------')
    # Pool
    # 如果要启动大量的子进程，可以用进程池的方式批量创建子进程
    # Pool可以提供指定数量的进程，供用户调用，当有新的请求提交到pool中时，如果池还没有满，那么就会创建一个新的进程用来执行该请求；
    # 但如果池中的进程数已经达到规定最大值，那么该请求就会等待，直到池中有进程结束，才会创建新的进程来它。
    from multiprocessing import Pool
    import os, time, random


    def Foo(i):
        time.sleep(2)
        print('到了2s')
        return i + 100


    def Bar(arg):
        print('结果：', arg)

    print('Parent process %s.' % os.getpid())
    p2 = Pool(5) #允许进程池同时放入5个进程

    for i in range(10): #10个进程都启动 但是一次只能运行5个'
        # p2.apply(func= Foo,args=(i,))  #串行执行进程，一次执行1个进程
        p2.apply_async(Foo, args=(i,), callback=Bar) #并行执行进程，一次5个,callback回调 Foo执行完就会执行Bar

    print('Waiting for all subprocesses done...')
    p2.close()  # 调用join()之前必须先调用close()，调用close()之后就不能继续添加新的Process
    p2.join()  # 对Pool对象调用join()方法会等待所有子进程执行完毕
    print('All subprocesses done.')

    '''    
    函数解释：
    apply_async(func[, args[, kwds[, callback]]]) 它是非阻塞，
    apply(func[, args[, kwds]])是阻塞的
    close()    关闭pool，使其不在接受新的任务。
    terminate()    结束工作进程，不在处理未完成的任务。
    join()    主进程阻塞，等待子进程的退出， join方法要在close或terminate之后使用。
    pool.apply(func, (msg, ))   #维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
    '''

    # 子进程  subprocess模块
    # 很多时候，子进程并不是自身，而是一个外部进程。我们创建了子进程后，还需要控制子进程的输入和输出。
    # subprocess模块可以让我们非常方便地启动一个子进程，然后控制其输入和输出
    # 下面的例子演示了如何在Python代码中运行命令nslookup www.python.org，这和命令行直接运行的效果是一样的
    import subprocess

    # run 方法语法格式如下：
    #
    # subprocess.run(args, *, stdin=None, input=None, stdout=None, stderr=None, capture_output=False, shell=False,
    # cwd=None,  timeout=None, check=False, encoding=None, errors=None, text=None, env=None, universal_newlines=None)
    # args：表示要执行的命令。必须是一个字符串，字符串参数列表。
    # stdin、stdout 和 stderr：子进程的标准输入、输出和错误。
    #   其值可以是 subprocess.PIPE、subprocess.DEVNULL、一个已经存在的文件描述符、已经打开的文件对象或者 None。
    #   subprocess.PIPE 表示为子进程创建新的管道。
    #   subprocess.DEVNULL 表示使用 os.devnull。
    #   默认使用的是 None，表示什么都不做。
    #   另外，stderr 可以合并到 stdout 里一起输出。
    # timeout：设置命令超时时间。如果命令执行时间超时，子进程将被杀死，并弹出 TimeoutExpired 异常。
    # check：如果该参数设置为 True，并且进程退出状态码不是 0，则弹 出 CalledProcessError 异常。
    # encoding: 如果指定了该参数，则 stdin、stdout 和 stderr 可以接收字符串数据，并以该编码方式编码。否则只接收 bytes 类型的数据。
    # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。

    # 实例：
    # 执行ls -l /dev/null 命令
    p_run = subprocess.run(["ls", "-l", "/dev/null"])
    print( p_run.stdout)

    # Popen() 方法
    # Popen 是 subprocess的核心，子进程的创建和管理都靠它处理。
    #
    # 构造函数：
    # class subprocess.Popen(args, bufsize=-1, executable=None, stdin=None, stdout=None, stderr=None,
    # preexec_fn=None, close_fds=True, shell=False, cwd=None, env=None, universal_newlines=False,
    # startupinfo=None, creationflags=0,restore_signals=True, start_new_session=False, pass_fds=(),
    # *, encoding=None, errors=None)

    # args：shell命令，可以是字符串或者序列类型（如：list，元组）
    # bufsize：缓冲区大小。当创建标准流的管道对象时使用，默认-1。
    # 0：不使用缓冲区
    # 1：表示行缓冲，仅当universal_newlines=True时可用，也就是文本模式
    # 正数：表示缓冲区大小
    # 负数：表示使用系统默认的缓冲区大小。
    # stdin, stdout, stderr：分别表示程序的标准输入、输出、错误句柄
    # preexec_fn：只在 Unix 平台下有效，用于指定一个可执行对象（callable object），它将在子进程运行之前被调用
    # shell：如果该参数为 True，将通过操作系统的 shell 执行指定的命令。
    # cwd：用于设置子进程的当前目录。
    # env：用于指定子进程的环境变量。如果 env = None，子进程的环境变量将从父进程中继承。

    # 实例
    p_popen = subprocess.Popen('ls -l', shell=True)
    print(p_popen.returncode)
    p_popen.wait()
    print(p_popen.returncode)

    # Popen 对象方法
    # poll(): 检查进程是否终止，如果终止返回 returncode，否则返回 None。
    # wait(timeout): 等待子进程终止。
    # communicate(input,timeout): 和子进程交互，发送和读取数据。
    # send_signal(singnal): 发送信号到子进程 。
    # terminate(): 停止子进程,也就是发送SIGTERM信号到子进程。
    # kill(): 杀死子进程。发送 SIGKILL 信号到子进程。

    # 实例 实现cmd 命令
    def cmd(command):
        subp = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
        subp.wait(2)
        if subp.poll() == 0:
            print(subp.communicate()[1])
        else:
            print("失败")

    cmd("java -version")

    # 进程间通信
    # Process之间肯定是需要通信的，操作系统提供了很多机制来实现进程间的通信。
    # Python的multiprocessing模块包装了底层的机制，提供了Queue、Pipes等多种方式来交换数据。
    # 以Queue为例，在父进程中创建两个子进程，一个往Queue里写数据，一个从Queue里读数据
    from multiprocessing import  Queue


    # 写数据进程执行的代码:
    def write(q):
        print('Process to write: %s' % os.getpid())
        for value in ['A', 'B', 'C']:
            print('Put %s to queue...' % value)
            q.put(value)
            time.sleep(random.random())


    # 读数据进程执行的代码:
    def read(q):
        print('Process to read: %s' % os.getpid())
        while True:
            value = q.get(True)
            print('Get %s from queue.' % value)

    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()





