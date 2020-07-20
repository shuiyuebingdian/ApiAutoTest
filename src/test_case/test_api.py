# _*_ coding:utf-8 _*_
import unittest

import ddt as ddt
import requests

from src.common.constant import *
from src.config import setting
from src.config.setting import CONFIG
from src.excel.read_excel import ReadExcel
from src.excel.write_excel import WriteExcel
from src.request.request import send_request, extract_cookies

test_api_data = ReadExcel(setting.SOURCE_FILE).read_data()
# --------- 读取conf.ini配置文件 ---------------
host = CONFIG.get("api", "host")


@ddt.ddt
class TestApi(unittest.TestCase):

    def setUp(self):
        self.session = requests.session()
        # 登录，将cookie加入headers
        login_api = {"URL": "/powerType/list?principal=admin", "METHOD": "get"}
        login_res = self.session.get(host + "/powerType/list?principal=admin")
        res_cookie = login_res.headers["Set-Cookie"]
        self.cookie = res_cookie[:res_cookie.index(";")]

    def tearDown(self):
        pass

    @ddt.data(*test_api_data)
    def test_api(self, data):
        # 获取ID字段数值，截取结尾数字并去掉开头0
        row_num = int(data[CASE_ID].split("_")[1])
        print("******* 正在执行用例 ->{0} *********".format(data[CASE_ID]))
        print("请求方式: {0}，请求URL: {1}".format(data[API_METHOD], data[API_URL]))
        print("请求参数: {0}".format(data[API_PARAMS]))
        print("post请求body类型为：{0} ,body内容为：{1}".format(data[API_TYPE], data[API_BODY]))

        # 发送请求
        res = send_request(self.session, host, self.cookie, data)
        self.result = res.json()
        print("页面返回信息：%s" % res.content.decode(ENCODING))
        # 获取excel表格数据的状态码和消息
        code = int(data[API_CODE])
        msg = data[API_MSG]

        if code == self.result["status"]:
            case_result = PASS
        else:
            case_result = FAIL
        print("用例测试结果:  {0}---->{1}".format(data[CASE_ID], case_result))
        WriteExcel(setting.TARGET_FILE).write_data(row_num + 1, case_result)

        self.assertEqual(self.result['status'], code, "返回实际结果是->:%s" % self.result['status'])


if __name__ == "__main__":
    unittest.main()
