import pymysql
from dbutils.pooled_db import PooledDB

# ============ PyMySQL = 操作MySQL（连接/查询/事务）============


# ------------ 1. 基础连接（别用，每次连太慢）------------
def bad_example():
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="123456",
        database="test",
        charset="utf8mb4",
    )
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data


# ------------ 2. ✅ 连接池（必用！）------------
class MySQLPool:
    """数据库连接池（生产环境用这个）"""

    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,  # 最大连接数
            mincached=2,  # 初始化空闲连接
            maxcached=5,  # 最大空闲连接
            blocking=True,  # 无连接时阻塞等待
            host="localhost",
            port=3306,
            user="root",
            password="123456",
            database="test",
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # ✅ 返回字典，不用元组
        )

    def get_conn(self):
        """从池拿连接"""
        return self.pool.connection()

    def execute(self, sql, args=None):
        """查询（返回结果）"""
        conn = self.get_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args or ())
                if sql.strip().upper().startswith("SELECT"):
                    return cur.fetchall()
                conn.commit()
                return cur.lastrowid or cur.rowcount
        finally:
            conn.close()  # 归还到池，不是真关闭


# 全局连接池（单例）
db = MySQLPool()


# ------------ 3. CRUD（增删改查）------------
def crud_examples():
    """增删改查，带参数化查询（防SQL注入）"""

    # 3.1 查询
    users = db.execute("SELECT id, name, age FROM users WHERE age > %s", (18,))
    for user in users:
        print(user["name"], user["age"])

    # 3.2 单条插入
    user_id = db.execute(
        "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)",
        ("张三", 25, "zhangsan@example.com"),
    )
    print(f"新增ID: {user_id}")

    # 3.3 批量插入（高性能）
    data = [
        ("李四", 30, "lisi@example.com"),
        ("王五", 28, "wangwu@example.com"),
        ("赵六", 22, "zhaoliu@example.com"),
    ]
    conn = db.get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)", data
            )
            conn.commit()
            print(f"批量插入: {cur.rowcount}条")
    finally:
        conn.close()

    # 3.4 更新
    rows = db.execute("UPDATE users SET age = %s WHERE name = %s", (26, "张三"))
    print(f"更新: {rows}条")

    # 3.5 删除
    rows = db.execute("DELETE FROM users WHERE age < %s", (18,))
    print(f"删除: {rows}条")


# ------------ 4. 事务（要么全成功，要么全失败）------------
def transfer_money(from_id, to_id, amount):
    """转账示例"""
    conn = db.get_conn()
    try:
        with conn.cursor() as cur:
            # 扣钱
            cur.execute(
                "UPDATE accounts SET balance = balance - %s WHERE id = %s AND balance >= %s",
                (amount, from_id, amount),
            )
            if cur.rowcount == 0:
                raise Exception("余额不足")

            # 加钱
            cur.execute(
                "UPDATE accounts SET balance = balance + %s WHERE id = %s",
                (amount, to_id),
            )

            # 记录流水
            cur.execute(
                "INSERT INTO transfers (from_id, to_id, amount) VALUES (%s, %s, %s)",
                (from_id, to_id, amount),
            )

            conn.commit()  # ✅ 提交事务
            return True
    except Exception as e:
        conn.rollback()  # ❌ 出错回滚
        raise e
    finally:
        conn.close()


# ------------ 5. 分页查询------------
def paginate_users(page=1, page_size=20):
    """分页查询"""
    offset = (page - 1) * page_size
    return db.execute(
        "SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s", (page_size, offset)
    )


# ------------ 6. 防SQL注入（必看！）------------
def sql_injection_example():
    """参数化查询防注入"""
    user_input = "'; DROP TABLE users; --"

    # ❌ 危险！绝对不要用
    # db.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

    # ✅ 安全！参数化查询
    db.execute("SELECT * FROM users WHERE name = %s", (user_input,))


# ------------ 7. 表是否存在------------
def table_exists(table_name):
    """检查表是否存在"""
    result = db.execute(
        "SELECT COUNT(*) as cnt FROM information_schema.tables WHERE table_name = %s AND table_schema = DATABASE()",
        (table_name,),
    )
    return result[0]["cnt"] > 0


# ------------ 8. 批量插入高性能版（executemany）------------
def batch_insert_users(users_list):
    """批量插入（一次网络往返）"""
    conn = db.get_conn()
    try:
        with conn.cursor() as cur:
            cur.executemany(
                "INSERT INTO users (name, age, email) VALUES (%s, %s, %s)", users_list
            )
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()


# ------------ 9. 上下文管理器（自动关）------------
class Database:
    """优雅的数据库操作类"""

    def __init__(self):
        self.pool = db.pool

    def __enter__(self):
        self.conn = self.pool.connection()
        self.cursor = self.conn.cursor(pymysql.cursors.DictCursor)
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.cursor.close()
        self.conn.close()


# 使用
def query_with_context():
    with Database() as cur:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()


# ============ 快速开始 ============
if __name__ == "__main__":
    # 1. 创建连接池
    db = MySQLPool()

    # 2. 建表
    db.execute("""
               CREATE TABLE IF NOT EXISTS users (
                                                    id INT AUTO_INCREMENT PRIMARY KEY,
                                                    name VARCHAR(50) NOT NULL,
                   age INT NOT NULL,
                   email VARCHAR(100),
                   created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                   )
               """)

    # 3. 增删改查
    crud_examples()

    # 4. 分页
    page1 = paginate_users(1, 5)
    print(f"第一页: {len(page1)}条")

    # 5. 批量插入
    users = [(f"user{i}", 20 + i, f"user{i}@test.com") for i in range(10, 20)]
    count = batch_insert_users(users)
    print(f"批量插入: {count}条")
