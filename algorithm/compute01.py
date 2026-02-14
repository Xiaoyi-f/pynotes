# f(x) = (f(x - 1) + 1) * 2
def handler(n):
    if n == 1:
        return 1
    return (handler(n - 1) + 1) * 2


# python的==会比较类型，但是不严格比较类型
days = input("请输入路飞吃桃子的天数:")
print(handler(int(days)))

# 轮次递归
"""
总结: 
    迭代次数
    关系
    有时语意对称
"""
