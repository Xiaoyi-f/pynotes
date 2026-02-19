from app import db


# 客户表
class Customer(db.Model):
    __tablename__ = "customers"
    id = db.Column("id", db.String(20), primary_key=True)
    name = db.Column("name", db.String(50), nullable=False)
    password = db.Column("password", db.String(20), nullable=False)
    address = db.Column("address", db.String(100))
    phone = db.Column("phone", db.String(20))
    birthday = db.Column("birthday", db.String(20))


# 商品表
class Goods(db.Model):
    __tablename__ = "goods"
    goods_id = db.Column("goods_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String(100), nullable=False)
    author = db.Column("author", db.String(30))
    press = db.Column("press", db.String(200))
    isbn = db.Column("isbn", db.String(30))
    edition = db.Column("edition", db.String(30))
    packaging = db.Column("packaging", db.String(30))
    format = db.Column("format", db.String(30))
    publication_time = db.Column("publication_time", db.String(30))
    paper = db.Column("paper", db.String(30))
    price = db.Column("price", db.String(30))
    description = db.Column("description", db.String(200))
    image = db.Column("image", db.String(100))
    # 关系定义
    order_line_items = db.relationship("OrderLineItem", backref="goods")


# 订单表
class Orders(db.Model):
    __tablename__ = "orders"
    orders_id = db.Column("orders_id", db.Integer, primary_key=True)
    order_date = db.Column("order_date", db.String(20))
    # 1表示待付款；0表示已付款
    status = db.Column("status", db.Integer, default=1)
    total = db.Column("total", db.Float)
    # 关系定义
    order_line_items = db.relationship("OrderLineItem", backref="orders")


# 详细订单表
class OrderLineItem(db.Model):
    __tablename__ = "order_line_items"
    id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
    goods_id = db.Column(
        "goods_id", db.Integer, db.ForeignKey("goods.goods_id"), nullable=False
    )
    orders_id = db.Column(
        "orders_id", db.Integer, db.ForeignKey("orders.orders_id"), nullable=False
    )
    quantity = db.Column("quantity", db.Integer)
    sub_total = db.Column("sub_total", db.Float)
