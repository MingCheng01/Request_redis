# ============================================================================================
#                                        模块导入部分                                          #
# ============================================================================================
# 参数相关模块
from Setting_and_param.Param import param
from Setting_and_param.Param import other_param
# 设置相关模块
from Setting_and_param.Setting import setting
# 日志相关模块
from Tools.Log import print_log
# 参数分发器相关模块
from Tools.Distribution import distribution_param
# 时间相关模块
import time
from Tools.Get_time import time_
# redis相关模块
from Sql.Redis_ import Redis_connect
# mysql相关模块
from Sql.Mysql_ import Mysql_connect
# request相关模块
from Request.Request_ import get_, post_
# web接口相关模块
# from Api.Webapi import get_api
# 队列相关模块
from collections import deque
# 多进程相关模块
# from concurrent.futures import ProcessPoolExecutor
# 多线程相关模块
from concurrent.futures import ThreadPoolExecutor
# concurrent中其他方法
from concurrent.futures import wait, ALL_COMPLETED


# 队列填充
class Start_Spider:
    # ============================================================================================
    #                                         初始化部分                                           #
    # ============================================================================================
    def __init__(self, task_name, pop_key, pop_num, return_to, method='get'):
        """
        :param task_name: 任务名称,同时也作为当前任务在redis中的暂存key
        :param pop_key: redis取出的key
        :param pop_num: 取出数量
        :param method: 请求方法
        :param return_to: 回调方法
        """
        self.task_name = task_name
        self.pop_key = pop_key
        self.pop_num = pop_num
        self.return_to = return_to
        self.method = method
        try:
            self.setting = setting[task_name]
            self.param = param[task_name]
        except:
            raise Exception(f'未找到当前任务名"{self.task_name}"的配置文件')
        # 初始化方法
        print_log(0, f'[{time_()} INFO]:{self.task_name}->任务启动中...')

        # 初始化redis
        if self.setting['Open_Redis']:
            print_log(0, f'[{time_()} INFO]:{self.task_name}->Redis初始化...')
            self.redis_cli = Redis_connect(
                host=self.param['redis_param']['host'],
                port=self.param['redis_param']['port'],
                db=self.param['redis_param']['db'],
                password=self.param['redis_param']['password'],
                max_connections=self.param['redis_param']['max_connections'],
                decode_responses=self.param['redis_param']['decode_responses']
            )
            print_log(0, f'[{time_()} INFO]:{self.task_name}->Redis初始化成功')

        # 初始化mysql
        if self.setting['Open_Mysql']:
            print_log(0, f'[{time_()} INFO]:{self.task_name}->Mysql初始化中...')
            self.mysql_cli = Mysql_connect(
                host=self.param['mysql_param']['host'],
                port=self.param['mysql_param']['port'],
                user=self.param['mysql_param']['user'],
                password=self.param['mysql_param']['password'],
                database=self.param['mysql_param']['database'],
                charset=self.param['mysql_param']['charset']
            )
            print_log(0, f'[{time_()} INFO]:{self.task_name}->Mysql初始化成功')

        # 初始化对列
        self.deque_ = deque(maxlen=self.param['queue_param']['max_len'] + 1)

        # 初始化线程池
        if self.setting['Open_Thread']:
            print_log(0, f'[{time_()} INFO]:{self.task_name}->线程池初始化...')
            self.threadpool_ = ThreadPoolExecutor(max_workers=self.param['thread_param']['max_workers'])
            print_log(0, f'[{time_()} INFO]:{self.task_name}->线程池初始化成功')
        print_log(0, f'[{time_()} INFO]:{self.task_name}初始化成功!')

    # ============================================================================================
    #                                         爬虫部分                                            #
    # ============================================================================================

    def get_url(self):
        """
        取出url
        :return: 取出的url
        """
        urls = self.redis_cli.lpop_list(self.task_name, self.pop_num)
        if not urls:
            return self.redis_cli.lpop_rpush(self.pop_key, self.task_name, self.pop_num)
        else:
            print_log(0, f'[{time_()} INFO]:{self.task_name}存在未完成的任务,将继续执行!')
            return urls

    def if_empty(self, url_list):
        """
        当url列表为空时自动挂起等待,阻塞进程,如果不为空则取出后返回url_list
        :param url_list: url列表
        :return: 返回url_list或None
        """
        if not url_list:
            print_log(1, f'[{time_()} INFO]:{self.task_name}->当前url_list为空,将暂停等待{other_param["no_link_sleep"]}s!')
            time.sleep(other_param['no_link_sleep'])
            return None
        else:
            return url_list

    def Queue_filling(self, url_list: list = None,
                      headers_list: list = None,
                      cookie_list: list = None,
                      param_list: list = None,
                      data_list: list = None,
                      json_list: list = None,
                      allow_redirects: list = None,
                      proxies_list: list = None,
                      verify_list: list = None) -> list:
        """
        填充对列,对传入的参数进行处理后交由start方法开始多线程爬虫
        :param url_list: url列表
        :param headers_list: 请求头列表
        :param cookie_list: cookie列表
        :param param_list: 参数列表
        :param data_list: 数据列表
        :param json_list: json列表
        :param allow_redirects: 重定向列表
        :param proxies_list: 代理列表
        :param verify_list: SSL验证列表
        :return: 启动方法
        """
        url_list = self.if_empty(url_list)
        if url_list is None:
            return

        url_list_len = len(url_list)
        headers_list = distribution_param(urls_len=url_list_len,
                                          param=headers_list if type(headers_list) == list or type(
                                              headers_list) == dict else [None])
        cookie_list = distribution_param(urls_len=url_list_len,
                                         param=cookie_list if type(cookie_list) == list or type(
                                             cookie_list) == dict else [None])
        param_list = distribution_param(urls_len=url_list_len,
                                        param=param_list if type(param_list) == list or type(
                                            param_list) == dict else [None])
        data_list = distribution_param(urls_len=url_list_len,
                                       param=data_list if type(data_list) == list or type(
                                           data_list) == dict else [None])
        json_list = distribution_param(urls_len=url_list_len,
                                       param=json_list if type(json_list) == list or type(
                                           json_list) == dict else [None])
        proxies_list = distribution_param(urls_len=url_list_len,
                                          param=proxies_list if type(proxies_list) == list or type(
                                              proxies_list) == dict else [None])
        allow_redirects = distribution_param(urls_len=url_list_len,
                                             param=allow_redirects if type(allow_redirects) == list or type(
                                                 allow_redirects) == dict else [None])
        verify_list = distribution_param(urls_len=url_list_len,
                                         param=verify_list if type(verify_list) == list or type(
                                             verify_list) == dict else [None])
        for i in range(url_list_len):
            request_param = {'url': url_list[i], 'headers': headers_list[i], 'cookies': cookie_list[i],
                             'params': param_list[i],
                             'data': data_list[i], 'json': json_list[i], 'allow_redirects': allow_redirects[i],
                             'timeout': self.param['spider_param']['timeout'], 'proxies': proxies_list[i],
                             'verify': verify_list[i],
                             'num': 0}
            self.deque_.append(request_param)

        return self.start()

    # 注入线程池
    def start(self):
        """
        启动线程池,开始处理任务,阻塞到当前线程池所有任务执行完毕
        :return: return到初始化时指定的return_to方法
        """
        while bool(self.deque_):
            if self.deque_.__len__() >= self.param['thread_param']['max_workers']:
                all_task = [
                    self.threadpool_.submit(lambda arg: get_(*arg) if self.method == 'get' else post_(*arg),
                                            [self.deque_.popleft(), self.return_to, self.task_name, self.deque_,
                                             self.redis_cli]) for _
                    in range(self.param['thread_param']['max_workers'])]
                wait(all_task, return_when=ALL_COMPLETED, timeout=self.param['thread_param']['timeout'])

            else:
                all_task = [
                    self.threadpool_.submit(lambda arg: get_(*arg) if self.method == 'get' else post_(*arg),
                                            [self.deque_.popleft(), self.return_to, self.task_name, self.deque_,
                                             self.redis_cli]) for _
                    in
                    range(self.deque_.__len__())]

                wait(all_task, return_when=ALL_COMPLETED, timeout=self.param['thread_param']['timeout'])

    # ============================================================================================
    #                                         保存部分                                            #
    # ============================================================================================

    def save_mysql(self, table, data):
        """
        保存到数据库
        :param table: 表名
        :param data: 数据
        :return: 运行结果
        """
        return self.mysql_cli.insert(table=table, data=data)
