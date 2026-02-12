import aiohttp
import asyncio


# 1. GET请求（取数据）
async def get_example():
    async with aiohttp.ClientSession() as session:
        async with session.get("https://api.github.com") as resp:
            return await resp.json()  # .text() .read()


# 2. POST请求（发数据）
async def post_example():
    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://httpbin.org/post", json={"key": "value"}
        ) as resp:  # 自动JSON
            return await resp.json()


# 3. 超时（别死等）
async def with_timeout():
    timeout = aiohttp.ClientTimeout(total=5)  # 5秒
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get("https://example.com") as resp:
            return await resp.text()


# 4. 并发（批量请求）
async def fetch_many(urls):
    async with aiohttp.ClientSession() as session:
        tasks = [session.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [await r.text() for r in responses]


# 5. 异常处理（别崩）
async def safe_get(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as resp:
                if resp.status == 200:
                    return await resp.text()
                return f"错误: {resp.status}"
    except (asyncio.TimeoutError, aiohttp.ClientError) as e:
        return f"请求失败: {e}"
