# This file is part of GongXueYun.
#
# GongXueYun is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# GongXueYun is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GongXueYun.  If not, see <https://www.gnu.org/licenses/>.
import time
from utils import AES,UTC as pytz
import random
import requests
import hashlib
import json
from datetime import timedelta, datetime
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding
from random import randint
import logging
import mysql.connector

logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
# 获取任务加密
def md5_encrypt(data):
    """
    :param data:
    :return: md5
    """
    return hashlib.md5(data.encode("utf-8")).hexdigest()

# 将用户令牌和user_id保存到 user_info.json

def save_user_info(phone, token, user_id):
    # 连接数据库
    connection, cursor = get_db_connection()
    try:
        # 检查 token 列是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'token'")
        if cursor.fetchone() is None:
            # 如果 token 列不存在，则添加 token 列
            cursor.execute("ALTER TABLE users ADD COLUMN token VARCHAR(400)")
        # 检查 user_id 列是否存在
        cursor.execute("SHOW COLUMNS FROM users LIKE 'user_id'")
        if cursor.fetchone() is None:
            # 如果 user_id 列不存在，则添加 user_id 列
            cursor.execute("ALTER TABLE users ADD COLUMN user_id VARCHAR(255)")
        # 更新已存在用户的 token 和 user_id
        cursor.execute("UPDATE users SET token = %s, user_id = %s WHERE phone = %s", (token, user_id, phone))
        # 提交事务
        connection.commit()
    except Exception as e:
        print(f"保存用户信息时出错： {e}")
    finally:
        # 关闭数据库连接
        cursor.close()
        connection.close()

# 更新日报提交状态
def daily_report_status(phone, status):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET daily_report_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error("更新用户的日报提交状态时出错： " + phone, exc_info=True)
    finally:
        cursor.close()
        connection.close()

# 更新周报提交状态
def weekly_report_status(phone, status):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET weekly_report_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error("更新用户的周报提交状态时出错： " + phone, exc_info=True)
    finally:
        cursor.close()
        connection.close()

# 更新打卡状态
def update_punch_status(phone, status):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET punch_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error("更新用户的打卡状态时出错： " + phone, exc_info=True)
    finally:
        cursor.close()
        connection.close()

# 更新打卡天数
def update_days(phone):
    connection, cursor = get_db_connection()
    try:
        # 先查询当前用户的 days 值
        cursor.execute("SELECT days FROM users WHERE phone = %s", (phone,))
        result = cursor.fetchone()
        if result is not None:
            days_str = result['days']
            try:
                # 尝试将 days 转换为整数
                days = int(days_str)
                if days > 0:
                    # 如果 days 是正整数，则执行更新操作
                    sql = "UPDATE users SET days = days - 1 WHERE phone = %s"
                    cursor.execute(sql, (phone,))
                    connection.commit()
                else:
                    logging.warning(f"用户: {phone} days 值非正整数：{days}")
            except ValueError:
                if days_str == '打卡天数已到期':
                    logging.info(f"用户: {phone} 打卡天数已到期，跳过更新")
                else:
                    logging.warning(f"用户: {phone} days 值异常：{days_str}")
        else:
            logging.warning(f"未找到用户: {phone}")
    except Exception as e:
        logging.error("Error updating days for user: " + phone, exc_info=True)
    finally:
        cursor.close()
        connection.close()

#读取日报文件
def get_random_diary_content():
    with open(r'./basic_info/day_diary', 'r',encoding="utf-8") as f:
        diary_entries = json.load(f)
        entry = random.choice(diary_entries)['content']
    return entry

#读取周报文件
def get_random_week():
    with open(r'./basic_info/week_diary', 'r',encoding="utf-8") as f:
        diary_entries = json.load(f)
        entry = random.choice(diary_entries)['content']
    return entry

# 连接数据库
def get_db_connection():
    # 数据库配置
    db_config = {
        'host': "47.109.88.41",#服务器ip/127.0.0.1
        'user': "gongxueyun",#用户名
        'password': "r4pBbCae55GSNjMS",#数据库密码
        'database': "gongxueyun",#数据库名称
        'port': 3306  # 更正键名/数据库端口默认3306
    }
    # 连接数据库并返回连接对象
    connection = mysql.connector.connect(**db_config)
    return connection, connection.cursor(dictionary=True)

