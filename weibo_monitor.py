import requests
from datetime import datetime, timedelta
from timeExe import time_exe, time_last_hours


def get_weibo(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?'
    weibos = []
    params = {'containerid': '107603' + str(uid), 'page': 1}
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
    headers = {'User-Agent': user_agent, 'Cookie': ''}
    data_json = requests.get(url, params=params, headers=headers).json()
    data_json = data_json['data']['cards']
    # 筛选最新5条
    for i in range(0, 5):
        weibos = data_json[i]
        if weibos:
            yield weibos


def update_msg(key, created_at, content):
    title = '【重要通知】 XXX 微博有更新，请点击详情查看'
    content = '发布时间：\n\n> {} \n\n发布内容：\n\n> {}'.format(created_at, content)
    api = "https://sc.ftqq.com/{}.send".format(key)
    data = {
        "text": title,
        "desp": content
    }
    req = requests.post(api, data=data)
    if req.status_code == 200:
        print('ok')

        
def push_sum_notification(msg):
    pass

def error_msg():
    pass


def is_updated():
    recent_weibo = get_weibo(wb_id)
    last_weibo = next(recent_weibo)
    last_update_time = time_exe(last_weibo['mblog']['created_at'])
    last_hours = time_last_hours()
    if last_update_time >= last_hours:
        content = last_weibo['mblog']['text']
        update_msg(KEY, last_update_time, content)
    else:
        print('False')


if __name__ == '__main__':
    # insert your key
    KEY = ''
    # insert wb_id you want to monitor
    wb_id = ''
    is_updated()
