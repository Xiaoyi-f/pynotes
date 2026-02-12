# 多线程和多进程的模型虽然解决了并发问题，但是系统不能无上限地增加线程。由于系统切换线程的开销也很大，所以，一旦线程数量过多，CPU的时间就花在线程切换上了，真正运行代码的时间就少了，结果导致性能严重下降。
# 由于我们要解决的问题是CPU高速执行能力和IO设备的龟速严重不匹配，多线程和多进程只是解决这一问题的一种方法。
# 另一种解决IO问题的方法是异步IO。当代码需要执行一个耗时的IO操作时，它只发出IO指令，并不等待IO结果，然后就去执行其他代码了。一段时间后，当IO返回结果时，再通知CPU进行处理
# Python对协程的支持是通过generator实现的。
# 在generator中，我们不但可以通过for循环来迭代，还可以不断调用next()函数获取由yield语句返回的下一个值。
# 但是Python的yield不但可以返回一个值，它还可以接收调用者发出的参数。
# asyncio、aiohttp模块使用
import asyncio
import time


# 1. 定义协程
async def hello(name="world"):
    """简单的异步函数示例"""
    print(f"Hello {name}! 开始执行...")
    await asyncio.sleep(1)  # 遇到sleep就切走，模拟IO操作
    print(f"Hello {name}! 执行完成!")
    return f"Hello {name}!"


# 2. 并发执行多个协程
async def concurrent_example():
    """并发执行示例"""
    print("=== 并发执行示例 ===")
    start_time = time.time()
    
    # 同时启动三个协程
    results = await asyncio.gather(
        hello("Alice"),
        hello("Bob"),
        hello("Charlie")
    )
    
    end_time = time.time()
    print(f"并发执行结果: {results}")
    print(f"总耗时: {end_time - start_time:.2f}秒")
    return results


# 3. 顺序执行对比
async def sequential_example():
    """顺序执行示例（用于对比）"""
    print("\n=== 顺序执行示例 ===")
    start_time = time.time()
    
    # 依次执行
    result1 = await hello("David")
    result2 = await hello("Eve")
    result3 = await hello("Frank")
    
    end_time = time.time()
    print(f"顺序执行结果: {[result1, result2, result3]}")
    print(f"总耗时: {end_time - start_time:.2f}秒")


# 4. 任务管理示例
async def task_management_example():
    """任务创建和管理示例"""
    print("\n=== 任务管理示例 ===")
    
    # 创建任务（丢后台执行）
    task1 = asyncio.create_task(hello("Task1"))
    task2 = asyncio.create_task(hello("Task2"))
    
    print("任务已创建，继续执行其他代码...")
    
    # 等待任务完成
    result1 = await task1
    result2 = await task2
    
    print(f"任务结果: {result1}, {result2}")


# 5. 生产者消费者队列示例
async def producer(queue, name):
    """生产者函数"""
    for i in range(5):
        await asyncio.sleep(0.5)  # 模拟生产时间
        item = f"{name}-item-{i}"
        await queue.put(item)
        print(f"生产者{name}: 生产了 {item}")


async def consumer(queue, name):
    """消费者函数"""
    while True:
        item = await queue.get()
        if item is None:  # 结束信号
            queue.task_done()
            break
        await asyncio.sleep(0.3)  # 模拟消费时间
        print(f"消费者{name}: 消费了 {item}")
        queue.task_done()


async def queue_example():
    """队列使用示例"""
    print("\n=== 生产者消费者队列示例 ===")
    
    # 创建队列
    queue = asyncio.Queue(maxsize=3)
    
    # 创建生产者和消费者任务
    producers = [
        asyncio.create_task(producer(queue, "P1")),
        asyncio.create_task(producer(queue, "P2"))
    ]
    
    consumers = [
        asyncio.create_task(consumer(queue, "C1")),
        asyncio.create_task(consumer(queue, "C2"))
    ]
    
    # 等待生产者完成
    await asyncio.gather(*producers)
    
    # 发送结束信号
    for _ in consumers:
        await queue.put(None)
    
    # 等待消费者完成
    await asyncio.gather(*consumers)
    print("队列示例完成")


# 6. 错误处理示例
async def risky_operation(should_fail=False):
    """可能出错的操作"""
    if should_fail:
        raise ValueError("这是一个测试错误")
    await asyncio.sleep(0.1)
    return "操作成功"


async def error_handling_example():
    """错误处理示例"""
    print("\n=== 错误处理示例 ===")
    
    try:
        # 正常操作
        result1 = await risky_operation(False)
        print(f"正常操作结果: {result1}")
        
        # 异常操作
        result2 = await risky_operation(True)
        print(f"异常操作结果: {result2}")
        
    except ValueError as e:
        print(f"捕获到错误: {e}")
    
    # 使用gather处理多个可能失败的任务
    tasks = [
        risky_operation(False),
        risky_operation(True),
        risky_operation(False)
    ]
    
    results = await asyncio.gather(*tasks, return_exceptions=True)
    for i, result in enumerate(results):
        if isinstance(result, Exception):
            print(f"任务{i+1}失败: {result}")
        else:
            print(f"任务{i+1}成功: {result}")


# 主函数 - 程序入口
async def main():
    """主函数，演示各种asyncio用法"""
    print("开始asyncio学习示例")
    print("=" * 50)
    
    # 1. 基本协程示例
    print("=== 基本协程示例 ===")
    result = await hello()
    print(f"基本示例结果: {result}\n")
    
    # 2. 并发执行
    await concurrent_example()
    
    # 3. 顺序执行对比
    await sequential_example()
    
    # 4. 任务管理
    await task_management_example()
    
    # 5. 队列示例
    await queue_example()
    
    # 6. 错误处理
    await error_handling_example()
    
    print("\n" + "=" * 50)
    print("所有示例完成！")


# 程序入口点
if __name__ == "__main__":
    print("Python asyncio 异步编程完整示例")
    print("作者: Lingma")
    print("用途: 学习和演示asyncio的各种用法")
    print("-" * 50)
    
    # 运行主函数
    asyncio.run(main())
