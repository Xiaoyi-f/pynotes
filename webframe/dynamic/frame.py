import re
from pymysql import *
import json

FUNC_URL_LIST = {}


# 路由装饰器 向字典里自动添加数据
def route(data):
    def func_out(func):
        FUNC_URL_LIST[data] = func
        return func
    return func_out


@route("/index.html")
def index():
    with open("./template/index.html", encoding="utf-8") as f:
        content = f.read()

    html = ""
    try:
        # 创建链接
        conn = connect(host='localhost', port=3306, database='stock', user='root', password='mysql', charset='utf8')
        # 创建游标
        cursor = conn.cursor()

        # 执行sql语句
        sql = "select * from info;"
        cursor.execute(sql)

        # 获取数据 元组  ((),())
        stock_data = cursor.fetchall()

        template = """
    <tr>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>
            <input type="button" value="添加" id="toAdd" name="toAdd" systemidvaule="000007">
        </td>
</tr>
    """

        for i in stock_data:
            html += template % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7])

        cursor.close()
        conn.close()
    except Exception as e:
        html = "<tr><td colspan='9' style='text-align:center;color:red;'>数据库连接失败: " + str(e) + "</td></tr>"

    # 通过正则进行替换
    # 1 被替换的局部内容(r:保持代码原始的意思)
    # 2 被替换的整体内容　
    # 3 替换内容　
    content = re.sub(r"{%content%}", html, content)

    return content


@route("/center.html")
def center():
    with open("./template/center.html", encoding="utf-8") as f:
        content = f.read()
    # # 创建链接
    # conn = connect(host='localhost', port=3306, database='stock', user='root', password='mysql', charset='utf8')
    # # 创建游标
    # cursor = conn.cursor()
    #
    # # 执行sql语句
    # sql = "select *  from info inner join focus on info.id=focus.id;"
    # cursor.execute(sql)
    #
    # # 获取数据 元组  ((),())
    # stock_data = cursor.fetchall()
    # # 关闭链接
    #
    # html = ""
    # template = """
    # <tr>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>%s</td>
    #         <td>
    #             <a type="button" class="btn btn-default btn-xs" href="/update/000007.html"> <span class="glyphicon glyphicon-star" aria-hidden="true"></span> 修改 </a>
    #         </td>
    #         <td>
    #             <input type="button" value="删除" id="toDel" name="toDel" systemidvaule="000007">
    #         </td>
    #     </tr>
    # """
    # # 组合数据
    # for i in stock_data:
    #     html += template % (i[1], i[2], i[3], i[4], i[5], i[6], i[9])
    # # 替换数据
    # content = re.sub(r"{%content%}", html, content)
    # # 关闭连接
    # cursor.close()
    # conn.close()
    # 返回数据
    return content


# ajax请求的数据
@route("/center_data.html")
def center_data():
    try:
        # 创建链接
        conn = connect(host='localhost', port=3306, database='stock', user='root', password='mysql', charset='utf8')
        # 创建游标
        cursor = conn.cursor()

        # 执行sql语句
        sql = "select *  from info inner join focus on info.id=focus.id;"
        cursor.execute(sql)

        # 获取数据 元组  ((),())
        stock_data = cursor.fetchall()

        # 把元组转化成列表
        center_data_list = [{"code":row[1],
                             "short":row[2],
                             "chg":row[3],
                             "turnover":row[4],
                             "price":str(row[5]),
                             "highs":str(row[6]),
                             "note_info":row[9]}for row in stock_data]

        # 把列表转化成json字符串
        # ensure_ascii = False 控制台中可以显示中文
        json_str = json.dumps(center_data_list, ensure_ascii=False)

        # 关闭连接
        cursor.close()
        conn.close()

        return json_str
    except Exception as e:
        # 返回错误信息的JSON
        error_data = [{"error": str(e)}]
        return json.dumps(error_data, ensure_ascii=False)


# 解耦合
def application(env):
    request_path = env["request_path"]
    try:
        # index               /index.py
        func = FUNC_URL_LIST[request_path]
        ret = func()
        return ret
    except Exception as e:
        print(e)
        return "404 not found..."