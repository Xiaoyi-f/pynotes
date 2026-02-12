import multiprocessing
import os

"""
每个进程都有自己的进程编号
一旦程序运行起来就会默认创建一个主进程
实际上子进程就是把主进程的资源拷贝一份
他们是相互独立的，进程之间是不共享数据的
主进程会等待所有子进程结束再结束
所有的进程之间都是并行的，包括主子进程之间
进程是分配资源的最小单位，实际上执行的最小单位是线程
一个进程中至少要有一个线程来执行程序
同一个进程中的线程共享进程单元的所有资源
"""
# 还有name线程名和group线程组参数
# 进程对象 = multiprocessing.Process(target=任务名, args=(参数1, 参数2))
# 进程对象 = multiprocessing.Process(target=任务名, kwargs={"参数1": 值1, "参数2": 值2})
# 进程对象.start()


# def work():
#     print("work进程编号:", os.getpid())
#     print("work父进程编号:", os.getppid())
#
#
# def demo():
#     print("demo进程编号:", os.getpid())
#     print("demo父进程编号:", os.getppid())

# my_list = []
#
#
# def write_data():
#     for i in range(3):
#         my_list.append(i)
#         print("add:", i)
#     print("write_data:", my_list)
#
#
# def read_data():
#     print("read_data:", my_list)
# 守护进程的设置需要再启动之前设置
# work_process.daemon = True 设置子进程为守护进程，当主进程结束，子进程直接销毁，直接结束主进程以即所有子进程
# work_process.terminate() 手动销毁子进程
# 若两个子进程的父进程相同则说明两个进程由同一个父进程创建
print(os.getpid())
# python中进程能使用多核但是资源开销大
