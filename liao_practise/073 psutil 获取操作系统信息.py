# --*-- coding:utf-8 --*--
# 顾名思义，psutil = process and system utilities

# 安装psutil
# pip install psutil
import psutil
# psutil还可以获取用户信息、Windows服务等很多有用的系统信息，具体请参考psutil的官网：https://github.com/giampaolo/psutil



if __name__ == '__main__':
    # 获取CPU信息
    print(psutil.cpu_count())  # CPU逻辑数量
    print(psutil.cpu_count(logical=False))  # CPU物理核心
    # 统计CPU的用户／系统／空闲时间：
    print(psutil.cpu_times())  # scputimes(user=656903.47, nice=0.0, system=370308.45, idle=1209886.31)
    # 实现类似top命令的CPU使用率，每秒刷新一次，累计10次
    for x in range(10):
        print(psutil.cpu_percent(interval=1, percpu=True))
    # [88.9, 65.3, 86.1, 65.3, 85.3, 66.0, 85.0, 65.3]
    # [84.2, 62.0, 81.0, 60.0, 80.8, 61.4, 79.0, 60.6]
    # [80.0, 53.5, 77.0, 52.5, 75.5, 50.0, 75.2, 50.5]
    # [86.0, 57.0, 84.0, 55.0, 83.0, 56.4, 81.2, 56.0]
    # [95.0, 83.2, 94.0, 82.0, 94.0, 82.2, 93.0, 82.0]
    # [84.0, 50.0, 79.0, 48.0, 80.2, 46.5, 80.0, 46.5]
    # [91.1, 66.0, 88.1, 65.3, 88.0, 67.0, 88.1, 66.0]
    # [89.1, 61.4, 87.1, 61.0, 87.0, 60.8, 87.0, 60.4]
    # [97.0, 88.0, 98.0, 87.0, 97.0, 88.0, 96.0, 87.1]
    # [81.8, 50.0, 76.2, 47.5, 77.2, 46.5, 75.2, 47.5]

    # 获取内存信息
    # 使用psutil获取物理内存和交换内存信息
    print(psutil.virtual_memory())
    # svmem(total=34359738368, available=14331977728, percent=58.3, used=19369197568, free=498126848, active=13910343680, inactive=13716361216, wired=5458853888)
    print(psutil.swap_memory())
    # sswap(total=1073741824, used=150732800, free=923009024, percent=14.0, sin=10705981440, sout=40353792)

    # 返回的是字节为单位的整数，可以看到，总内存大小是34359738368 = 32 GB，已用14331977728，使用了58.3%。
    # 而交换区大小是1073741824 = 1 GB。

    # 获取磁盘信息
    # 通过psutil获取磁盘分区、磁盘使用率和磁盘IO信息：
    print(psutil.disk_partitions())
    # [sdiskpart(device='/dev/disk1s5s1', mountpoint='/', fstype='apfs', opts='ro,local,rootfs,dovolfs,journaled,multilabel', maxfile=255, maxpath=1024), sdiskpart(device='/dev/disk1s4', mountpoint='/System/Volumes/VM', fstype='apfs', opts='rw,noexec,local,dovolfs,dontbrowse,journaled,multilabel,noatime', maxfile=255, maxpath=1024), sdiskpart(device='/dev/disk1s2', mountpoint='/System/Volumes/Preboot', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel', maxfile=255, maxpath=1024), sdiskpart(device='/dev/disk1s6', mountpoint='/System/Volumes/Update', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel', maxfile=255, maxpath=1024), sdiskpart(device='/dev/disk1s1', mountpoint='/System/Volumes/Data', fstype='apfs', opts='rw,local,dovolfs,dontbrowse,journaled,multilabel', maxfile=255, maxpath=1024)]
    print(psutil.disk_usage('/'))
    # sdiskusage(total=499963174912, used=30959017984, free=218329436160, percent=12.4)
    print(psutil.disk_io_counters())
    # sdiskio(read_count=68062409, write_count=31311015, read_bytes=824709390336, write_bytes=1057203191808, read_time=58484733, write_time=14914085)
    # 磁盘'/'的总容量是499963174912 ，使用了12.4%。文件格式是apfs，opts中包含rw表示可读写，journaled表示支持日志。

    # 获取网络信息
    # psutil可以获取网络接口和网络连接信息：
    print(psutil.net_io_counters())  # 获取网络读写字节／包的个数
    print(psutil.net_if_addrs())  # 获取网络接口信息
    print(psutil.net_if_stats())  # 获取网络接口状态
    # 获取当前网络连接信息
    try:
        print(psutil.net_connections())
        # 你可能会得到一个AccessDenied错误，原因是psutil获取信息也是要走系统接口，而获取网络连接信息需要root权限，这种情况下，可以退出Python交互环境，用sudo重新启动：
    except Exception as e:
        print(e)

    # 获取进程信息
    try:
        print(psutil.pids())  # 所有进程ID
        p = psutil.Process(1)
        print(p.name())  # 进程名称
        print(p.exe())  # 进程exe路径
        print(p.cwd())  # 进程工作目录
        print(p.cmdline())  # 进程启动的命令行
        print(p.ppid())  # 父进程ID
        print(p.parent())   # 父进程
        print(p.children())  # 子进程列表
        print(p.status())  # 进程状态
        print(p.username())  # 进程用户名
        print(p.create_time())  # 进程创建时间
        p.terminal()  # 进程终端
        p.cpu_times()  # 进程使用的CPU时间
        p.memory_info()  # 进程使用的内存
        p.open_files()  # 进程打开的文件
        p.connections()  # 进程相关网络连接
        p.num_threads()  # 进程的线程数量
        p.threads()  # 所有线程信息
        p.environ()  # 进程环境变量
        p.terminate()  # 结束进程
    except Exception as e:
        print(e)
        # 和获取网络连接类似，获取一个root用户的进程需要root权限，启动Python交互环境或者.py文件时，需要sudo权限。

    # psutil还提供了一个test()函数，可以模拟出ps命令的效果：
    print(psutil.test())


