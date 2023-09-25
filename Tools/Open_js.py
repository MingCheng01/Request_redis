# ============================================================================================
#                                            Js                                              #
#                                  (该部分用于打开指定的Js文件)                                   #
# ============================================================================================
import execjs


def open_js(
        path_: str = '',
        encoding: str = 'utf-8',
        cwd: any = None
) -> object:
    """
    用于打开Js文件
    :param path_: 路径
    :param encoding: 编码
    :param cwd: cwd
    :return: execjs对象
    """
    with open(path_, 'r', encoding=encoding) as f:
        return execjs.compile(f.read(), cwd)
