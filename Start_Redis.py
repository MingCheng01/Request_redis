import time
from lxml import etree
import Engine.Main_Engine as ME
cookies = {
    'bid': 'amLulp0TT-k',
    'douban-fav-remind': '1',
    '_pk_id.100001.8cb4': 'b0e957dd3b1f618f.1694226023.',
    'll': '"118221"',
    '__utmz': '30149280.1695535174.7.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
    'ap_v': '0,6.0',
    '__utma': '30149280.1410852063.1694226023.1695535174.1695605588.8',
    '__utmc': '30149280',
    '_pk_ref.100001.8cb4': '%5B%22%22%2C%22%22%2C1695605841%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D',
    '_pk_ses.100001.8cb4': '1',
    '__utmt': '1',
    '__utmb': '30149280.1.10.1695605588',
}
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # 'Cookie': 'bid=amLulp0TT-k; douban-fav-remind=1; _pk_id.100001.8cb4=b0e957dd3b1f618f.1694226023.; ll="118221"; __utmz=30149280.1695535174.7.5.utmcsr=cn.bing.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; __utma=30149280.1410852063.1694226023.1695535174.1695605588.8; __utmc=30149280; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1695605841%2C%22https%3A%2F%2Fcn.bing.com%2F%22%5D; _pk_ses.100001.8cb4=1; __utmt=1; __utmb=30149280.1.10.1695605588',
    'Pragma': 'no-cache',
    'Referer': 'https://cn.bing.com/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'cross-site',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.188',
    'sec-ch-ua': '"Not/A)Brand";v="99", "Microsoft Edge";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
}


def request():
    _ = time.time()
    start1.redis_cli.rpush_list('test', [f'https://movie.douban.com/top250?start={i * 25}&filter=' for i in range(4)])
    while True:
        start1.Queue_filling(url_list=start1.get_url(), headers_list=[headers], cookie_list=[cookies])
        print('test1:', time.time() - _)

def parse1(data):
    html = etree.HTML(data.text)
    title = html.xpath(r'//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[1]/a/span[1]/text()')
    score = html.xpath(r'//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/div/span[2]/text()')
    msg = html.xpath(r'//*[@id="content"]/div/div[1]/ol/li/div/div[2]/div[2]/p[2]/span/text()')
    return start1.save_mysql('save_test', {'title': title, 'msg': msg, 'score': score})


if __name__ == '__main__':
    start1 = ME.Start_Spider(task_name='test1', pop_key='test', pop_num=10, return_to=parse1)
    request()
