# _*_ coding:utf-8 _*_
import json
from src.common.constant import *


def send_request(session, api):
    """从api中提取request请求参数，组装request请求并发送请求"""
    try:

        method = api[API_METHOD]
        url = api[API_URL]
        if api[API_PARAMS]:
            params = eval(api[API_PARAMS])
        else:
            params = None

        if api[API_HEADERS]:
            headers = eval(api[API_HEADERS])
        else:
            headers = None

        data_type = api[API_TYPE]
        if api[API_BODY]:
            body = eval(api[API_BODY])
            if data_type == JSON_TYPE:
                body = json.dumps(body)
        else:
            body = None

        # 发送请求
        return session.request(method=method, url=url, headers=headers, params=params, data=body, verify=False)

    except Exception as e:
        print(e)
