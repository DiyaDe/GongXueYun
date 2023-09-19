import time
from utils import AES,UTC as pytz
import random
import requests
import hashlib
import json
from datetime import timedelta, datetime
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding
from random import randint
import MessagePush
#登录加密
def encrypt(key, text):
    aes = AES(key.encode("utf-8"))
    res = aes.encrypt(text.encode('utf-8'))
    msg = res.hex()
    return msg
def aes_encrypt(data):
    """
    :param data:
    :return: AES encrypt
    """
    key = '23DbtQHR2UMbH6mJ'
    encrypt_type = AESECBPKCS5Padding(key, "hex")
    text_encrypt = encrypt_type.encrypt(str(data))
    return text_encrypt
def time_shift(date):
    """
    :param time:
    :return: 将时间转成时间戳
    """
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp
def day_shift(date):
    """
    :param time:
    :return: 将时间转成时间戳
    """
    time_array = time.strptime(date, "%Y-%m-%d %H:%M:%S")
    time_stamp = int(time.mktime(time_array))
    return time_stamp
# 获取任务加密
def md5_encrypt(data):
    """
    :param data:
    :return: md5
    """
    return hashlib.md5(data.encode("utf-8")).hexdigest()
#随机user-agent
def getUserAgent():
    user= random.choice(
        [
            'Mozilla/5.0 (Linux; U; Android 9; zh-cn; Redmi Note 5 Build/PKQ1.180904.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/71.0.3578.141 Mobile Safari/537.36 XiaoMi/MiuiBrowser/11.10.8',
            'Mozilla/5.0 (Linux; Android 9; MI 6 Build/PKQ1.190118.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.2.3 (Baidu; P1 9)',
            'Mozilla/5.0 (Linux; Android 10; EVR-AL00 Build/HUAWEIEVR-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 baiduboxapp/11.0.5.12 (Baidu; P1 10)',
            'Mozilla/5.0 (Linux; Android 9; JKM-AL00b Build/HUAWEIJKM-AL00b; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/8951 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 9; COR-TL10 Build/HUAWEICOR-TL10; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)',
            'Mozilla/5.0 (Linux; Android 10; VCE-AL00 Build/HUAWEIVCE-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/74.0.3729.186 Mobile Safari/537.36 baiduboxapp/11.0.5.12 (Baidu; P1 10)',
            'Mozilla/5.0 (Linux; Android 10; CLT-AL00 Build/HUAWEICLT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10) NABar/1.0',
            'Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/6002 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/WIFI Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045129 Mobile Safari/537.36 MMWEBID/6735 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 10; SKW-A0 Build/SKYW2001202CN00MQ0; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 10)',
            'Mozilla/5.0 (Linux; Android 8.1.0; PBAM00 Build/OPM1.171019.026; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0) NABar/2.0',
            'Mozilla/5.0 (Linux; Android 9; HWI-AL00 Build/HUAWEIHWI-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045129 Mobile Safari/537.36 MMWEBID/6735 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/WIFI Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 10; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1170 MMWEBSDK/200201 Mobile Safari/537.36 MMWEBID/3371 MicroMessenger/7.0.12.1620(0x27000C36) Process/toolsmp NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 8.1.0; Redmi Note 5 Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0) NABar/2.0',
            'Mozilla/5.0 (Linux; Android 9; ELE-AL00 Build/HUAWEIELE-AL0001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1170 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/873 MicroMessenger/7.0.10.1580(0x27000AFE) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 10; HMA-AL00 Build/HUAWEIHMA-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2679 MicroMessenger/7.0.10.1580(0x27000A59) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 8.1.0; DUB-TL00 Build/HUAWEIDUB-TL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 8.1.0) NABar/2.0',
            'Mozilla/5.0 (Linux; Android 8.1.0; M1813 Build/O11019; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045129 Mobile Safari/537.36 MMWEBID/1221 MicroMessenger/7.0.12.1620(0x27000C37) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 10; CLT-AL00 Build/HUAWEICLT-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/045130 Mobile Safari/537.36 MMWEBID/2644 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/WIFI Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; U; Android 9; zh-cn; HWI-AL00 Build/HUAWEIHWI-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/10.1 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 9; CLT-AL01 Build/HUAWEICLT-AL01; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/76.0.3809.89 Mobile Safari/537.36 T7/11.20 SP-engine/2.16.0 baiduboxapp/11.20.0.14 (Baidu; P1 9)',
            'Mozilla/5.0 (Linux; Android 10; VOG-AL00 Build/HUAWEIVOG-AL00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/45016 Mobile Safari/537.36 MMWEBID/3894 MicroMessenger/7.0.12.1620(0x27000C36) Process/tools NetType/4G Language/zh_CN ABI/arm64',
            'Mozilla/5.0 (Linux; Android 7.0; Mi-4c Build/NRD91M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 XWEB/1169 MMWEBSDK/191201 Mobile Safari/537.36 MMWEBID/2208 MicroMessenger/7.0.10.1580(0x27010AFF) Process/tools NetType/4G Language/zh_CN ABI/arm64',
                ])
    return user
