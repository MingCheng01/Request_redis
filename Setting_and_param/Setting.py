# ============================================================================================
#                                           设置                                              #
#                                  (该部分用于设置初始化的内容)                                   #
# ============================================================================================
setting = {
    'test1': {
        # 是否初始化Redis
        'Open_Redis': True,
        # 是否初始化Mysql
        'Open_Mysql': True,
        # 是否启用多进程
        'Open_Process': False,
        # 是否启用多线程
        'Open_Thread': True
    }
}
# 日志等级
'''
info : 展示info及以上等级的信息
warn : 展示警告及以上的信息
error: 展示报错及以上的信息
'''
Log_Level = 'info'
