import itertools

# ============ itertools 必会3个（80%场景） ============

# ------------ 1. chain: 拼合多个列表（不用+号） ------------
list1 = [1, 2, 3]
list2 = [4, 5, 6]
list3 = [7, 8, 9]

# ❌ 慢：生成新列表
merged = list1 + list2 + list3  # [1,2,3,4,5,6,7,8,9]

# ✅ 快：迭代器，省内存
merged = list(itertools.chain(list1, list2, list3))  # [1,2,3,4,5,6,7,8,9]


# 实战：合并多个API返回的列表
# def get_all_users():
#     page1 = api.get_users(page=1)  # [{'id':1}, {'id':2}]
#     page2 = api.get_users(page=2)  # [{'id':3}, {'id':4}]
#     page3 = api.get_users(page=3)  # [{'id':5}, {'id':6}]
#     return list(itertools.chain(page1, page2, page3))


# ------------ 2. groupby: 分组（必须先排序！） ------------
from datetime import datetime

# 数据：订单列表
orders = [
    {"date": "2024-01-01", "amount": 100},
    {"date": "2024-01-01", "amount": 200},
    {"date": "2024-01-02", "amount": 150},
    {"date": "2024-01-02", "amount": 300},
    {"date": "2024-01-03", "amount": 50},
]

# ❌ 错：groupby不排序直接分组，结果不对
for date, group in itertools.groupby(orders, key=lambda x: x["date"]):
    print(date, list(group))  # 相邻相同才合并，不排序会分成多组

# ✅ 对：先排序，再分组
sorted_orders = sorted(orders, key=lambda x: x["date"])
for date, group in itertools.groupby(sorted_orders, key=lambda x: x["date"]):
    total = sum(item["amount"] for item in group)
    print(f"{date}: 总额 {total}")


# 实战：日志按天分组
def group_logs_by_day(logs):
    logs.sort(key=lambda x: x["timestamp"][:10])  # 按日期字符串排序
    for day, group in itertools.groupby(logs, key=lambda x: x["timestamp"][:10]):
        yield day, list(group)


# ------------ 3. product: 嵌套循环平替 ------------
colors = ["红", "蓝", "绿"]
sizes = ["S", "M", "L"]

# ❌ 丑：三层缩进
result1 = []
for color in colors:
    for size in sizes:
        result1.append(f"{color}{size}")

# ✅ 美：一层缩进
result2 = []
for color, size in itertools.product(colors, sizes):
    result2.append(f"{color}{size}")

# 更简洁：列表推导式
result3 = [f"{c}{s}" for c, s in itertools.product(colors, sizes)]
# ['红S', '红M', '红L', '蓝S', '蓝M', '蓝L', '绿S', '绿M', '绿L']


# 实战：生成测试用例
def generate_test_cases():
    browsers = ["chrome", "firefox", "safari"]
    devices = ["desktop", "mobile", "tablet"]
    languages = ["en", "zh", "ja"]

    for browser, device, lang in itertools.product(browsers, devices, languages):
        yield {
            "browser": browser,
            "device": device,
            "lang": lang,
            "url": f"/test?b={browser}&d={device}&l={lang}",
        }


# ============ 补充：偶尔用到的2个 ============

# ------------ 4. combinations: 组合（顺序无关） ------------
# 选2个，不考虑顺序
list(itertools.combinations(["A", "B", "C"], 2))  # [('A','B'), ('A','C'), ('B','C')]


# 实战：推荐系统（同时购买）
def get_frequently_bought_together(orders):
    """统计经常一起购买的商品对"""
    pairs = []
    for order in orders:
        items = order["items"]
        if len(items) >= 2:
            pairs.extend(itertools.combinations(items, 2))
    return pairs


# ------------ 5. islice: 切片迭代器（省内存） ------------
# 大文件取中间几行，不用readlines()
def read_lines(filename, start, end):
    with open(filename) as f:
        return list(itertools.islice(f, start, end))


# 等价于 f.readlines()[start:end]，但不一次性加载整个文件


# ============ 完整实战：日志分析 ============
def analyze_logs(log_file):
    """用groupby统计每天错误数"""
    errors = []

    # 读取错误日志
    with open(log_file) as f:
        for line in f:
            if "ERROR" in line:
                # 假设格式: 2024-01-01 10:23:45 ERROR: xxx
                date = line[:10]
                errors.append({"date": date, "line": line})

    # 按日期分组统计
    errors.sort(key=lambda x: x["date"])  # ⚠️ 必须排序！
    result = {}
    for date, group in itertools.groupby(errors, key=lambda x: x["date"]):
        result[date] = len(list(group))

    return result


if __name__ == "__main__":
    # 1. chain 测试
    print("chain:", list(itertools.chain([1, 2], [3, 4], [5, 6])))

    # 2. groupby 测试
    data = [("A", 1), ("A", 2), ("B", 3), ("B", 4)]
    data.sort(key=lambda x: x[0])
    for k, g in itertools.groupby(data, key=lambda x: x[0]):
        print(f"{k}: {list(g)}")

    # 3. product 测试
    print(
        "product:", [f"{c}{s}" for c, s in itertools.product(["红", "蓝"], ["S", "M"])]
    )