headers = {
    'Host': 'api.moguding.net:9000',
    'accept-language': 'zh-CN,zh;q=0.8',
    'user-agent': getUserAgent(),
    'authorization': "",
    'rolekey': "",
    'content-type': 'application/json; charset=UTF-8',
    'content-length': '161',
    'accept-encoding': 'gzip',
    'cache-control': 'no-cache'
}
# 获取planid
def get_plan(token,user_id,user):
    plan_sign = user_id + "student" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({"authorization": token, "rolekey": "student", 'sign': md5_encrypt(plan_sign)})
    data = {
        'state': ''
    }
    rsp = requests.post(url="https://api.moguding.net:9000/practice/plan/v3/getPlanByStu", headers=headers, data=json.dumps(data)).json()
    if rsp.get("code") == 401 and rsp.get("msg") == "token失效":
        # 如果用户有令牌，则清除 token
        if user.get("token"):
            # Token 失效，进行处理，例如
            user.pop("token")
            user.pop("user_id")
            print('手动登录获取token', user["phone"])
            data = {
                "password": encrypt("23DbtQHR2UMbH6mJ", (user["password"])),
                "phone": encrypt("23DbtQHR2UMbH6mJ",(user["phone"])),
                "t":encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))) ,
                "loginType": "android",
                "uuid": ""
            }
            headers2 = {
            "content-type": "application/json; charset=UTF-8",
            "user-agent": getUserAgent()
            }
            rsp = requests.post(url='https://api.moguding.net:9000/session/user/v3/login', headers=headers2, data=json.dumps(data)).json()
            # 假设成功响应具有关键“数据”
            if rsp.get("data"):
                data = rsp["data"]
                token = data["token"]
                user_id = data["userId"]
                save_user_info(user["phone"], token, user_id)           
    else:
        print(rsp)
        data = rsp["data"][0]
        plan_id = data["planId"]
        print("这个是 plan", plan_id)
        return plan_id

#获取周次
def get_weeks(plan_id):
    """
    获取去年该月到该月周的时间段
    :param plan_id:
    :return: 当前周和前19周的时间段
    """
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v3/getWeeks1", headers=headers,
                        data=json.dumps({"planId": plan_id})).json()
    print(rsp)
    return rsp['data'][:20]
# 获取提交周报次数
def get_week_count(plan_id, user_id):
    """
    :param plan_id:
    :return: 提交周报次数
    """
    sign = md5_encrypt(user_id + 'studentweek' + "3478cbbc33f84bd00d75d7dfa69e0daa")
    headers.update({"sign": sign})
    data = {"reportType": "week", "currPage": "1", "pageSize": "10", "planId": plan_id}
    rsp = requests.post(url='https://api.moguding.net:9000/practice/paper/v2/listByStu', headers=headers,
                        data=json.dumps(data)).json()
    return int(rsp['flag'])

