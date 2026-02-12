from pymysql import *

def init_database():
    try:
        # 创建数据库连接
        conn = connect(host='localhost', port=3306, user='root', password='mysql', charset='utf8')
        cursor = conn.cursor()
        
        # 创建数据库
        cursor.execute("CREATE DATABASE IF NOT EXISTS stock DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print("数据库创建成功")
        
        # 切换到stock数据库
        cursor.execute("USE stock")
        
        # 创建info表
        create_info_table = """
        CREATE TABLE IF NOT EXISTS info (
            id INT PRIMARY KEY AUTO_INCREMENT,
            code VARCHAR(20) NOT NULL UNIQUE,
            short VARCHAR(50),
            chg VARCHAR(20),
            turnover VARCHAR(20),
            price VARCHAR(20),
            highs VARCHAR(20),
            note_info VARCHAR(100),
            time DATE
        )
        """
        cursor.execute(create_info_table)
        print("info表创建成功")
        
        # 创建focus表
        create_focus_table = """
        CREATE TABLE IF NOT EXISTS focus (
            id INT PRIMARY KEY,
            note_info VARCHAR(100),
            FOREIGN KEY (id) REFERENCES info(id) ON DELETE CASCADE
        )
        """
        cursor.execute(create_focus_table)
        print("focus表创建成功")
        
        # 插入示例数据
        sample_data = [
            (1, '000007', '全新好', '10.00%', '5.25%', '12.50', '13.80', '优质股票', '2024-01-01'),
            (2, '000001', '平安银行', '2.50%', '3.15%', '11.20', '11.80', '银行股', '2024-01-02'),
            (3, '000002', '万科A', '-1.20%', '2.80%', '8.50', '9.20', '地产股', '2024-01-03'),
            (4, '000004', '国华网安', '5.60%', '4.30%', '15.20', '16.50', '科技股', '2024-01-04'),
            (5, '000005', '世纪星源', '3.20%', '1.85%', '6.80', '7.50', '小盘股', '2024-01-05')
        ]
        
        insert_sql = """
        INSERT INTO info (id, code, short, chg, turnover, price, highs, note_info, time)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
        short=VALUES(short), chg=VALUES(chg), turnover=VALUES(turnover), 
        price=VALUES(price), highs=VALUES(highs), note_info=VALUES(note_info), time=VALUES(time)
        """
        
        cursor.executemany(insert_sql, sample_data)
        conn.commit()
        print("示例数据插入成功")
        
        # 插入一些关注的股票
        focus_data = [
            (1, '关注中'),
            (2, '长期持有')
        ]
        
        insert_focus_sql = """
        INSERT INTO focus (id, note_info)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE note_info=VALUES(note_info)
        """
        
        cursor.executemany(insert_focus_sql, focus_data)
        conn.commit()
        print("关注数据插入成功")
        
        cursor.close()
        conn.close()
        print("数据库初始化完成！")
        
    except Exception as e:
        print(f"数据库初始化失败: {e}")
        if 'conn' in locals():
            conn.rollback()
            cursor.close()
            conn.close()

if __name__ == '__main__':
    init_database()