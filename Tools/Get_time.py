# ============================================================================================
#                                           时间                                              #
#                                   (该部分用于返回时间的内容)                                   #
# ============================================================================================
import time


def time_() -> str:
    """
    生成时间
    :return: %Y-%m-%d %H:%M:%S格式的时间
    """
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())