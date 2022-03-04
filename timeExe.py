from datetime import datetime, timedelta


def time_exe(source_time):
    if type(source_time) == str:
        if u'刚刚' in source_time:
            date_fm = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        elif u'分钟' in source_time:
            minute = source_time[:source_time.find(u'分钟')]
            minute = timedelta(minutes=int(minute))
            date_fm = (datetime.now() - minute).strftime('%Y-%m-%d %H:%M:%S')
        elif u'小时' in source_time:
            hour = source_time[:source_time.find(u'小时')]
            hour = timedelta(hours=int(hour))
            date_fm = (datetime.now() - hour).strftime('%Y-%m-%d %H:%M:%S')
        elif u'昨天' in source_time:
            day = timedelta(days=1)
            date_fm = (datetime.now() - day).strftime('%Y-%m-%d %H:%M:%S')
        else:
            created_at = source_time.replace('+0800 ', '')
            temp = datetime.strptime(created_at, '%c')
            date_fm = datetime.strftime(temp, '%Y-%m-%d %H:%M:%S')
    else:
        date_fm = source_time.strftime('%Y-%m-%d %H:%M:%S')
    return date_fm


def time_last_hours():
    return time_exe(datetime.now() + timedelta(hours=-1))
