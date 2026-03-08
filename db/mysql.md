基本使用:
登录连接
mysql -P 3306 -u user -p 
修改当前登录用户的密码
ALTER USER USER() IDENTIFIED BY '新密码';
CREATE DATABASE db;
SHOW CREATE DATABASE db;
SHOW DATABASES
DROP DATABASE db;
DROP DATABASE IF EXISTS db;
USE db;
SHOW TABLES;;
SELECT DATABASE();
CREATE TABLE student(
  employee_id INT NOT NULL UNIQUE,
  id INT PRIMARY KEY AUTO_INCREMENT 
  name VARCHAR(20) NOT NULL DEFAULT '',
  grades FLOAT NOT NULL DEFAULT '0.0'
  -- 合并声明主键
  PRIMARY KEY (employee_id, id)
);
CREATE TABLE orders(
  order_id INT NOT NULL PRIMARY KEY,
  order_number INT NOT NULL,
  customer_id INT,
  FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
  );
CREATE TABLE products(
  product_id INT NOT NULL PRIMARY KEY,
  product_name VARCHAR(100) NOT NULL,
  -- 总共10位数，小数部分占两位，整数部分占8位
  price DECIMAL(10, 2) CHECK (price >= 0)
);
SHOW CREATE TABLE student;
DESC student;
SELECT * FROM student;
INSERT INTO student(id, name, grades) VALUES(01, '张三', 90);
UPDATE student
SET id = 02, grades = 95
WHERE name = '张三';
-- AND OR NOT
-- NULL -> (IS, IS NOT)
DELETE FROM student WHERE name = '张三';
DROP TABLE student;
SELECT name, grades AS '成绩' FROM student;
SELECT DISTINCT name, grades, id FROM student;
SELECT name, grades, id FROM student LIMIT 2;
SELECT name, grades FROM student WHERE name LIKE '%三';
SELECT * FROM employees ORDER BY department ASC, salary DESC;
CREATE INDEX idx_name ON student(name);
ALTER TABLE student
ADD COLUMN email VARCHAR(100),
MODIFY COLUMN salary DECIMAL(10, 2),
DROP COLUMN email,
RENAME COLUMN name TO nickname,
ADD PRIMARY KEY (id);
-- 删除数据，但保留结构
TRUNCATE TABLE student;
--分组后过滤
SELECT column1, column2
FROM table_name
WHERE condition
GROUP BY column
HAVING condition;
-- 事务
-- 原子性、一致性、隔离性、持久性
BEGIN TRANSACTION;
UPDATE accounts SET balance = balance - 1000 WHERE user_id = 1;
COMMIT; -- 提交，结束事务，永久保存
ROLLBACK； -- 回滚: 撤销所有操作，回到事务前
数据库用户权限:
-- GRANT用于授予用户或角色对数据库对象的访问权限
-- 授予表权限
GRANT SELECT, INSERT, UPDATE ON employees TO user1;

-- 授予所有权限
GRANT ALL PRIVILEGES ON employees TO user1;

-- 授予数据库所有表的权限
GRANT SELECT ON database_name.* TO user1;

-- 授予存储过程执行权限
GRANT EXECUTE ON PROCEDURE get_employee TO user1;

-- 授予角色给用户
GRANT admin_role TO user1;

-- 允许用户将自己权限授予他人
GRANT SELECT ON employees TO user1 WITH GRANT OPTION;

-- REVOKE用于撤销之前授予的权限
-- 撤销特定权限
REVOKE INSERT, UPDATE ON employees FROM user1;

-- 撤销所有权限
REVOKE ALL PRIVILEGES ON employees FROM user1;

-- 撤销GRANT OPTION权限
REVOKE GRANT OPTION FOR SELECT ON employees FROM user1;

-- 撤销角色
REVOKE admin_role FROM user1;


