import random

# 使用随机模块
nums = [1, 3, 5, 7, 9]
demo = random.Random()
demo_int = demo.randrange(1, 40)
demo_float = demo.uniform(1.0, 40.0)
demo_choice = demo.choice(nums)
demo_sample = demo.sample(nums, 3)
demo.shuffle(nums)  # 原地操作，返回None
