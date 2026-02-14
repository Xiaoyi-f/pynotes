n = int(input())
arr = []


def handler(start, len):
    if len > 0:
        for i in range(len):
            if i >= 1:
                print(" ", end="")
            print(arr[i], end="")
        print()

    for i in range(start, n + 1):
        arr.append(i)
        handler(i + 1, len + 1)
        arr.pop()


# 最后一次是递进 -> 回归 -> 再回归

if __name__ == "__main__":
    handler(1, 0)

# 序态递归
"""
总结:
    最后一次递进虽然没有执行有效代码，
    但是也是递进，回归依旧执行，
    最后会执行以下arr.pop()这个很容易被忽略
    递归 = 递进 + 回归
    序态递归可以使用递归特性堆状态
"""
