# _*_ coding:utf-8 _*_
import xlrd


class ReadExcel(object):
    """读取excel用例文件所有Sheet的数据"""

    def __init__(self, file_name):
        self.wb = xlrd.open_workbook(file_name)

    def read_data(self):
        """读取文件"""
        # 获取workbook中所有的表格
        sheets = self.wb.get_sheet_names()
        list_api_data = []
        for i in range(len(sheets)):
            sheet = self.wb.get_sheet_by_name(sheets[i])

            print('\n\n第' + str(i + 1) + '个sheet: ' + sheet.title + '->>>')

            # 获取第一行的标题内容，作为每一行数据的键
            keys = sheet.row_values(0)
            # 从第二行开始，获取每一行的内容
            for r in range(1, sheet.max_row + 1):
                # 获取第r行的内容
                values = sheet.row_values(r)
                # keys，values组合转换为字典
                api_dict = dict(zip(keys, values))
                list_api_data.append(api_dict)
        return list_api_data

