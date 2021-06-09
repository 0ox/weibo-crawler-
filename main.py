import csv
import time
import random
import codecs
import logging
import requests
from lxml import etree
import pandas as pd
from selenium import webdriver
from datetime import datetime, date, timedelta

# uid list,demo id = '3952070245' 范冰冰
uid_list = ['3952070245']
end_page = 3
scheduler = BlockingScheduler()
# logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO, filename='weibo.log')
logger = logging.getLogger('weibo-spider-log')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s: - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
fh = logging.FileHandler('weibo.log')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.addHandler(fh)


def get_yesterday():
    today = date.today()
    oneday = timedelta(days=1)
    yesterday = str(today - oneday)
    return yesterday

# formate time object
def date_format(date):
    if type(date) == str:
        if u'刚刚' in date:
            date_fm = datetime.now().strftime('%Y-%m-%d')
        elif u'分钟' in date:
            minute = date[:date.find(u'分钟')]
            minute = timedelta(minutes=int(minute))
            date_fm = (datetime.now() - minute).strftime('%Y-%m-%d')
        elif u'小时' in date:
            hour = date[:date.find(u'小时')]
            hour = timedelta(hours=int(hour))
            date_fm = (datetime.now() - hour).strftime('%Y-%m-%d')
        elif u'昨天' in date:
            day = timedelta(days=1)
            date_fm = (datetime.now() - day).strftime('%Y-%m-%d')
        else:
            created_at = date.replace('+0800 ', '')
            temp = datetime.strptime(created_at, '%c')
            date_fm = datetime.strftime(temp, '%Y-%m-%d')
    else:
        date_fm = date.strftime('%Y-%m-%d')
    return date_fm


def get_weibos(uid, page):
    url = 'https://m.weibo.cn/api/container/getIndex?'
    weibos = []
    for i in range(1, page):
        params = {'containerid': '107603' + str(uid), 'page': i}
        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'
        headers = {'User-Agent': user_agent, 'Cookie': ''}
        js = requests.get(url, params=params, headers=headers).json()
        weibos.append(js['data']['cards'])
        # time sleep,not required
        time.sleep(random.uniform(3, 6))
    # print(weibos)
    return weibos


def get_one_weibo(info):
    weibo_info = info['mblog']
    return weibo_info


def get_all_data(uid_list, page):
    for i in range(0, len(uid_list)):
        uid = uid_list[i]
        weibos_list = get_weibos(uid, page)
        wb_data = {}
        write_count = 0
        screen_name = ''
        for weibos in weibos_list:
            for w in weibos:
                if w['card_type'] == 9:
                    wb = get_one_weibo(w)
                    screen_name = wb['user']['screen_name']
                    # if you want to get more information ,you cant edit this.
                    if date_format(wb['created_at']) == yesterday:
                        # User_name
                        screen_date = date_format(wb['created_at'])
                        # bid
                        bid = wb['bid']
                        wb_link = 'https://weibo.com/' + str(uid) + '/' + bid
                        # text
                        text_body = wb['text']
                        text = etree.HTML(text_body).xpath('string(.)')
                        wb_data['screen_date'] = screen_date
                        wb_data['screen_name'] = screen_name
                        wb_data['wb_link'] = wb_link
                        wb_data['text'] = text
                        write_to_csv(wb_data)
                        write_count += 1
                    else:
                        pass
        log_data = {screen_name: write_count}
        logger_handle(log_data)


def write_to_csv(data):
    # field_names = ['screen_date', 'screen_name', 'wb_link', 'text']
    with codecs.open('test.csv', 'a', 'utf_8_sig') as f:
        w = csv.DictWriter(f, data.keys())
        w.writerow(data)


def logger_handle(log_data):
    if log_data == 0:
        logger.info(u'程序启动')
    elif log_data == 1:
        logger.info('定时脚本启动')
    elif type(log_data) == dict:
        for user_name, data_sum in log_data.items():
            logger.info(u'已爬取用户:"{}" {} 条数据'.format(user_name, data_sum))


def get_screenshot():
    data = pd.read_csv('test1.csv', header=0)
    path = 'screenshot/'
    for i in range(0, len(data))[::-1]:
        date_data = str(data.iloc[i, 0])
        if date_data == yesterday:
            link = data.iloc[i, 1]
            driver = webdriver.Chrome()
            driver.maximize_window()
            driver.get(link)
            time.sleep(5)
            driver.save_screenshot(path + yesterday + '/' + str(i) + '.png')
            driver.quit()
        else:
            break


def main():
    # logger_handle(1)
    logger_handle(0)
    get_all_data(uid_list, end_page)


if __name__ == '__main__':
    yesterday = get_yesterday()
    main()
