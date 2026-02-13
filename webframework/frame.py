import re
from pymysql import *
import json
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('webserver.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

FUNC_URL_LIST = {}

# 内存数据存储（当数据库不可用时使用）
memory_stock_data = [
    (1, '000007', '全新好', '10.00%', '5.25%', '12.50', '13.80', '2024-01-01'),
    (2, '000001', '平安银行', '2.50%', '3.15%', '11.20', '11.80', '2024-01-02'),
    (3, '000002', '万科A', '-1.20%', '2.80%', '8.50', '9.20', '2024-01-03'),
    (4, '000004', '国华网安', '5.60%', '4.30%', '15.20', '16.50', '2024-01-04'),
    (5, '000005', '世纪星源', '3.20%', '1.85%', '6.80', '7.50', '2024-01-05')
]

memory_focus_data = {
    1: '关注中',
    2: '长期持有'
}

def get_db_connection():
    try:
        conn = connect(host='localhost', port=3306, database='stock', user='root', password='mysql', charset='utf8')
        return conn, True
    except Exception as e:
        print(f"数据库连接失败，使用内存数据: {e}")
        return None, False


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
        conn, db_available = get_db_connection()
        
        if db_available:
            cursor = conn.cursor()
            sql = "select * from info;"
            cursor.execute(sql)
            stock_data = cursor.fetchall()
            cursor.close()
            conn.close()
        else:
            stock_data = memory_stock_data

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
            <input type="button" value="添加" id="toAdd" name="toAdd" systemIdVaule="%s">
        </td>
</tr>
    """

        for i in stock_data:
            html += template % (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[1])
            
    except Exception as e:
        html = "<tr><td colspan='9' style='text-align:center;color:red;'>数据加载失败: " + str(e) + "</td></tr>"

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
        conn, db_available = get_db_connection()
        
        if db_available:
            cursor = conn.cursor()
            sql = "select *  from info inner join focus on info.id=focus.id;"
            cursor.execute(sql)
            stock_data = cursor.fetchall()
            cursor.close()
            conn.close()
            
            center_data_list = [{"code":row[1],
                                 "short":row[2],
                                 "chg":row[3],
                                 "turnover":row[4],
                                 "price":str(row[5]),
                                 "highs":str(row[6]),
                                 "note_info":row[9]}for row in stock_data]
        else:
            center_data_list = []
            for stock_id, note_info in memory_focus_data.items():
                stock = next((s for s in memory_stock_data if s[0] == stock_id), None)
                if stock:
                    center_data_list.append({
                        "code": stock[1],
                        "short": stock[2],
                        "chg": stock[3],
                        "turnover": stock[4],
                        "price": stock[5],
                        "highs": stock[6],
                        "note_info": note_info
                    })

        json_str = json.dumps(center_data_list, ensure_ascii=False)
        return json_str
    except Exception as e:
        error_data = [{"error": str(e)}]
        return json.dumps(error_data, ensure_ascii=False)


# 解耦合
def application(env):
    request_path = env["request_path"]
    try:
        # 处理带参数的URL
        import re
        
        # 匹配添加股票的URL
        add_match = re.search(r"^/add/(\d+).html$", request_path)
        if add_match:
            code = add_match.group(1)
            logger.info(f"收到添加股票请求: {code}")
            conn, db_available = get_db_connection()
            
            if db_available:
                cursor = conn.cursor()
                check_sql = "select id from info where code = %s"
                cursor.execute(check_sql, (code,))
                stock_id = cursor.fetchone()
                
                if stock_id:
                    check_focus_sql = "select id from focus where id = %s"
                    cursor.execute(check_focus_sql, (stock_id[0],))
                    if not cursor.fetchone():
                        insert_sql = "insert into focus (id) values (%s)"
                        cursor.execute(insert_sql, (stock_id[0],))
                        conn.commit()
                        result = {"status": "success", "message": "添加成功"}
                        logger.info(f"股票 {code} 添加到关注列表成功")
                    else:
                        result = {"status": "info", "message": "股票已在关注列表中"}
                        logger.info(f"股票 {code} 已在关注列表中")
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
                
                cursor.close()
                conn.close()
            else:
                stock = next((s for s in memory_stock_data if s[1] == code), None)
                if stock:
                    stock_id = stock[0]
                    if stock_id not in memory_focus_data:
                        memory_focus_data[stock_id] = "关注中"
                        result = {"status": "success", "message": "添加成功"}
                        logger.info(f"内存数据: 股票 {code} 添加到关注列表成功")
                    else:
                        result = {"status": "info", "message": "股票已在关注列表中"}
                        logger.info(f"内存数据: 股票 {code} 已在关注列表中")
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
            
            return json.dumps(result, ensure_ascii=False)
        
        # 匹配删除股票的URL
        del_match = re.search(r"^/del/(\d+).html$", request_path)
        if del_match:
            code = del_match.group(1)
            logger.info(f"收到删除股票请求: {code}")
            conn, db_available = get_db_connection()
            
            if db_available:
                cursor = conn.cursor()
                check_sql = "select id from info where code = %s"
                cursor.execute(check_sql, (code,))
                stock_id = cursor.fetchone()
                
                if stock_id:
                    delete_sql = "delete from focus where id = %s"
                    cursor.execute(delete_sql, (stock_id[0],))
                    conn.commit()
                    result = {"status": "success", "message": "删除成功"}
                    logger.info(f"股票 {code} 从关注列表删除成功")
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
                
                cursor.close()
                conn.close()
            else:
                stock = next((s for s in memory_stock_data if s[1] == code), None)
                if stock:
                    stock_id = stock[0]
                    if stock_id in memory_focus_data:
                        del memory_focus_data[stock_id]
                        result = {"status": "success", "message": "删除成功"}
                        logger.info(f"内存数据: 股票 {code} 从关注列表删除成功")
                    else:
                        result = {"status": "info", "message": "股票不在关注列表中"}
                        logger.info(f"内存数据: 股票 {code} 不在关注列表中")
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
            
            return json.dumps(result, ensure_ascii=False)
        
        # 匹配修改股票备注的URL
        update_match = re.search(r"^/update/(\d+).html$", request_path)
        if update_match:
            code = update_match.group(1)
            logger.info(f"收到修改股票备注请求: {code}")
            conn, db_available = get_db_connection()
            
            if db_available:
                cursor = conn.cursor()
                check_sql = "select id, code, short, chg, turnover, price, highs from info where code = %s"
                cursor.execute(check_sql, (code,))
                stock_info = cursor.fetchone()
                
                if stock_info:
                    # 获取当前备注信息
                    get_note_sql = "select note_info from focus where id = %s"
                    cursor.execute(get_note_sql, (stock_info[0],))
                    note_result = cursor.fetchone()
                    note_info = note_result[0] if note_result else ""
                    
                    cursor.close()
                    conn.close()
                    
                    # 读取模板并替换变量
                    with open("./template/update.html", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 替换模板变量
                    content = content.replace("{{stock_code}}", code)
                    content = content.replace("{{note_info}}", note_info)
                    stock_info_str = f"代码: {stock_info[1]}, 简称: {stock_info[2]}, 涨跌幅: {stock_info[3]}, 换手率: {stock_info[4]}, 价格: {stock_info[5]}, 前期高点: {stock_info[6]}"
                    content = content.replace("{{stock_info}}", stock_info_str)
                    
                    return content
                else:
                    cursor.close()
                    conn.close()
                    return f"<h1>错误</h1><p>股票 {code} 不存在</p><a href='/center.html'>返回个人中心</a>"
            else:
                stock = next((s for s in memory_stock_data if s[1] == code), None)
                if stock:
                    stock_id = stock[0]
                    note_info = memory_focus_data.get(stock_id, "")
                    
                    # 读取模板并替换变量
                    with open("./template/update.html", encoding="utf-8") as f:
                        content = f.read()
                    
                    # 替换模板变量
                    content = content.replace("{{stock_code}}", code)
                    content = content.replace("{{note_info}}", note_info)
                    stock_info_str = f"代码: {stock[1]}, 简称: {stock[2]}, 涨跌幅: {stock[3]}, 换手率: {stock[4]}, 价格: {stock[5]}, 前期高点: {stock[6]}"
                    content = content.replace("{{stock_info}}", stock_info_str)
                    
                    return content
                else:
                    return f"<h1>错误</h1><p>股票 {code} 不存在</p><a href='/center.html'>返回个人中心</a>"
        
        # 匹配保存备注的URL
        save_note_match = re.search(r"^/save_note/(\d+).html$", request_path)
        if save_note_match:
            code = save_note_match.group(1)
            logger.info(f"收到保存股票备注请求: {code}")
            
            # 获取POST数据
            import sys
            note_info = ""
            if env.get('wsgi.input'):
                try:
                    content_length = int(env.get('CONTENT_LENGTH', '0'))
                    if content_length > 0:
                        post_data = env['wsgi.input'].read(content_length).decode('utf-8')
                        # 解析POST数据
                        import urllib.parse
                        post_params = urllib.parse.parse_qs(post_data)
                        note_info = post_params.get('note_info', [''])[0]
                except Exception as e:
                    logger.error(f"解析POST数据失败: {e}")
            
            if not note_info:
                return json.dumps({"status": "error", "message": "备注信息不能为空"}, ensure_ascii=False)
            
            conn, db_available = get_db_connection()
            
            if db_available:
                cursor = conn.cursor()
                check_sql = "select id from info where code = %s"
                cursor.execute(check_sql, (code,))
                stock_id = cursor.fetchone()
                
                if stock_id:
                    # 检查是否存在备注记录
                    check_note_sql = "select id from focus where id = %s"
                    cursor.execute(check_note_sql, (stock_id[0],))
                    if cursor.fetchone():
                        # 更新备注
                        update_sql = "update focus set note_info = %s where id = %s"
                        cursor.execute(update_sql, (note_info, stock_id[0]))
                        conn.commit()
                        result = {"status": "success", "message": "备注保存成功"}
                        logger.info(f"股票 {code} 备注更新成功")
                    else:
                        result = {"status": "error", "message": "股票不在关注列表中"}
                        logger.warning(f"股票 {code} 不在关注列表中")
                    
                    cursor.close()
                    conn.close()
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
            else:
                stock = next((s for s in memory_stock_data if s[1] == code), None)
                if stock:
                    stock_id = stock[0]
                    if stock_id in memory_focus_data:
                        memory_focus_data[stock_id] = note_info
                        result = {"status": "success", "message": "备注保存成功"}
                        logger.info(f"内存数据: 股票 {code} 备注更新成功")
                    else:
                        result = {"status": "error", "message": "股票不在关注列表中"}
                        logger.warning(f"股票 {code} 不在关注列表中")
                else:
                    result = {"status": "error", "message": "股票不存在"}
                    logger.warning(f"股票 {code} 不存在")
            
            return json.dumps(result, ensure_ascii=False)
        
        # 处理普通URL
        func = FUNC_URL_LIST[request_path]
        ret = func()
        return ret
    except Exception as e:
        print(e)
        return "404 not found..."