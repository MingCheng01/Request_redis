# ============================================================================================
#                                           分发                                              #
#                                    (该部分用于平均分发参数)                                    #
# ============================================================================================
def distribution_param(urls_len, param) -> list:
    """
    分发参数
    :param urls_len: url列表的长度
    :param param: 参数列表
    :return: 经过平均分配的参数的列表,长度与url列表长度一致
    """
    if type(param) == dict:
        param_ = [param for _ in range(urls_len)]
    else:
        param_len = len(param)
        paramlen = urls_len / param_len
        if paramlen % 1 > 0:
            paramlen = int(paramlen) + 1
        else:
            paramlen = int(paramlen)
        lens = paramlen
        param_ = []
        for i in range(urls_len):
            if lens != 0:
                lens -= 1
                param_.append(param[-param_len])
            else:
                lens = paramlen
                lens -= 1
                param_len -= 1
                param_.append(param[-param_len])
    return param_
