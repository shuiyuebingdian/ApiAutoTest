# _*_ coding:utf-8 _*_
import os
import sys

from src.config import setting
from src.runner.HTMLTestRunner import HTMLTestRunner
import unittest
import time

from src.runner.create_report import new_report
from src.runner.send_mail import send_mail
from src.config.setting import CONFIG
sys.path.append(os.path.dirname(__file__))


def add_case(test_path=setting.TEST_CASE):
    """加载所有的测试用例"""
    discover = unittest.defaultTestLoader.discover(test_path, pattern='*api.py')
    return discover


def run_case(all_case, result_path=setting.TEST_REPORT):
    """执行所有的测试用例"""

    # 初始化接口测试数据

    now = time.strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(result_path, now + "_result.html")
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title=CONFIG.get("project", "report_name"),
                            description=CONFIG.get("project", "description"))
    runner.run(all_case)
    fp.close()
    report = new_report(setting.TEST_REPORT)  # 调用模块生成最新的报告
    # send_mail(report)  # 调用发送邮件模块


if __name__ == "__main__":
    cases = add_case()
    run_case(cases)
