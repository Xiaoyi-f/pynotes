-- 按照默认编码与默认规则创建数据库
CREATE DATABASE db1;

-- 查看创建数据库时的信息
SHOW CREATE DATABASE db1;

-- 显示所有数据库
SHOW DATABASES;

-- 这个是注释

-- 删除数据库 -> 非常危险的操作
DROP DATABASE db1;

DROP DATABASE IF EXISTS db1;

-- 进入使用数据库
USE db1;

-- 展示表
SHOW TABLES;

-- 恢复备份数据库 -》 mysqldump -u root -P 3306 -p 数据库名 > 备份文件路径/名字.sql
-- SOURCE /home/mysql/db1.sql;

-- 查询当前所在的数据库 -> Mysql内置函数
SELECT DATABASE();

-- 唯一标识表中的每一行记录。PRIMARY KEY 约束是 NOT NULL 和 UNIQUE 的结合
-- 主键只能有一个
-- 创建数据表
CREATE TABLE student(
    EmployeeID INT NOT NULL UNIQUE,
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(20) NOT NULL DEFAULT '',
    grades FLOAT NOT NULL DEFAULT '0.0' --,
    -- PRIMARY KEY (id)
    -- PRIMARY KEY (order_id, product_id)  -- 两个列组成复合主键
);

-- 外键
CREATE TABLE Orders (
    OrderID INT NOT NULL PRIMARY KEY,
    OrderNumber INT NOT NULL,
    CustomerID INT,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

-- CHECK
CREATE TABLE Products (
    ProductID INT NOT NULL PRIMARY KEY,
    ProductName VARCHAR(100) NOT NULL,
    Price DECIMAL(10, 2) CHECK (Price >= 0)
);

SHOW CREATE TABLE student;

-- 查看数据结构
DESC student;

-- 查看
SELECT * FROM student;

-- 插入数据
INSERT INTO student(id, name, grades) VALUES(01, '张三', 90);
INSERT INTO student(id, name, grades) VALUES(02, '王五', 88.5);

-- 修改数据
UPDATE student
SET id = 001, grades = 90.5
WHERE name = '张三';

-- 删除行
DELETE FROM student WHERE name = '张三';

-- 删除表
DROP TABLE student;

-- 选择查询
SELECT name, grades AS '成绩' FROM student;

-- 去重查询
SELECT DISTINCT name, grades, id FROM student;

-- 截断查询
SELECT name, grades, id FROM student LIMIT 2;

-- AND OR NOT
-- NULL只能使用IS, IS NOT检验

-- 模糊查询
SELECT name, grades FROM student WHERE name LIKE '%三';

-- 排序
SELECT * FROM employees ORDER BY department ASC, salary DESC; -- 先按部门升序，同部门内按薪水降序

-- 索引是一种高效获取数据的数据结构 -> B+树
CREATE INDEX idx_name ON student(name);

-- ALTER用于修改现有数据库对象（表、视图、索引等）的结构

-- 添加新列
ALTER TABLE employees
ADD COLUMN email VARCHAR(100);

-- 修改列数据类型
ALTER TABLE employees
ALTER COLUMN salary DECIMAL(10,2);

-- MySQL修改列
ALTER TABLE employees
MODIFY COLUMN salary DECIMAL(12,2);

-- 删除列
ALTER TABLE employees
DROP COLUMN email;

-- 重命名列
ALTER TABLE employees
RENAME COLUMN old_name TO new_name;

-- 添加主键
ALTER TABLE employees
ADD PRIMARY KEY (id);

-- 添加外键
ALTER TABLE orders
ADD CONSTRAINT fk_customer
FOREIGN KEY (customer_id) REFERENCES customers(id);

-- 删除约束
ALTER TABLE employees
DROP CONSTRAINT pk_employee;

-- TRUNCATE用于快速删除表中的所有数据，但保留表结构
-- 删除所有数据
TRUNCATE TABLE employees;

-- 带有重置自增列（MySQL）
TRUNCATE TABLE employees AUTO_INCREMENT = 1;

-- 级联删除（PostgreSQL）
TRUNCATE TABLE employees CASCADE;

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

-- 分组后过滤
SELECT column1, aggregate_function(column2)
FROM table_name
WHERE condition
GROUP BY column1
HAVING condition_on_aggregate;

-- 事务

-- 特性	        中文	        通俗解释	             例子
-- Atomicity	原子性	要么全做，要么全不做	转账必须两步都完成或都取消
-- Consistency	一致性	数据始终符合规则	    转账前后总金额不变
-- Isolation	隔离性	多个事务互不干扰	    你转账时别人查余额看到的是转账前的状态
-- Durability	持久性	一旦提交永久保存	转账成功，即使断电也不会丢失

-- 方法1：显式事务（推荐新手用）
BEGIN TRANSACTION;  -- 开始事务
-- 或者简写：BEGIN
-- 或者：START TRANSACTION（MySQL）

-- 执行你的SQL操作
UPDATE accounts SET balance = balance - 1000 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 1000 WHERE user_id = 2;

-- 结束事务
COMMIT;  -- 提交：永久保存
-- 或
ROLLBACK;  -- 回滚：撤销所有操作，回到事务前

-- 更改密码和查看用户不同数据库命令不同，自行使用时问AI即可