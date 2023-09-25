# ============================================================================================
#                                           mysql                                            #
#                                 (该部分用于mysql相关模块定义)                                  #
# ============================================================================================
import pymysql


class Mysql_connect:

    def __init__(
            self,
            host: str = 'localhost',
            port: int = 3306,
            user: str = 'root',
            password: str = 'root',
            database: str = '',
            charset: str = 'utf8'
    ):
        """
        :param host: 主机
        :param port: 端口
        :param user: 用户
        :param password: 密码
        :param database: 数据库
        :param charset: 编码
        """
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset
        )

    def insert(self, table, data) -> bool:
        """
        插入方法,支持多条数据同时插入,类型{key1:[list],key2:[list],...}
        :param table: 要插入的表
        :param data: 数据字典
        :return:是否插入成功
        """
        keys = ', '.join(data.keys())
        keys_list = list(data.keys())
        s_count = len(keys_list) * "%s,"
        try:
            with self.conn.cursor() as cursor:
                if type(data[list(data.keys())[0]]) == list:
                    data_len = len(data[list(data.keys())[0]])
                    values = [tuple([data[key][i] for key in keys_list]) for i in range(data_len)]
                    sql = "insert into " + table + " (" + keys + ") values (" + s_count[:-1] + ")"
                    cursor.executemany(sql, values)
                else:
                    sql = "insert into " + table + " (" + keys + ") values (" + s_count[:-1] + ")"
                    cursor.execute(sql, list(data.values()))
            self.conn.commit()
            return True, ''
        except Exception as e:
            self.conn.rollback()
            return False, e

    def close(self) -> None:
        """
        :return: None
        """
        self.conn.close()