# 随机user-agent
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

def login(user):
    data = {
        "password": encrypt("23DbtQHR2UMbH6mJ", (user["password"])),
        "phone": encrypt("23DbtQHR2UMbH6mJ", (user["phone"])),
        "t": encrypt("23DbtQHR2UMbH6mJ", str(int(time.time() * 1000))),
        "loginType": "android", 
        "uuid": ""
    }
    headers = {
        "content-type": "application/json; charset=UTF-8",
        "user-agent": getUserAgent()
    }
    logging.info("登录获取" + user["phone"] + "token")
    rsp = requests.post(url='https://api.moguding.net:9000/session/user/v3/login', headers=headers, data=json.dumps(data)).json()
    if rsp.get("data"):
        data = rsp["data"]
        token = data["token"]
        user_id = data["userId"]
        save_user_info(user["phone"], token, user_id)
        logging.info("已保存用户" + user["phone"] + "token和user_id")
        return token, user_id
    else:
        print(rsp)
        logging.info("登录用户" + user["phone"] + "账号或密码错误")
        return None, None

def get_plan(token, user_id, user):
    max_retries = 3
    sleep_time = 5  # 设置重试间隔时间
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
    }  # 根据您的需求初始化 headers
    for _ in range(max_retries):
        try:
            plan_sign = user_id + "student" + "3478cbbc33f84bd00d75d7dfa69e0daa"
            headers.update({"authorization": token, "rolekey": "student", 'sign': md5_encrypt(plan_sign)})
            data1 = {'state': ''}
            
            rsp = requests.post(url="https://api.moguding.net:9000/practice/plan/v3/getPlanByStu", headers=headers, data=json.dumps(data1))
            
            # 检查响应状态码和内容
            if rsp.status_code == 200 and rsp.text:
                try:
                    json_data = rsp.json()
                except json.JSONDecodeError:
                    logging.error("用户" + user['phone']+ "无法解码 JSON")
                    time.sleep(sleep_time)
                    continue
            else:
                logging.error("用户{}无法解码 JSON，状态代码: {}, 内容: {}".format(user['phone'], rsp.status_code, rsp.text))
                time.sleep(sleep_time)
                continue
            if json_data.get("code") == 401 and json_data.get("msg") == "token失效":
                logging.info("用户" + user['phone'] + "token失效")
                token, user_id = login(user)  # 登录并返回 token 和 user_id
                logging.info("用户" + user['phone'] + "成功获取token")
                if token is None and user_id is None:
                    logging.info("登录用户" + user["phone"] + "账号或密码错误1")
                    time.sleep(sleep_time)
                    continue  # 进行下一次循环尝试
            elif json_data.get("data"):
                data = json_data["data"][0]
                plan_id = data["planId"]
                logging.info("自动获取" + user["phone"] + "plan_id")
                return plan_id, token
            else:
                logging.info(user["phone"] + 'API响应中缺少"data"键,正在重新获取任务id')
                time.sleep(sleep_time)
                continue
                
        except Exception as e:
            logging.error(f"处理用户时出错{user['phone']}: {e}")
            time.sleep(sleep_time)
    
    logging.info(user["phone"] + "经过多次尝试，未能成功获取plan_id")
    return None, None

#生成补交日报的随机时分秒
def random_time():
    hour = randint(7, 22)
    minute = randint(0, 59)
    second = randint(0, 59)
    return f"{hour:02}:{minute:02}:{second:02}"

