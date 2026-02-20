import sqlite3

DB_FILE = "./db/database.db"

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

try:
    # 更新商品图片字段
    updates = [
        (1, 'book1.jpg'),
        (2, 'book2.jpg'),
        (3, 'book3.jpg'),
        (4, 'book4.jpg'),
        (5, 'book5.jpg')
    ]
    
    for goods_id, image_name in updates:
        cursor.execute("UPDATE goods SET image = ? WHERE goods_id = ?", (image_name, goods_id))
        print(f"Updated goods_id {goods_id} to image {image_name}")
    
    conn.commit()
    print("\n数据库更新成功！")
    
except Exception as e:
    print(f"数据库更新失败: {e}")
    conn.rollback()
finally:
    conn.close()