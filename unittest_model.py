import unittest
from unittest.mock import patch, MagicMock


class TestDemo(unittest.TestCase):
    @classmethod
    def setUpClass(cls):  # 类前一次
        print("类初始化")

    @classmethod
    def tearDownClass(cls):  # 类后一次
        print("类清理")

    def setUp(self):  # 每个方法前
        print("方法前")

    def tearDown(self):  # 每个方法后
        print("方法后")

    def test_func(self):  # 必须test_开头
        self.assertEqual(1 + 1, 2)


# 常用断言
# self.assertEqual(a, b)      # a == b
# self.assertTrue(x)          # x 为真
# self.assertFalse(x)         # x 为假
# self.assertIn(a, b)        # a in b
# self.assertIsNone(x)       # x is None
# self.assertRaises(Error)   # 抛异常
# self.assertAlmostEqual(0.1+0.2, 0.3)  # 浮点数


@patch("module.func")
def test_mock(self, mock_func):
    mock_func.return_value = "mock"
    # result = module.func()
    mock_func.assert_called_once()


# 命令行
# python -m unittest test.py
# python -m unittest discover  # 发现所有测试

# 代码内
unittest.main()
