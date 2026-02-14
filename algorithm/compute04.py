n, m = map(int, input().split(" "))
arr = []


def handler(start, len):
    if len == m:
        for i in range(len):
            if i > 0:
                print(" ", end="")
            print(arr[i], end="")
        print()
        return  # 阻断递进

    # 减枝
    if n - start + 1 < m - len:
        return

    for i in range(start, n + 1):
        arr.append(i)
        handler(i + 1, len + 1)
        arr.pop()


handler(1, 0)

# 序态递归
"""
总结:
    递归是利用栈实现的
    遵循先进后出原则
    利用栈帧盒子和剪枝优化
    巧妙阻断递进
"""
