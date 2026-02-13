from contextlib import contextmanager, asynccontextmanager, suppress
import time
import os

"""
上下文管理器：自动处理"打开-关闭"这类操作，避免忘记关
"""


# 1. @contextmanager：函数转上下文（最常用）
@contextmanager
def timer(name):
    """计时器：统计代码执行时间"""
    start = time.time()
    try:
        yield  # with块里的代码在这里执行
    finally:
        print(f"{name}耗时: {time.time()-start:.2f}秒")


# 使用
with timer("查询"):
    time.sleep(0.5)  # 模拟数据库查询


# 2. 文件操作（自动关文件）
@contextmanager
def open_file(path, mode="r"):
    f = open(path, mode)
    try:
        yield f
    finally:
        f.close()  # 自动关闭


# 使用
with open_file("test.txt", "w") as f:
    f.write("hello")


# 3. 临时改环境变量（用完恢复）
@contextmanager
def set_env(key, value):
    import os

    old = os.environ.get(key)
    os.environ[key] = value
    try:
        yield
    finally:
        if old is None:
            del os.environ[key]
        else:
            os.environ[key] = old


# 使用
with set_env("DEBUG", "true"):
    print(os.environ["DEBUG"])  # true
# 自动恢复原值


def create_connection():
    pass


# 4. @asynccontextmanager：异步版（数据库连接）
@asynccontextmanager
async def db_connection():
    conn = await create_connection()  # 假设这是异步创建连接
    try:
        yield conn
    finally:
        await conn.close()  # 自动关闭


# 使用
async def get_data():
    async with db_connection() as conn:
        return await conn.execute("SELECT * FROM users")


# 5. suppress：忽略指定异常（不用try/except）
with suppress(FileNotFoundError):
    os.remove("不存在的文件")  # 文件不存在也不会报错


# 6. 数据库事务（自动回滚）
@contextmanager
def transaction(db):
    try:
        yield db
        db.commit()  # 没异常就提交
    except Exception as e:
        db.rollback()  # 有异常就回滚
        raise e


# 使用
# with transaction(db) as conn:
#     conn.execute("UPDATE users SET age=26 WHERE id=1")

"""
记住：
- @contextmanager: 把函数变with，yield上下是进入/退出
- suppress: 忽略异常，少写try/except
- 异步用@asynccontextmanager + async with
"""