def submit_report(user, plan_id, user_id, token, bujiao_start_date=None, bujiao_end_date=None):
    """
    提交或补交日报。
    :param bujiao_start_date: 开始日期，如果为空，则为今天提交日报。
    :param bujiao_end_date: 结束日期，如果为空，则只提交bujiao_start_date当天的日报。
    """
    if not bujiao_start_date:  # 如果没有指定开始日期，则为今天提交日报
        bujiao_start_date = datetime.now().strftime('%Y-%m-%d')
    if not bujiao_end_date:
        bujiao_end_date = bujiao_start_date
    start = datetime.strptime(bujiao_start_date, '%Y-%m-%d')
    end = datetime.strptime(bujiao_end_date, '%Y-%m-%d')
    while start <= end:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        report_time = start.strftime(f'%Y-%m-%d {random_time()}')
        content = get_random_diary_content() + f"\n\n{report_time}"
        data = {
            "yearmonth": "",
            "address": "",
            "t": aes_encrypt(int(str(time_shift(current_time)) + "000") - 3600).upper(),
            'reportTime': report_time,
            "title": "日报",
            "longitude": "0.0",
            "latitude": "0.0",
            "planId": plan_id,
            "reportType": "day",
            "content": content
        }
        time.sleep(30)
        day_sign = user_id + "day" + plan_id + "日报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
        headers.update({
            'sign': md5_encrypt(day_sign),
            "authorization": token
        })
        rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, data=json.dumps(data))
        rsp_json = rsp.json()
        if rsp_json.get("code") == 200:
            logging.info('用户：%s 日报已提交，日期%s', user['phone'], start.strftime('%Y-%m-%d'))
            daily_report_status(user['phone'],"日报提交成功")
        elif rsp_json.get("code") == 500:
            logging.info('用户：%s 今天已经写过日报，日期%s', user['phone'], start.strftime('%Y-%m-%d'))
            daily_report_status(user['phone'], rsp.text)
            start += timedelta(days=1)
            continue
        else:
            logging.info('%s 响应数据不是期望的格式: %s', user['phone'], rsp.text)
        start += timedelta(days=1)

#获取周次
def get_weeks(plan_id,token):
    """
    :return: 当前周和前19周的时间段
    """
    headers.update({
            "authorization":token
        })
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v3/getWeeks1", headers=headers,
                        data=json.dumps({"planId": plan_id})).json()
    logging.info(rsp)
    return rsp['data'][:20]
# 获取提交周报次数
def get_week_count(plan_id, user_id,token):
    """
    :return: 提交周报次数
    """
    sign = md5_encrypt(user_id + 'studentweek' + "3478cbbc33f84bd00d75d7dfa69e0daa")
    headers.update({"sign": sign,
                    "authorization":token})
    data = {"reportType": "week", "currPage": "1", "pageSize": "10", "planId": plan_id}
    rsp = requests.post(url='https://api.moguding.net:9000/practice/paper/v2/listByStu', headers=headers,
                        data=json.dumps(data)).json()
    return int(rsp['flag'])

# 判断执行提交周报还是补交周报
def submit_week(plan_id, user_id, user, token):
    # 获取当前时间和日期
    hourNow = datetime.now(pytz.timezone('PRC')).hour
    current_datetime = datetime.now()
    current_weekday = current_datetime.strftime('%A')
    if user['zhobao']:
        # 提交周报逻辑
        if current_weekday == "Sunday" and 9 <= hourNow < 12:
            logging.info('用户：' + user['phone'] + "开始写周报")
            weeks = get_weeks(plan_id, token)
            week_start = weeks[0]["startTime"]
            week_end = weeks[0]["endTime"]
            nowweek = get_week_count(plan_id, user_id, token) + 1
            handle_weekly_report(plan_id, user_id, user, token, week_start, week_end, nowweek)
    # 补交周报逻辑
    if user.get('reedy', False):
        logging.info('用户：' + user['phone'] + "开始补交周报")
        time.sleep(180)
        weeks = get_weeks(plan_id, token)
        not_submit_week = weeks[:int(user['requirement_week_num']) + 1]
        not_submit_week.reverse()
        for i in not_submit_week:
            week_start = i['startTime']
            week_end = i["endTime"]
            nowweek = get_week_count(plan_id, user_id, token) + 1
            time.sleep(30)
            handle_weekly_report(plan_id, user_id, user, token, week_start, week_end, nowweek)

