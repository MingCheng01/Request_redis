# ============================================================================================
#                                           日志                                              #
#                                  (该部分用于打印日志中的内容)                                   #
# ============================================================================================
from Setting_and_param.Setting import Log_Level

# 初始化日志信息
Log_Level_dict = {'info': 0, 'warn': 1, 'error': 2}
Log_Level = Log_Level_dict[Log_Level.lower()]


def print_log(level, text) -> None:
    """
    日志打印
    :param level: 日志等级
    :param text: 文本
    :return: None
    """
    if Log_Level <= level:
        if level == 0:
            print(f'\033[1;32m {text} \033[0m\n', end='')
        elif level == 1:
            print(f'\033[1;33m {text} \033[0m\n', end='')
        elif level == 2:
            print(f'\033[1;31m {text} \033[0m\n', end='')
