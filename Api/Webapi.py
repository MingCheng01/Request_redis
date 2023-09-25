import urllib.request
from Setting_and_param.Param import web_api
from socket import *


def get_api(web_recv):
    server = socket()
    server.bind((web_api['ip'], web_api['port']))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        data_from_client = conn.recv(1024)
        data_from_client = data_from_client.decode('utf8')
        conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
        current_path = data_from_client.split(' ')[1]
        print(current_path)
        if urllib.request.unquote(current_path) == '/' + web_api['task_name']:
            text=str(web_recv.get())
            conn.send(text.encode('gbk'))
            conn.close()
        else:
            conn.send('{msg:"error!没有当前命名的任务"}'.encode('gbk'))
            conn.close()
