# 递归之轮次递归
# 实现猴子偷桃问题的解决

days = int(input("请输入猴子吃桃子的天数:"))


def handler(days):
    if days == 1:
        return 1
    # days标签是轮数限制器兼递变参数
    return (handler(days - 1) + 1) * 2


if __name__ == "__main__":
    print(handler(days))


# 递归之计动递归
# 实现跳跃动作的计数

n = int(input("请输入您要输入数值的个数:"))

if n == 0:
    print(0)
else:
    str_input = input().split(maxsplit=n - 1)
    if len(str_input) != n:
        print(f"输入数量不符，期望 {n} 个")
    else:
        nums = [int(x) for x in str_input]  # 正确将每个元素转为整数
        count = 0

        def handler(pos, n, nums):
            # 终止条件：当前位置超出数组范围
            if pos >= n:
                return 0
            # 当前跳一步，然后递归跳到下一个位置
            # 下一个位置 = pos + nums[pos]
            next_pos = pos + nums[pos]
            return 1 + handler(next_pos, n, nums)
            # 回归后加1

        if __name__ == "__main__":
            result = handler(0, n, nums)  # 从位置 0 开始跳
            print(result)

# 递归之序态递归
# 实现组合

n, m = input("请输入两个序列数和限制数: ").split()
n, m = int(n), int(m)
nums = [None] * m


def handler(start: int, len: int):
    if len == m:
        for i in range(len):
            if i > 0:
                print(" ", end="")
            print(nums[i], end="")
        print()
        return

    for i in range(start, n + 1):
        nums[len] = i
        handler(i + 1, len + 1)


if __name__ == "__main__":
    handler(1, 0)