#读取日报文件
def get_random_diary_content():
    with open(r'./basic_info/day_diary', 'r',encoding="utf-8") as f:
        diary_entries = json.load(f)
        entry = random.choice(diary_entries)['content']
    return entry

#生成补交日报的随机时分秒
def random_time():
    hour = randint(7, 22)
    minute = randint(0, 59)
    second = randint(0, 59)
    return f"{hour:02}:{minute:02}:{second:02}"

# 补交日报
# bujiao_end_date补交起始日期
# bujiao_end_date补交结束日期
def bujiao_day(plan_id, user_id, bujiao_start_date, bujiao_end_date):
    """
    :param plan_id:
    :param user_id:
    :param start_date: 起始日期
    :param end_date: 结束日期
    :return:
    """
    # 解析日期
    start = datetime.strptime(bujiao_start_date, '%Y-%m-%d')
    end = datetime.strptime(bujiao_end_date, '%Y-%m-%d')
    # 获取当前时间
    now = datetime.now()
    day_end = now.strftime('%Y-%m-%d %H:%M:%S')
    # 遍历日期范围并补交日报
    while start <= end:
        report_time = start.strftime(f'%Y-%m-%d {random_time()}')
        # 获取随机日记内容并与当前日期相结合以确保唯一性
        content = get_random_diary_content() + f"\n\n{report_time}"
        data = {
            "yearmonth": "",
            "address": "",
            "t": aes_encrypt(int(str(day_shift(day_end)) + "000") - 3600).upper(),
            'reportTime': report_time, # 使用当前日期作为reportTime
            "title": "日报",
            "longitude": "0.0",
            "latitude": "0.0",
            "planId": plan_id,
            "reportType": "day",
            "content": content
        }
        day_sign = user_id + "day" + plan_id + "日报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
        headers.update({'sign': md5_encrypt(day_sign)})
        print(f"开始写{report_time}的日报")
        time.sleep(random.randint(10, 30))
        rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, data=json.dumps(data))
        print(rsp.text)
        # 递增日期
        start += timedelta(days=1)

# 提交日报
def tijioa_dayk(plan_id, user_id):
    """
    :param url:
    :param plan_id:
    :param user_id:
    :return:
    """
    # 获取当前时间
    now = datetime.now()
    day_end = now.strftime('%Y-%m-%d %H:%M:%S')
    # 获取随机日记内容并与当前日期相结合以确保唯一性
    content = get_random_diary_content() + f"\n\n{day_end}"
    #请求体
    data = {
        "yearmonth": "",
        "address": "",
        "t": aes_encrypt(int(str(day_shift(day_end)) + "000") - 3600).upper(),
        "title": "日报",
        "longitude": "0.0",
        "latitude": "0.0",
        "planId": plan_id,
        "reportType": "day",
        "content": content
    }
    day_sign = user_id + "day" + plan_id + "日报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({'sign': md5_encrypt(day_sign)})
    print("开始写日报")
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v2/save", headers=headers, data=json.dumps(data))
    print(rsp.text)
#读取周报文件
def get_random_week():
    with open(r'./basic_info/week_diary', 'r',encoding="utf-8") as f:
        diary_entries = json.load(f)
        entry = random.choice(diary_entries)['content']
    return entry
# 这个代码当我执行补交周报的时候，写入周报的内容都是一样的如何解决
# 提交周报
# requirement_week_num补交的周数
# remedy是否开启补交
def submit_week(plan_id, user_id):
    """
    提交周报
    :param url:
    :param plan_id:
    :param user_id:
    :return:
    """
    weeks = get_weeks(plan_id)
    week_start = weeks[0]["startTime"]
    week_end = weeks[0]["endTime"]
    # # 已提交周报个数
    total = get_week_count(plan_id, user_id)
    # # 第几周的周报
    content_entry = get_random_week()
    nowweek = total + 1
    data = {
        "yearmonth": "",
        "address": "",
        "t": aes_encrypt(int(str(time_shift(week_end)) + "000") - 3600),
        "title": "周报",
        "longitude": "0.0",
        "latitude": "0.0",
        "weeks": f'第{str(nowweek)}周',
        "endTime": f"{str(week_end)}",
        "startTime": f"{str(week_start)}",
        "planId": plan_id,
        "reportType": "week",
        "content": content_entry
    }
    week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({'sign': md5_encrypt(week_sign)})
    print("开始写周报")
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v2/save", headers=headers, data=json.dumps(data))
    print(rsp.text)
