-- SQLite 需要先启用外键支持
-- 需要在连接后执行：
pragma foreign_keys = ON;

drop table if exists customers;
drop table if exists order_line_items;
drop table if exists goods;
drop table if exists orders;

-- 客户表
create table customers(
    id varchar(20) primary key,
    name varchar(50) not null,
    password varchar(20) not null,
    address varchar(100),
    phone varchar(20),
    birthday varchar(20)
);

-- 商品表
create table goods(
    goods_id integer primary key autoincrement,
    name varchar(100) not null,
    author varchar(30),
    press varchar(200),
    isbn varchar(30),
    edition varchar(30),
    packaging varchar(30),
    format varchar(30),
    publication_time varchar(30),
    paper varchar(30),
    price varchar(30),
    description varchar(200),
    image varchar(100)
);

-- 订单表
create table orders(
    orders_id integer primary key,
    order_date varchar(20),
    status integer default 1,
    total float
);

-- 详细订单表
create table order_line_items(
    id integer primary key autoincrement,
    -- 简写语法定义外键
    goods_id integer not null references goods(goods_id),
    orders_id integer not null references orders(orders_id),
    quantity integer,
    sub_total float
);

