import requests
from timeExe import time_exe, time_last_hours


def push_notification(key, data):
    api = "https://sc.ftqq.com/{}.send".format(key)
    req = requests.post(api, data=data)
    if req.json()['data']['error'] == 'SUCCESS':
        print('Push success!')
    else:
        print('Push error!!!')


def get_weibo(uid):
    url = 'https://m.weibo.cn/api/container/getIndex?'
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


def update_msg(bid, created_at, content):
    link = BASE_URL + wb_id + '/' + bid
    title = '【重要通知】 XXX 微博有更新，请点击详情查看'
    content = '发布时间：\n\n> {} \n\n发布内容：\n\n> {}\n\n连接:\n\n> {}'.format(created_at, content, link)
    # api = "https://push.showdoc.com.cn/server/api/push/{}".format(key)
    data = {
        "text": title,
        "desp": content
    }
    push_notification(KEY, data)


def error_msg():
    pass


def is_updated():
    recent_weibo = get_weibo(wb_id)
    last_weibo = next(recent_weibo)
    last_update_time = time_exe(last_weibo['mblog']['created_at'])
    last_hours = time_last_hours()
    if last_update_time >= last_hours:
        bid = last_weibo['mblog']['bid']
        content = last_weibo['mblog']['text']
        update_msg(bid, last_update_time, content)
    else:
        print('No update')


if __name__ == '__main__':
    # insert your key
    KEY = '#'
    # insert wb_id you want to monitor
    wb_id = '#'
    BASE_URL = 'https://www.weibo.com/'
    is_updated()
