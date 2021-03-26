# _*_ coding:utf-8 _*_
import json
from src.common.constant import *


def send_request(session, host, head, api):
    """从api中提取request请求参数，组装request请求并发送请求"""
    try:

        method = api[API_METHOD]
        url = host + api[API_URL]

        headers = {}
        if api[API_HEADERS]:
            header_val = api[API_HEADERS].split(":")
            if "$" in api[API_HEADERS]:
                headers[header_val[0]] = header_val[1].replace("$", head)
            else:
                headers[header_val[0]] = header_val[1]

        data_type = api[API_TYPE]
        if data_type == JSON_TYPE:
            if api[API_BODY]:
                body = eval(api[API_BODY])
            if api[API_PARAMS]:
                params = eval(api[API_PARAMS])
        else:
            body = api[API_BODY]
            params = api[API_PARAMS]

        # 发送请求
        return session.request(method=method, url=url, headers=headers, params=params, data=body, verify=False)

    except Exception as e:
        print(e)


def extract_cookies(cookie):
    """从浏览器或者request headers中拿到cookie字符串，提取为字典格式的cookies"""
    cookies = dict([i.split("=", 1) for i in cookie.split("; ")])
    return cookies
