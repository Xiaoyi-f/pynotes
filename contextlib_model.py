from contextlib import contextmanager, asynccontextmanager, closing, suppress
import os
import asyncio
import time

# 模拟数据库连接类
class MockConnection:
    async def execute(self, query):
        print(f"执行查询: {query}")
        await asyncio.sleep(0.1)  # 模拟异步操作
        return "查询结果"
    
    async def close(self):
        print("关闭数据库连接")

async def create_connection():
    """模拟创建数据库连接"""
    await asyncio.sleep(0.1)  # 模拟连接建立的延迟
    return MockConnection()
# ============ 1. @contextmanager：函数转上下文管理器（最常用） ============
@contextmanager
def open_file(path, mode='r'):
    """不用写类，yield上一句是进入，下一句是退出"""
    f = open(path, mode)
    print(">>> 打开文件")
    try:
        yield f  # with块执行到这里
    finally:
        f.close()  # 无论是否异常，都会执行
        print("<<< 关闭文件")

# 使用示例（在main函数中演示）
# with open_file('test.txt') as f:
#     print(f.read())  # 自动关，不用写f.close()


# ============ 2. @asynccontextmanager：异步版（数据库/Redis） ============
@asynccontextmanager
async def get_db_connection():
    """异步上下文，await配合用"""
    conn = await create_connection()
    print(">>> 连接数据库")
    try:
        yield conn
    finally:
        await conn.close()
        print("<<< 关闭连接")

# 异步使用示例
async def db_example():
    async with get_db_connection() as conn:
        result = await conn.execute('SELECT 1')
        print(f"查询结果: {result}")


# ============ 3. closing：自动调用close() ============
from urllib.request import urlopen

# 不用closing（注意：urlopen示例需要网络连接）
# with urlopen('https://python.org') as f:  # 不是所有对象都支持with
#     print(f.read())

# 用closing示例（需要网络连接，这里注释掉）
# from contextlib import closing
# with closing(urlopen('https://python.org')) as f:  # 退出自动f.close()
#     print(f.read())


# ============ 4. suppress：忽略指定异常 ============
from contextlib import suppress

# 不用suppress
try:
    os.remove('somefile.tmp')
except FileNotFoundError:
    pass

# 用suppress（3行变1行）
with suppress(FileNotFoundError):
    os.remove('somefile.tmp')


# ============ 5. 实战：临时修改环境变量 ============
@contextmanager
def set_env(key, value):
    """临时改环境变量，用完自动恢复"""
    import os
    old_value = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old_value is None:
            del os.environ[key]
        else:
            os.environ[key] = old_value

# 使用
with set_env('DEBUG', 'true'):
    print(os.environ['DEBUG'])  # true
print(os.environ.get('DEBUG'))  # 恢复原值


# ============ 6. 实战：计时器 ============
@contextmanager
def timer(name):
    """代码块执行耗时"""
    start = time.time()
    try:
        yield
    finally:
        end = time.time()
        print(f"{name}: {end - start:.4f}秒")

# 使用
with timer('排序'):
    sorted([3, 1, 4, 1, 5, 9, 2, 6])


# ============ 7. 完整运行示例 ============
def main():
    """主函数：演示所有contextlib功能"""
    print("=== ContextLib 上下文管理器完整示例 ===\n")
    
    # 1. 基本文件操作
    print("1. 基本文件上下文管理器:")
    try:
        with open('test.txt', 'w') as f:
            f.write('Hello ContextLib!')
        
        with open_file('test.txt') as f:
            content = f.read()
            print(f"读取内容: {content}")
    except Exception as e:
        print(f"文件操作示例跳过: {e}")
    
    print()
    
    # 2. 环境变量管理
    print("2. 环境变量临时修改:")
    original_debug = os.environ.get('DEBUG')
    with set_env('DEBUG', 'true'):
        print(f"临时DEBUG值: {os.environ.get('DEBUG')}")
    print(f"恢复后DEBUG值: {os.environ.get('DEBUG', '未设置')}")
    
    print()
    
    # 3. 计时器
    print("3. 代码执行计时:")
    with timer('列表排序'):
        data = list(range(1000, 0, -1))
        sorted_data = sorted(data)
    
    print()
    
    # 4. 异常抑制
    print("4. 异常抑制示例:")
    with suppress(FileNotFoundError):
        os.remove('不存在的文件.txt')
        print("文件删除成功（如果存在的话）")
    
    print()
    
    # 5. 异步示例
    print("5. 异步上下文管理器:")
    try:
        asyncio.run(db_example())
    except Exception as e:
        print(f"异步示例执行失败: {e}")
    
    print()
    print("=== 所有示例演示完成 ===")

if __name__ == '__main__':
    main()