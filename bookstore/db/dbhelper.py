import sqlite3

DB_FILE = "./db/database.db"


def create_tables():
    file_name = "./db/store-schema.sql"
    with open(file_name, "r", encoding="utf-8") as file:
        sql = file.read()
        conn = sqlite3.connect(DB_FILE)
        try:
            conn.executescript(sql)
            print("数据库初始化成功")
        except Exception as e:
            print("数据库初始化失败")
            print(e)
        finally:
            conn.close()


def load_data():
    file_name = "./db/store-dataload.sql"
    with open(file_name, "r", encoding="utf-8") as file:
        sql = file.read()
        conn = sqlite3.connect(DB_FILE)
        try:
            conn.executescript(sql)
            print("数据库插入成功")
        except Exception as e:
            print("数据库插入失败")
            print(e)
        finally:
            conn.close()
