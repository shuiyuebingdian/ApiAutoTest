import os


def new_report(report_dir):
    """查找测试报告目录中最新的文件并返回"""
    lists = os.listdir(report_dir)
    lists.sort(key=lambda fn: os.path.getmtime(report_dir + "\\" + fn))
    new_file = os.path.join(report_dir, lists[-1])
    return new_file

