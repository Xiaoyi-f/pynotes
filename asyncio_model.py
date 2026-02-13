import asyncio
import aiohttp  # 异步HTTP库，需要安装：pip install aiohttp

"""
异步IO解决什么问题？
- 场景：爬虫、API调用、数据库查询等IO密集型任务
- 优势：一个线程内切换任务，比多线程更轻量
- 核心：遇到IO等待就切走，不闲着
"""


# 1. 基础协程函数（async def定义）
async def fetch_url(url):
    """异步获取网页内容（最常用）"""
    print(f"开始请求: {url}")
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.text()  # await等待IO


# 2. 并发请求（核心用法）
async def fetch_all():
    """同时请求多个网址"""
    urls = [
        "http://httpbin.org/delay/1",  # 这个接口会延迟1秒
        "http://httpbin.org/delay/2",
        "http://httpbin.org/delay/3",
    ]

    # 创建任务（立即开始执行）
    tasks = [asyncio.create_task(fetch_url(url)) for url in urls]

    # 等待所有任务完成
    results = await asyncio.gather(*tasks)
    return results


# 3. 超时控制（必用）
async def fetch_with_timeout(url, timeout=5):
    """带超时的请求"""
    try:
        # async with timeout:  Python 3.11+写法
        # 旧版本用 asyncio.wait_for
        async with asyncio.timeout(timeout):
            return await fetch_url(url)
    except asyncio.TimeoutError:
        print(f"请求超时: {url}")
        return None


# 4. 限制并发数（防止被封）
async def fetch_with_semaphore():
    """最多同时请求3个"""
    semaphore = asyncio.Semaphore(3)
    urls = ["http://httpbin.org/delay/1" for _ in range(10)]

    async def fetch_one(url):
        async with semaphore:  # 拿令牌，最多3个同时
            return await fetch_url(url)

    tasks = [fetch_one(url) for url in urls]
    return await asyncio.gather(*tasks)


# 5. 生产消费者模式（爬虫常用）
async def producer_consumer():
    """队列：爬取URL，处理结果"""
    queue = asyncio.Queue()
    urls = ["url1", "url2", "url3"]  # 要爬的网址

    # 生产者：不断放URL
    async def producer():
        for url in urls:
            await queue.put(url)
            await asyncio.sleep(0.1)
        # 放结束信号
        for _ in range(3):
            await queue.put(None)

    # 消费者：不断取URL爬取
    async def consumer(cid):
        while True:
            url = await queue.get()
            if url is None:
                break
            print(f"消费者{cid}爬取: {url}")
            # 这里调用fetch_url
            await asyncio.sleep(0.5)  # 模拟爬取
            queue.task_done()

    # 启动生产者和3个消费者
    tasks = [
        asyncio.create_task(producer()),
        *[asyncio.create_task(consumer(i)) for i in range(3)],
    ]
    await asyncio.gather(*tasks)


# 6. 实际工作模板（复制即用）
async def batch_fetch_urls(urls, max_concurrent=5, timeout=10):
    """
    批量获取URL内容
    :param urls: URL列表
    :param max_concurrent: 最大并发数
    :param timeout: 每个请求超时时间
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch(session, url):
        async with semaphore:
            try:
                async with asyncio.timeout(timeout):
                    async with session.get(url) as resp:
                        return {
                            "url": url,
                            "status": resp.status,
                            "data": await resp.text(),
                        }
            except Exception as e:
                return {"url": url, "error": str(e)}

    async with aiohttp.ClientSession() as session:
        tasks = [fetch(session, url) for url in urls]
        return await asyncio.gather(*tasks)


# 使用示例
async def main():
    urls = ["http://example.com" for _ in range(10)]
    results = await batch_fetch_urls(urls, max_concurrent=3)
    for r in results:
        print(f"{r['url']}: {r.get('status', 'error')}")


# 运行
if __name__ == "__main__":
    asyncio.run(main())

"""
记住4个核心：
1. 定义: async def 函数名
2. 等待: await 协程()  # 等结果
3. 并发: asyncio.gather(*任务列表)  # 一起执行
4. 限制: Semaphore(并发数)  # 控制数量
"""
