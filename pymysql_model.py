import pymysql
from dbutils.pooled_db import PooledDB


# 连接池（必用！）
class MySQLPool:
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=10,  # 最大连接数
            host="localhost",  # ⚠️改成你的
            user="root",  # ⚠️改成你的
            password="123456",  # ⚠️改成你的
            database="test_db",  # ⚠️改成你的
            charset="utf8mb4",
            cursorclass=pymysql.cursors.DictCursor,  # 让查询结果返回字典
        )

    def execute(self, sql, args=None):
        conn = self.pool.connection()
        try:
            with conn.cursor() as cur:
                cur.execute(sql, args or ())
                if sql.strip().upper().startswith("SELECT"):
                    return cur.fetchall()  # 获取所有查询结果返回
                conn.commit()
                return cur.lastrowid or cur.rowcount
                # lastrowid：插入数据时，返回新数据的ID
                # rowcount：更新/删除时，返回影响了多少行
        finally:
            conn.close()  # 归还到池


# 全局用这一个
db = MySQLPool()


# 增删改查（工作够用）
# 查询
users = db.execute("SELECT * FROM users WHERE age > %s", (18,))

# 插入
user_id = db.execute("INSERT INTO users (name,age) VALUES (%s,%s)", ("张三", 25))

# 更新
db.execute("UPDATE users SET age=%s WHERE name=%s", (26, "张三"))

# 删除
db.execute("DELETE FROM users WHERE age < %s", (18,))


# 分页查询
def get_page(page=1, size=10):
    offset = (page - 1) * size
    return db.execute(
        "SELECT * FROM users ORDER BY id LIMIT %s OFFSET %s", (size, offset)
    )


# 批量插入（高性能）
def batch_insert(data):
    """data = [(name,age), ...]"""
    conn = db.pool.connection()
    try:
        with conn.cursor() as cur:
            cur.executemany("INSERT INTO users (name,age) VALUES (%s,%s)", data)
            conn.commit()
            return cur.rowcount
    finally:
        conn.close()


# 事务（要么全成功要么全失败）
def transfer(from_id, to_id, amount):
    """转账示例"""
    conn = db.pool.connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE accounts SET balance=balance-%s WHERE id=%s AND balance>=%s",
                (amount, from_id, amount),
            )
            if cur.rowcount == 0:
                raise Exception("余额不足")

            cur.execute(
                "UPDATE accounts SET balance=balance+%s WHERE id=%s", (amount, to_id)
            )
            conn.commit()
            return True
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


"""
重点说明:
1. 连接池：db.execute(sql, args)  # 所有操作都用这个
2. 防注入：永远用%s，别拼字符串 
    sql：你要执行的SQL语句（用 %s 占位）
    args：要替换 %s 的具体数据（防SQL注入）
3. 事务：一个连接里执行多条SQL，最后commit/rollback
"""
