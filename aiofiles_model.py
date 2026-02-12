import aiofiles
import asyncio

async def main():
    # 读
    async with aiofiles.open('input.txt', 'r') as f:
        content = await f.read()

    # 写
    async with aiofiles.open('output.txt', 'w') as f:
        await f.write(content.upper())

    # 追加
    async with aiofiles.open('log.txt', 'a') as f:
        await f.write('done\n')

    # 二进制
    async with aiofiles.open('img.jpg', 'rb') as f:
        data = await f.read()

asyncio.run(main())