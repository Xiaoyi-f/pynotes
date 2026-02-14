def handler(i, nums, len):
    if nums[i] >= (len - i):
        return 0
    return handler(i + nums[i], nums, len) + 1


if __name__ == "__main__":
    len = int(input())
    nums = input().split(" ")
    nums = list(map(lambda x: int(x.strip()), nums))  # 返回迭代器，不是直接原型操作
    print(handler(0, nums, len) + 1)