# 将用户令牌和user_id保存到 user_info.json
def save_user_info(phone, token, user_id):
    with open('user_info.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    for user in data:
        if user["phone"] == phone:
            user["token"] = token
            user["user_id"] = user_id
            break
    else:
        user_entry = {
            "phone": phone,
            "token": token,
            "user_id": user_id
        }
        data.append(user_entry)
    with open('user_info.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)
# 主函数
def main(log_url):
    with open('user_info.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
    for user in users:
        # 如果用户没有令牌，则登录并获取令牌并user_id
        if not user.get("token"):
            print('手动登录 for user', user["phone"])
            data = {
                "password": encrypt("23DbtQHR2UMbH6mJ", (user["password"])),
                "phone": encrypt("23DbtQHR2UMbH6mJ",(user["phone"])),
                "t":encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))) ,
                "loginType": "android",
                "uuid": ""
            }
            headers2 = {
            "content-type": "application/json; charset=UTF-8",
            "user-agent": getUserAgent()
            }
            rsp = requests.post(url=log_url, headers=headers2, data=json.dumps(data)).json()
            # 假设成功响应具有关键“数据”
            if rsp.get("data"):
                data = rsp["data"]
                token = data["token"]
                user_id = data["userId"]
                save_user_info(user["phone"], token, user_id)
                plan_id  = get_plan(token, user_id,user)
                # 开始签到
                hourNow = datetime.now(pytz.timezone('PRC')).hour
                if hourNow < 12:
                    signType = 'START'
                else:
                    signType = 'END'
                # 打卡签名算法
                post_sign = "Android" + signType + plan_id + user_id + user['address'] + "3478cbbc33f84bd00d75d7dfa69e0daa"
                sings= md5_encrypt(post_sign)
                # 打卡请求头
                headers2 = {
                    'roleKey': 'student',
                    "user-agent": getUserAgent(),
                    "sign": sings,
                    "authorization": token,
                    "content-type": "application/json; charset=UTF-8"
                }
                # 打卡请求体
                data2 = {"device": "Android", "address": user['address'],
                        "description": user.get("desc","打卡"), "country": "中国", "longitude": user['longitude'], "city":user['city'],
                        "latitude": user['latitude'],
                        "t": aes_encrypt(int(time.time() * 1000)),
                        "planId": plan_id, "province": user['province'], "type": signType}
                rsp = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save", headers=headers2, data=json.dumps(data2))
                if 9 <= hourNow < 10:
                # 开始写日报
                    tijioa_dayk(plan_id,user_id)
                # 补交日报
                if user['bujiao']==True:
                    bujiao_start_date=user['bujiao_start_date']
                    bujiao_end_date=user['bujiao_end_date']
                    bujiao_day(plan_id, user_id, bujiao_start_date, bujiao_end_date)
                    del user["bujiao"]
                    del user["bujiao_start_date"]
                    del user["bujiao_end_date"]               # 补交周报
                if user['reedy']==True:
                    weeks = get_weeks(plan_id)
                    not_submit_week = weeks[:user['requirement_week_num'] + 1]
                    not_submit_week.reverse()
                    # # 第几周的周报
                    content_entry = get_random_week()
                    week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
                    for i in not_submit_week:
                        time.sleep(30)
                        after_week = get_week_count(plan_id, user_id) + 1
                        headers.update({'sign': md5_encrypt(week_sign)})
                        week_end = i["endTime"]
                        data["t"] = aes_encrypt(time_shift(week_end) - 36000 + 1000)
                        data["startTime"] = i['startTime']
                        data["endTime"] = week_end
                        data["weeks"] = f'第{str(after_week)}周'
                        data["content"] = content_entry['content']
                        rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v2/save", headers=headers, data=json.dumps(data))
                        print(rsp.text)
                    del user["reedy"]
                    del user["requirement_week_num"]                
                    # 获取当前日期和时间
                current_datetime = datetime.now()
                # 从当前日期中提取日期和星期几
                current_weekday = current_datetime.strftime('%A')
                # 开始提交周报
                if current_weekday=="Sunday":
                    submit_week(plan_id, user_id)
            else:
                print(f"用户登录失败 {user['phone']}")
                MessagePush.pushMessage(user['phone'], '工学云' ,'用户：' + user['phone']+ '登录失败' , user.get("pushKey","931dc45e83a442d39eddf0230d2c09e5"))
        else:
            print('自动登录对于用户', user["phone"])
            user_id = user["user_id"]
            token=user["token"]
            plan_id  = get_plan(token, user_id,user)           
                # 开始签到
            hourNow = datetime.now(pytz.timezone('PRC')).hour
            if hourNow < 12:
                signType = 'START'
            else:
                signType = 'END'
                # 打卡签名算法
            print(signType)
            print(plan_id)
            print(user_id)
            print(user['address'])
            post_sign = "Android" + signType + plan_id + user_id + user['address'] + "3478cbbc33f84bd00d75d7dfa69e0daa"
            sings= md5_encrypt(post_sign)
                # 打卡请求头
            headers2 = {
                    'roleKey': 'student',
                    "user-agent": getUserAgent(),
                    "sign": sings,
                    "authorization": token,
                    "content-type": "application/json; charset=UTF-8"
                }
                # 打卡请求体
            data2 = {"device": "Android", "address": user['address'],
                        "description": user.get("desc","打卡"), "country": "中国", "longitude": user['longitude'], "city":user['city'],
                        "latitude": user['latitude'],
                        "t": aes_encrypt(int(time.time() * 1000)),
                        "planId": plan_id, "province": user['province'], "type": signType}
            rsp = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save", headers=headers2, data=json.dumps(data2))
            # 8点到9点开始写日报
            if 9 <= hourNow < 10:
                tijioa_dayk(plan_id,user_id)
                # 补交日报
            if user['bujiao']==True:
                bujiao_start_date=user['bujiao_start_date']
                bujiao_end_date=user['bujiao_end_date']
                bujiao_day(plan_id, user_id, bujiao_start_date, bujiao_end_date)
                del user["bujiao"]      
                del user["bujiao_start_date"]
                del user["bujiao_end_date"]
            if user['reedy']==True:
                weeks = get_weeks(plan_id)
                not_submit_week = weeks[:user['requirement_week_num'] + 1]
                not_submit_week.reverse()
                # # 第几周的周报
                content_entry = get_random_week()
                week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
                for i in not_submit_week:
                    time.sleep(30)
                    after_week = get_week_count(plan_id, user_id) + 1
                    headers.update({'sign': md5_encrypt(week_sign)})
                    week_end = i["endTime"]
                    data["t"] = aes_encrypt(time_shift(week_end) - 36000 + 1000)
                    data["startTime"] = i['startTime']
                    data["endTime"] = week_end
                    data["weeks"] = f'第{str(after_week)}周'
                    data["content"] = content_entry['content']
                    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v2/save", headers=headers, data=json.dumps(data))
                    print(rsp.text)
                del user["reedy"]
                del user["requirement_week_num"]
            # 开始提交周报
            # 获取当前日期和时间
            current_datetime = datetime.now()
            # 从当前日期中提取日期和星期几
            current_weekday = current_datetime.strftime('%A')
            if current_weekday=="Sunday":
                submit_week(plan_id, user_id)

if __name__ == '__main__':
    log_url='https://api.moguding.net:9000/session/user/v3/login'
    main(log_url)
