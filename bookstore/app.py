from flask import Flask, request, session, render_template, redirect, url_for, flash
from exts import db
from flask_wtf import CSRFProtect
from forms import CustomerRegForm, LoginForm
from models import Customer, Goods, Orders, OrderLineItem
from commands import init_app
import config
import random
import datetime

app = Flask(__name__)
app.config.from_object(config)
csrf = CSRFProtect()
csrf.init_app(app)
db.init_app(app)
init_app(app)


# 客户注册
@app.route("/reg/", methods=["GET", "POST"])
def register():
    form = CustomerRegForm()
    if request.method == "POST":
        if form.validate():
            new_customer = Customer()
            new_customer.id = form.userid.data
            new_customer.name = form.name.data
            new_customer.password = form.password.data
            new_customer.address = form.address.data
            new_customer.birthday = form.birthday.data
            new_customer.phone = form.phone.data
            db.session.add(new_customer)
            db.session.commit()
            print("注册成功")
            return render_template("customer_reg_success.html", form=form)
    return render_template("customer_reg.html", form=form)


# 客户登录
@app.route("/")
@app.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            c = db.session.query(Customer).filter_by(id=form.userid.data).first()
            if c is not None and c.password == form.password.data:
                print("登录成功")
                customer = {}
                customer["id"] = c.id
                customer["name"] = c.name
                customer["password"] = c.password
                customer["address"] = c.address
                customer["phone"] = c.phone
                customer["birthday"] = c.birthday
                session["customer"] = customer
                return redirect(url_for("main"))
        else:
            flash("您输入的客户账号和密码错误.")
            return render_template("login.html", form=form)
    return render_template("login.html", form=form)


# 登录成功后的主页面
@app.route("/main/")
def main():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    return render_template("main.html")


# 商品列表
@app.route("/list/")
def show_goods_list():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    goodslist = db.session.query(Goods).all()
    return render_template("goods_list.html", list=goodslist)


# 商品详细
@app.route("/detail/")
def show_goods_detail():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    goodsid = request.args["id"]
    goods = db.session.query(Goods).filter_by(id=goodsid).first()
    return render_template("goods_detail.html", goods=goods)


# 添加购物车
@app.route("/add/")
def add_cart():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    goodsid = int(request.args["id"])
    goodsname = request.args["name"]
    goodsprice = float(request.args["price"])
    if "cart" not in session.keys():
        session["cart"] = []
    cart = session["cart"]
    flag = 0
    for item in cart:
        if item[0] == goodsid:
            item[3] += 1
            flag = 1
            break
    if flag == 0:
        cart.append([goodsid, goodsname, goodsprice, 1])
    session["cart"] = cart
    print(cart)
    flash("已经添加商品【" + goodsname + "】到购物车")

    return redirect(url_for("show_goods_list"))


# 查看购物车
@app.route("/cart/")
def show_cart():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    if "cart" not in session.keys():
        return render_template("cart.html", list=[], total=0.0)
    cart = session["cart"]
    list = []
    total = 0.0
    for item in cart:
        subtotal = item[2] * item[3]
        total += subtotal
        new_item = (item[0], item[1], item[2], item[3], subtotal)
        list.append(new_item)
    return render_template("cart.html", list=list, total=total)


# 提交订单
@app.route("/submit_order/", methods=["POST"])
def submit_order():
    orders = Orders()
    n = random.randint(0, 9)
    d = datetime.datetime.today()
    orderid = int(d.timestamp() * 1e6) + n
    orders.id = orderid
    orders.orderdate = d.strftime("%Y-%m-%d %H:%M:%S")
    orders.status = 1
    db.session.add(orders)
    cart = session["cart"]
    total = 0.0
    for item in cart:
        quantity = request.form["quantity_" + str(item[0])]
        try:
            quantity = int(quantity)
        except:
            quantity = 0
        subtotal = item[2] * quantity
        total += subtotal
        order_line_item = OrderLineItem()
        order_line_item.quantity = quantity
        order_line_item.goods_id = item[0]
        order_line_item.orders_id = orderid
        order_line_item.subtotal = subtotal
        db.session.add(order_line_item)
    orders.total = total
    db.session.commit()
    session.pop("cart", None)
    return render_template("order_finish.html", orderid=orderid)


# 客户账户
@app.route("/user/")
def show_user():
    if "customer" not in session.keys():
        flash("您还没有登录,请登录.")
        return redirect(url_for("login"))
    name = session["customer"]["name"]
    user = db.session.query(Customer).filter_by(name=name).first()
    return render_template("user.html", user=user)


if __name__ == "__main__":
    app.run(debug=True)
