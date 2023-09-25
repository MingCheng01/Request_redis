# ============================================================================================
#                                           redis                                            #
#                                 (该部分用于redis相关模块定义)                                  #
# ============================================================================================
import redis


class Redis_connect:

    def __init__(self,
                 host: str = 'localhost',
                 port: int = 6379,
                 db: str = 0,
                 password: str = '',
                 max_connections: int = 10,
                 decode_responses: bool = True
                 ):
        """
        :param host: 主机
        :param port: 端口
        :param db: 数据库
        :param password: 密码
        :param max_connections: 最大连接数
        :param decode_responses: 解码响应
        """
        self.pool = redis.ConnectionPool(host=host, port=port, db=db,
                                         password=password, max_connections=max_connections,
                                         decode_responses=decode_responses)
        self.redis_pool = redis.Redis(connection_pool=self.pool)
        self.pipline = self.redis_pool.pipeline()

    def rpush_list(self, key, data) -> str:
        """
        右侧插入
        :param key: 键名
        :param data: 列表或集合或字符串
        :return: 'ok'
        """
        if type(data) == str:
            self.pipline.rpush(key, data)
        else:
            [self.pipline.rpush(key, d) for d in data]
        self.pipline.execute()
        return 'ok'

    def lpop_list(self, key, num) -> list:
        """
        左侧取出
        :param key: 键名
        :param num: 取出数量
        :return: data列表
        """
        self.pipline.lrange(key, 0, num - 1)
        self.pipline.ltrim(key, num, -1)
        data = self.pipline.execute()[0]
        return data

    def lpop_rpush(self, key1, key2, num) -> list:
        """
        右侧插入左侧取出
        :param key1: 原key
        :param key2: 需要迁移到的key
        :param num: 迁移数量
        :return: 迁移的data列表
        """
        self.pipline.lrange(key1, 0, num - 1)
        self.pipline.ltrim(key1, num, -1)
        data = self.pipline.execute()[0]
        [self.pipline.rpush(key2, d) for d in data]
        self.pipline.execute()
        return data

    def lrem(self, key, value) -> str:
        """
        :param key: 键名
        :param value: 值
        :return: 'ok'
        """
        self.pipline.lrem(key, 1, value)
        self.pipline.execute()
        return 'ok'
