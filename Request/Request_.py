# ============================================================================================
#                                           请求                                              #
#                                (该部分封装了请求方法和异常处理)                                   #
# ============================================================================================
import requests
from Tools import Log
from Tools.Memory import memory
from Tools.Get_time import time_
from Setting_and_param.Param import param
from Module.Reques_params import Request_param_revise
from Module.Request_failed import Request_failed_revise
from Module.Request_success import Request_success_criteria


def get_(params, return_to, task_name, deque_, redis_click) -> None:
    """
    封装的get方法
    :param params: 封装好的参数
    :param return_to: 回调
    :param task_name: 任务名称
    :param deque_: 任务对列
    :return: return到回调方法
    """
    try:
        params = Request_param_revise(params)
        respones = requests.get(url=params['url'], headers=params['headers'], cookies=params['cookies'],
                                params=params['params'], data=params['data'], json=params['json'],
                                allow_redirects=params['allow_redirects'],
                                proxies=params['proxies'], verify=params['verify'], timeout=params['timeout'])
        if Request_success_criteria(respones):
            Log.print_log(0, f'[{time_()} INFO]:{task_name}->GET:{params["url"]}请求成功!')
        else:
            params = Request_failed_revise(params, respones)
            raise Exception('状态码:' + str(respones.status_code))
    except Exception as e:
        respones = False
        Exception_handling(params, '请求失败', e, deque_, task_name)
    if respones:
        outcome, e = return_to(respones)
        if outcome:
            Log.print_log(0, f'[{time_()} INFO]:{task_name}->{params["url"]}保存成功!')
            redis_click.lrem(task_name, params["url"])
        else:
            Exception_handling(params, '保存失败', e, deque_, task_name)


def post_(params, return_to, task_name, deque_, redis_click) -> None:
    """
    封装的post方法
    :param params: 封装好的参数
    :param return_to: 回调
    :param task_name: 任务名称
    :param deque_: 任务对列
    :return: return到回调方法
    """
    try:
        params = Request_param_revise(params)
        respones = requests.post(url=params['url'], headers=params['headers'], cookies=params['cookies'],
                                 params=params['params'], data=params['data'], json=params['json'],
                                 allow_redirects=params['allow_redirects'],
                                 proxies=params['proxies'], verify=params['verify'], timeout=params['timeout'])
        if Request_success_criteria(respones):
            Log.print_log(0, f'[{time_()} INFO]:{task_name}->POST:{params["url"]}请求成功!')
        else:
            params = Request_failed_revise(params, respones)
            raise Exception('状态码:' + str(respones.status_code))
    except Exception as e:
        respones = False
        Exception_handling(params, '请求失败', e, deque_, task_name)
    if respones:
        outcome, e = return_to(respones)
        if outcome:
            Log.print_log(0, f'[{time_()} INFO]:{task_name}->{params["url"]}保存成功!')
            redis_click.lrem(task_name, params["url"])
        else:
            Exception_handling(params, '保存失败', e, deque_, task_name)


def Exception_handling(params, error_type, e, deque_, task_name) -> None:
    """
    封装的异常处理方法,用于处理请求失败引发的异常
    :param params: 参数
    :param error_type: 错误类型
    :param e: 错误详情
    :param deque_: 对列
    :param task_name:任务名称
    :return: 当为超过指定最大重试次数时,返回到对列,超出则写入日志
    """
    if params['num'] < param[task_name]['spider_param']['max_retry']:
        params['num'] += 1
        Log.print_log(1,
                      f'[{time_()} INFO]:{params["url"]}{error_type}'
                      f'({params["num"]}/{param[task_name]["spider_param"]["max_retry"]})!{e},返回Param.')
        return deque_.append(params)
    else:
        params['num'] += 1
        Log.print_log(2, f'[{time_()} INFO]:{params["url"]}{error_type}!{e},超出次数,写入错误日志.')
        params['error'] = e
        memory['Error_log'].append(params)
