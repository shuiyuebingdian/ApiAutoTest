from pymysql.err import OperationalError
from pymysql import connect, cursors

from src.common.constant import ENCODING
from src.config.setting import CONFIG


class DB:
    """
    MySQL基本操作
    """
    def __init__(self):
        try:
            # 连接数据库
            self.conn = connect(host=CONFIG.get("mysql", "host"),
                                user=CONFIG.get("mysql", "user"),
                                password=CONFIG.get("mysql", "password"),
                                db=CONFIG.get("mysql", "db"),
                                charset='utf8mb4',
                                cursorclass=cursors.DictCursor)
        except OperationalError as e:
            print("MySQL Error %d: %s" % (e.args[0], e.args[1]))

    def clear(self, table_name):
        """清除表数据"""
        sql = "delete from " + table_name + ";"
        with self.conn.cursor() as cursor:
            # 取消表的外键约束
            cursor.execute("SET FOREIGN_KEY_CHECKS=0;")
            cursor.execute(sql)
        self.conn.commit()

    def insert(self, table_name, table_data):
        """插入表数据"""
        for key in table_data:
            table_data[key] = "'" + str(table_data[key]) + "'"
        key = ",".join(table_data.keys())
        value = ",".join(table_data.values())
        sql = "INSERT INTO " + table_name + " (" + key + ") VALUES (" + value + ");"
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
        self.conn.commit()

    def close(self):
        """关闭数据库"""
        self.conn.close()

    def init_data(self, datas):
        for table, data in datas.items():
            self.clear(table)
            for d in data:
                self.insert(table, d)
        self.close()