def handle_weekly_report(plan_id, user_id, user, token, week_start, week_end, nowweek):
    # 公共提交逻辑
    content_entry = get_random_week()
    now = datetime.now()
    day_end = now.strftime('%Y-%m-%d %H:%M:%S')
    data = {
        "yearmonth": "",
        "address": "",
        "t": aes_encrypt(int(str(time_shift(day_end)) + "000") - 3600),
        "title": "周报",
        "longitude": "0.0",
        "latitude": "0.0",
        "weeks": f'第{str(nowweek)}周',
        "endTime": week_end,
        "startTime": week_start,
        "planId": plan_id,
        "reportType": "week",
        "content": content_entry
    }
    week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({
        'sign': md5_encrypt(week_sign),
        "authorization": token
    })
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, data=json.dumps(data))
    logging.info(user['phone'] + "提交周报返回值", rsp.text)
    if rsp.json()["code"] == 200 and rsp.json()["msg"]:
        weekly_report_status(user['phone'], "周报提交成功")
        logging.info('用户：' + user['phone'] + "周报提交成功")
    else:
        logging.info('用户：' + user['phone'] + "周报提交失败")
        weekly_report_status(user['phone'], rsp.text)
    
    # 仅在补交周报时执行数据库更新
    if user.get('reedy', False):
        connection, cursor = get_db_connection()
        try:
            cursor.execute("""
                UPDATE users
                SET reedy = NULL, requirement_week_num = NULL
                WHERE phone = %s
            """, (user['phone'],))
            connection.commit()
        except Exception as e:
            print(f"删除用户字段时出错： {e}")
        finally:
            cursor.close()
            connection.close()

def get_sign_type():
    """
    根据当前时间确定打卡类型。
    """
    hourNow = datetime.now(pytz.timezone('PRC')).hour
    if hourNow < 12:
        return 'START'
    return 'END'

def get_punch_sign(user, user_id, plan_id, signType):
    """
    获取打卡签名。
    """
    return md5_encrypt("Android" + signType + plan_id + user_id + user['address'] + "3478cbbc33f84bd00d75d7dfa69e0daa")

def punch_card(user, user_id, plan_id, token):
    """
    执行打卡操作。
    """
    signType = get_sign_type()
    headers2 = {
        'roleKey': 'student',
        "user-agent": getUserAgent(),
        "sign": get_punch_sign(user, user_id, plan_id, signType),
        "authorization": token,
        "content-type": "application/json; charset=UTF-8"
    }
    data2 = {
        "device": "Android",
        "address": user['address'],
        "description": user.get("desc","打卡"),
        "country": "中国",
        "longitude": user['longitude'],
        "city": user['city'],
        "latitude": user['latitude'],
        "t": aes_encrypt(int(time.time() * 1000)),
        "planId": plan_id,
        "province": user['province'],
        "type": signType
    }
    rsp = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save", headers=headers2, data=json.dumps(data2))
    if rsp.json()["code"] == 200 and rsp.json()["msg"]:
        logging.info('用户：' + user['phone']+"打卡成功")
        update_punch_status(user['phone'], '签到成功')
        if get_sign_type() == 'END':
            update_days(user['phone'])
    else:
        logging.info('用户：' + user['phone']+"打卡失败")
        update_punch_status(user['phone'], rsp.text)

def submit_report_entry(user, plan_id, user_id, token):
    """
    提交或补交日报。
    """
    # 提交日报
    if user['xuanbujiao']:
        hourNow = datetime.now(pytz.timezone('PRC')).hour
        if 9 <= hourNow < 12:
            logging.info('用户：' + user['phone'] + "开始写日报")
            submit_report(user, plan_id, user_id, token)

    # 补交日报
    if user.get('bujiao', False):  # 注意这里改为了 if 而不是 elif
        logging.info('用户：' + user['phone'] + "开始补交日报")
        time.sleep(100)
        bujiao_start_date = user['bujiao_start_date']
        bujiao_end_date = user['bujiao_end_date']
        submit_report(user, plan_id, user_id, token, bujiao_start_date, bujiao_end_date)
        clear_makeup_daily_report(user['phone'])

def clear_makeup_daily_report(phone):
    """
    清除补交日报的信息。
    """
    connection, cursor = get_db_connection()
    try:
        cursor.execute("""
            UPDATE users 
            SET bujiao = NULL, bujiao_start_date = NULL, bujiao_end_date = NULL 
            WHERE phone = %s
        """, (phone,))
        connection.commit()
    except Exception as e:
        logging.warning(f"删除用户字段时出错： {e}")
    finally:
        cursor.close()
        connection.close()

def check_user_days(user):
    """检查用户的打卡天数并更新数据库和用户信息（如有必要）"""
    days = user['days']
    if days == '打卡天数已到期' or (isinstance(days, int) and days <= 0):
        logging.info(f"用户: {user['phone']} 打卡天数已到期或天值小于等于0,跳过打卡操作")
        return False
    connection, cursor = get_db_connection()
    try:
        days_int = int(days)
        if days_int <= 0:
            logging.warning(f"天值小于或等于0,更新用户状态:{user['phone']}")
            cursor.execute("UPDATE users SET days = %s WHERE phone = %s", ("打卡天数已到期", user['phone']))
            connection.commit()
            user['days'] = '打卡天数已到期'
            return False
    except ValueError:
        logging.info(f"用户:{user['phone']} days 不是整数，不执行操作")
    finally:
        cursor.close()
        connection.close()
    return True

def transform_user_data(user):
    """转换用户数据的类型，如 Decimal 到 float, int 到 bool 等"""
    # 将 Decimal 类型转换为 float
    user['latitude'] = float(user['latitude'])
    user['longitude'] = float(user['longitude'])
    # 将整数转换为布尔值
    user['bujiao'] = bool(user['bujiao'])
    user['reedy'] = bool(user['reedy'])
    user['xuanbujiao'] = bool(user['xuanbujiao'])
    user['zhobao'] = bool(user['zhobao'])
    # 将 datetime.date 类型转换为字符串
    if user['bujiao_start_date'] is not None:
        user['bujiao_start_date'] = user['bujiao_start_date'].strftime('%Y-%m-%d')
    else:
        user['bujiao_start_date'] = ''  # 将日期字段设置为空字符串
    if user['bujiao_end_date'] is not None:
        user['bujiao_end_date'] = user['bujiao_end_date'].strftime('%Y-%m-%d')
    else:
        user['bujiao_end_date'] = ''  # 将日期字段设置为空字符串

# 处理签到和周报提交
def handle_sign_in_and_report(user, user_id, plan_id, token):
    logging.info("开始打卡")
    # 执行打卡操作
    punch_card(user, user_id, plan_id, token)
    # 提交日报
    submit_report_entry(user, plan_id, user_id, token)
    # 提交周报
    submit_week(plan_id, user_id,user,token)

# 处理登录和获取令牌
def handle_login_and_token(user):
    if not user.get("token"):
        logging.info('手动登录' + user["phone"])
        token, user_id = login(user)
        if token is None and user_id is None:
            logging.warning("登录失败，跳过用户：" + user["phone"])
            return None, None
    else:
        logging.info('自动登录对于用户 {}'.format(user["phone"]))
        user_id = user["user_id"]
        token = user["token"]
    plan_id, token = get_plan(token, user_id, user)
    if plan_id is None and token is None:
        logging.warning("获取plan_id失败，跳过用户：" + user["phone"])
        return None, None
    return user_id, token, plan_id
# 主函数
def main(users):
    # 对每个用户数据进行转换
    for user in users:
        try:
            if not check_user_days(user):
                continue
            transform_user_data(user)
            # 如果用户没有令牌，则登录并获取令牌并user_id
            user_id, token, plan_id = handle_login_and_token(user)
            if user_id is None or token is None or plan_id is None:
                continue
            # 开始提交周报和开始签到
            handle_sign_in_and_report(user, user_id, plan_id, token)
        except Exception as e:
            logging.error(f"处理用户时出错 {user['phone']}: {e}")
            continue

if __name__ == '__main__':
    connection, cursor = get_db_connection()
    # 查询所有用户信息
    query = """SELECT phone, password, address, province, city, area, latitude, longitude,
                    bujiao, bujiao_start_date, bujiao_end_date, reedy, requirement_week_num,token,user_id,days,punch_status,zhobao,xuanbujiao
            FROM users"""  # 请根据实际的表名和字段名修改此查询语句
    cursor.execute(query)
    # 获取查询结果
    users = cursor.fetchall()
    print(users)
    # 关闭数据库连接
    cursor.close()
    connection.close()
    main(users)