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
# 连接数据库
def get_db_connection():
    # 数据库配置
    db_config = {
        "host": "xxx,
        "user": "gongxueyun",
        "password": "xxxxx",
        "database": "gongxueyun",
        "port": 3306
    }
    # 连接数据库并返回连接对象
    connection = mysql.connector.connect(**db_config)
    return connection, connection.cursor(dictionary=True)
# 将用户令牌和user_id保存到 user_info.json
def save_user_info(phone: str, token: str, user_id: str):
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
def daily_report_status(phone: str, status: str):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET daily_report_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error(f"更新用户的日报提交状态时出错： {phone}", exc_info=True)

    finally:
        cursor.close()
        connection.close()

# 更新周报提交状态
def weekly_report_status(phone: str, status: str):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET weekly_report_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error(f"更新用户的周报提交状态时出错： {phone}", exc_info=True)

    finally:
        cursor.close()
        connection.close()

# 更新打卡状态
def update_punch_status(phone: str, status: str):
    # 创建数据库连接
    connection, cursor = get_db_connection()
    try:
        # 更新用户的打卡状态
        sql = "UPDATE users SET punch_status = %s WHERE phone = %s"
        cursor.execute(sql, (status, phone))
        connection.commit()
    except Exception as e:
        logging.error(f"更新用户的打卡状态时出错： {phone}", exc_info=True)
    finally:
        cursor.close()
        connection.close()

# 更新打卡天数
def update_days(phone: str):
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
        logging.error(f"用户更新天数时出错： {phone}", exc_info=True)

    finally:
        cursor.close()
        connection.close()

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

def login(user,proxy):
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
    logging.info(f"登录获取{user['phone']}token")
    time.sleep(random.randint(5, 10))
    rsp = requests.post(url='https://api.moguding.net:9000/session/user/v3/login', headers=headers,proxies=proxy, data=json.dumps(data)).json()
    if rsp.get("data"):
        data = rsp["data"]
        token = data["token"]
        user_id = data["userId"]
        save_user_info(user["phone"], token, user_id)
        logging.info(f"已保存用户{user['phone']}token和user_id")
        return token, user_id
    else:
        logging.info(f"登录用户{user['phone']}账号或密码错误")
        return None, None

def get_plan(token: str, user_id: str, user,proxy):
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
            time.sleep(random.randint(1, 5))
            rsp = requests.post(url="https://api.moguding.net:9000/practice/plan/v3/getPlanByStu", headers=headers, proxies=proxy,data=json.dumps(data1))
            # 检查响应状态码和内容
            if rsp.status_code == 200 and rsp.text:
                try:
                    json_data = rsp.json()
                except json.JSONDecodeError:
                    logging.error(f"用户{user['phone']}无法解码 JSON")
                    time.sleep(sleep_time)
                    continue
            else:
                logging.error("用户{}无法解码 JSON，状态代码: {}, 内容: {}".format(user['phone'], rsp.status_code, rsp.text))
                time.sleep(sleep_time)
                continue
            if json_data.get("code") == 401 and json_data.get("msg") == "token失效":
                logging.error(f"用户{user['phone']}token失效")
                token, user_id = login(user)  # 登录并返回 token 和 user_id
                logging.info(f"用户{user['phone']}成功获取token")
                if token is None and user_id is None:
                    logging.info(f"登录用户{user['phone']}账号或密码错误")
                    time.sleep(sleep_time)
                    continue  # 进行下一次循环尝试
            elif json_data.get("data"):
                data = json_data["data"][0]
                plan_id = data["planId"]
                logging.info(f"自动获取{user['phone']}plan_id")
                return plan_id, token
            else:
                logging.info(f"{user['phone']}API响应中缺少data键,正在重新获取任务id")
                time.sleep(sleep_time)
                continue
        except Exception as e:
            logging.error("get_plan:处理用户时出错{}: {}".format(user['phone'], repr(e)))
            time.sleep(sleep_time)
            continue

    logging.info(f"{user['phone']}经过多次尝试，未能成功获取plan_id")
    return None, None

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
def bujiao_day(plan_id: str, user_id: str, bujiao_start_date: str, bujiao_end_date: str,user,token,proxy):
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
    # 遍历日期范围并补交日报
    while start <= end:
          # 获取当前时间
        now = datetime.now()
        day_end = now.strftime('%Y-%m-%d %H:%M:%S')
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
        time.sleep(random.randint(5, 10))
        day_sign = user_id + "day" + plan_id + "日报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
        headers.update({
            'sign': md5_encrypt(day_sign),
            "authorization":token
        })
        logging.info(f"用户：{user['phone']}开始写{report_time}的日报")
        time.sleep(random.randint(10, 30))
        rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers,proxies=proxy, data=json.dumps(data))
        rsp_json = rsp.json()
        logging.info(f"{user['phone']}补交日报返回值 {rsp.text}")
        if isinstance(rsp_json, dict):
            if rsp_json.get("code") == 200:
                logging.info('用户：%s 补交日报已提交，日期%s', user['phone'], start.strftime('%Y-%m-%d'))
            elif rsp_json.get("code") == 500:
                logging.info('用户：%s 今天已经写过日报，日期%s', user['phone'], start.strftime('%Y-%m-%d'))
                start += timedelta(days=1)
                continue
        else:
            logging.info('%s 响应数据不是JSON格式: %s', user['phone'], rsp.text)
            start += timedelta(days=1)
            continue
        # 递增日期
        start += timedelta(days=1)

# 提交日报
def tijioa_dayk(user,plan_id, user_id,token,proxy):
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
        'reportTime':day_end,
        "longitude": "0.0",
        "latitude": "0.0",
        "planId": plan_id,
        "reportType": "day",
        "content": content
    }
    day_sign = user_id + "day" + plan_id + "日报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
    headers.update({
            'sign': md5_encrypt(day_sign),
            "authorization":token
        })
    time.sleep(random.randint(5, 10))
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, proxies=proxy,data=json.dumps(data))

    if rsp.json()["code"] == 200 and rsp.json()["msg"]:
        daily_report_status(user['phone'],"日报提交成功")
        logging.info(f"用户：{user['phone']}日报提交成功{rsp.text}")
    else:
        # 增加返回值
        logging.info(f"用户：{user['phone']}日报提交失败 {rsp.text}")
        # 当提交日报失败时，调用这个函数并将状态设为API的返回值或错误信息
        daily_report_status(user['phone'], rsp.text)

#读取周报文件
def get_random_week():
    with open(r'./basic_info/week_diary', 'r',encoding="utf-8") as f:
        diary_entries = json.load(f)
        entry = random.choice(diary_entries)['content']
    return entry

#获取周次
def get_weeks(plan_id,token,proxy):
    """
    获取去年该月到该月周的时间段
    :param plan_id:
    :return: 当前周和前19周的时间段
    """
    headers.update({
            "authorization":token
        })
    time.sleep(random.randint(5, 10))
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v3/getWeeks1", headers=headers,proxies=proxy,
                        data=json.dumps({"planId": plan_id})).json()
    logging.info(rsp)
    return rsp['data'][:20]
# 获取提交周报次数
def get_week_count(plan_id: str, user_id: str,token,proxy):
    """
    :param plan_id:
    :return: 提交周报次数
    """
    sign = md5_encrypt(user_id + 'studentweek' + "3478cbbc33f84bd00d75d7dfa69e0daa")
    headers.update({"sign": sign,
                    "authorization":token})
    data = {"reportType": "week", "currPage": "1", "pageSize": "10", "planId": plan_id}
    time.sleep(random.randint(5, 10))
    rsp = requests.post(url='https://api.moguding.net:9000/practice/paper/v2/listByStu', headers=headers,proxies=proxy,
                        data=json.dumps(data)).json()
    return int(rsp['flag'])

# 提交周报
def submit_week(plan_id, user_id,user,token,proxy):
    """
    提交周报
    :param url:
    :param plan_id:
    :param user_id:
    :return:
    """
    weeks = get_weeks(plan_id,token,proxy)
    week_start = weeks[0]["startTime"]
    week_end = weeks[0]["endTime"]
    # 获取当前时间
    now = datetime.now()
    day_end = now.strftime('%Y-%m-%d %H:%M:%S')
    # # 已提交周报个数
    total = get_week_count(plan_id, user_id,token,proxy)
    # # 第几周的周报
    content_entry = get_random_week()
    nowweek = total + 1
    data = {
        "yearmonth": "",
        "address": "",
        "t": aes_encrypt(int(str(time_shift(day_end)) + "000") - 3600),
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
    headers.update({
            'sign':md5_encrypt(week_sign),
            "authorization":token
        })
    time.sleep(random.randint(5, 10))
    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, proxies=proxy,data=json.dumps(data))
    if rsp.json()["code"] == 200 and rsp.json()["msg"]:
        weekly_report_status(user['phone'],"周报提交成功")
        logging.info(f"用户：{user['phone']}周报提交成功 {rsp.text}")
    else:
        # 增加返回值
        logging.info(f"用户：{user['phone']}周报提交失败 {rsp.text}")
         # 当提交日报失败时，调用这个函数并将状态设为API的返回值或错误信息
        weekly_report_status(user['phone'], rsp.text)


# 执行打卡日报周报
def zong(user,user_id: str,plan_id: str,token: str,proxy):
        hourNow = datetime.now(pytz.timezone('PRC')).hour
        # 获取当前日期和时间
        current_datetime = datetime.now()
        # 从当前日期中提取日期和星期几
        current_weekday = current_datetime.strftime('%A')
        if not current_weekday=="Sunday":
            logging.info("开始打卡")
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
            time.sleep(random.randint(5, 10))
            rsp = requests.post(url="https://api.moguding.net:9000/attendence/clock/v2/save", headers=headers2, proxies=proxy,data=json.dumps(data2))
            if rsp.json()["code"] == 200 and rsp.json()["msg"]:
                logging.info(f"用户：{user['phone']}签到成功 {rsp.text}")
                update_punch_status(user['phone'], '签到成功')
                # 如果是打下班卡，将days字段的值减一
                if signType == 'END':
                    update_days(user['phone'])
            else:
                # 增加返回值
                logging.info(f"用户：{user['phone']}签到失败 {rsp.text}")
                # 当打卡失败时，调用这个函数并将状态设为API的返回值或错误信息
                update_punch_status(user['phone'], rsp.text)
            # 开始写日报
            if user['xuanbujiao']==True:
                if 7 <= hourNow < 12:
                    logging.info(f"用户：{user['phone']}提交日报")
                    tijioa_dayk(user,plan_id, user_id,token,proxy)
            # 补交日报
            if user.get('bujiao',False):
                logging.info(f"用户：{user['phone']}补交日报")
                bujiao_start_date=user['bujiao_start_date']
                bujiao_end_date=user['bujiao_end_date']
                bujiao_day(plan_id, user_id, bujiao_start_date, bujiao_end_date,user,token,proxy)
                connection, cursor = get_db_connection()
                try:
                    # 更新指定用户的字段值为 NULL
                    cursor.execute("""
                        UPDATE users 
                        SET bujiao = NULL, bujiao_start_date = NULL, bujiao_end_date = NULL 
                        WHERE phone = %s
                    """, (user['phone'],))
                    # 提交事务
                    connection.commit()
                except Exception as e:
                    logging.warning(f"删除用户字段时出错： {e}")
                finally:
                    # 关闭数据库连接
                    cursor.close()
                    connection.close()    
            # 补交周报
            if user.get('reedy',False):
                logging.info(f"用户：{user['phone']}补交周报")
                weeks = get_weeks(plan_id,token,proxy)
                # print('补交周报' + str(weeks))
                not_submit_week = weeks[:int(user['requirement_week_num']) + 1]
                not_submit_week.reverse()
                week_sign = user_id + "week" + plan_id + "周报" + "3478cbbc33f84bd00d75d7dfa69e0daa"
                for i in not_submit_week:
                    # 获取当前时间
                    now = datetime.now()
                    day_end = now.strftime('%Y-%m-%d %H:%M:%S')
                    time.sleep(10)
                    after_week = get_week_count(plan_id, user_id,token,proxy) + 1
                    # 第几周的周报
                    content_entry = get_random_week()
                    week_end = i["endTime"]
                    week_star = i['startTime']
                    data = {
                        "yearmonth": "",
                        "address": "",
                        "t": aes_encrypt(int(str(time_shift(day_end)) + "000") - 3600),
                        "title": "周报",
                        "longitude": "0.0",
                        "latitude": "0.0",
                        "weeks": f'第{str(after_week)}周',
                        "endTime": week_end,
                        "startTime": week_star,
                        "planId": plan_id,
                        "reportType": "week",
                        "content": content_entry
                            }           
                    headers.update({
                        'sign':md5_encrypt(week_sign),
                        "authorization":token
                    })
                    # print(headers)
                    # print(data)
                    time.sleep(random.randint(5, 10))
                    rsp = requests.post(url="https://api.moguding.net:9000/practice/paper/v5/save", headers=headers, proxies=proxy,data=json.dumps(data))
                    # 解析响应的 JSON 内容
                    response_json = rsp.json()
                    logging.info(f"用户：{user['phone']}提交周报返回值 {response_json}")
                    # 检查 'code' 和 'msg' 的
                    if response_json.get("code") == 200:
                        logging.info(f"用户：{user['phone']}已提交{week_end}")
                    elif response_json.get("code") == 500 and response_json.get("msg") == "此时间段已经写过周记":
                        logging.info(f"用户：{user['phone']}{rsp.text}")

                connection, cursor = get_db_connection()
                try:
                    # 更新指定用户的字段值为 NULL
                    cursor.execute("""
                        UPDATE users
                        SET reedy = NULL, requirement_week_num = NULL
                        WHERE phone = %s
                    """, (user['phone'],))
                    # 提交事务
                    connection.commit()
                except Exception as e:
                    print(f"删除用户字段时出错： {e}")
                finally:
                    # 关闭数据库连接
                    cursor.close()
                    connection.close()
# 周末提交周报
def zhong(plan_id: str, user_id: str,user,token,proxy):
    # 获取当前时间
    hourNow = datetime.now(pytz.timezone('PRC')).hour
    # 获取当前日期和时间
    current_datetime = datetime.now()
    # 从当前日期中提取日期和星期几
    current_weekday = current_datetime.strftime('%A')
    if current_weekday=="Saturday":
        if 7 <= hourNow < 12:
            logging.info(f"用户：{user['phone']}提交周报")
            submit_week(plan_id, user_id,user,token,proxy)

def ip(user):
    json_file_path = 'C:\\Users\\33323\\Desktop\\py代码\\gong\\henan_area_codes.json'
    # 读取JSON文件
    with open(json_file_path, 'r', encoding='utf-8') as file:
        area_codes = json.load(file)
    province = user['province']
    city = user['city']
    # 提取特定地区的数据
    if province in area_codes and city in area_codes[province]:
        district_code = area_codes[province][city]
    else:
        # 从字典中随机选择一个省市组合
        province, cities = random.choice(list(area_codes.items()))
        city, district_code = random.choice(list(cities.items()))
    # 构建 API 请求 URL
    district_url = f"http://{district_code}"
    response = requests.get(district_url)
    if response.status_code == 200:
        data = response.json()
        ip = data['data'][0]['ip']
        port = data['data'][0]['port']
        return f"https://{ip}:{port}"
    else:
        logging.warning("API请求失败")
        return None
    
# 主函数
def main(users):
    # 对每个用户数据进行转换
    for user in users:
        try:
            days = user['days']
            if days == '打卡天数已到期' or (isinstance(days, int) and days <= 0):
                logging.info(f"用户: {user['phone']} 打卡天数已到期或天值小于等于0,跳过打卡操作")
                continue
            connection, cursor = get_db_connection()
            try:
                days_int = int(days)
                if days_int <= 0:
                    logging.warning(f"天值小于或等于0,更新用户状态:{user['phone']}")
                    # 更新数据库中的 days 列
                    cursor.execute("UPDATE users SET days = %s WHERE phone = %s", ("打卡天数已到期", user['phone']))
                    connection.commit()
                    # 同时更新程序中的 days 变量
                    user['days'] = '打卡天数已到期'
                    continue  # 更新后，跳过当前用户的后续处理
            except ValueError:
                logging.info(f"用户:{user['phone']} days 不是整数，不执行操作")
            finally:
                cursor.close()
                connection.close()
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
            proxy=ip(user)
            logging.info(f"用户：{user['phone']}开始获取代理IP:{proxy}")
            # 如果用户没有令牌，则登录并获取令牌并user_id
            if not user.get("token"):
                logging.info(f"手动登录{user['phone']}")
                token, user_id = login(user,proxy)#可能会返回空值，需要判断
                if token is None and user_id is None:
                    logging.warning(f"登录失败，跳过用户：{user['phone']}")
                    continue
                plan_id , token= get_plan(token, user_id,user,proxy)
                if plan_id is None or token is None:
                    logging.warning(f"获取plan_id失败，跳过用户：{user['phone']}")
                    continue
                # 开始签到
                zong(user,user_id,plan_id,token,proxy)
                # 开始提交周报
                if user['zhobao']==True:
                    zhong(plan_id, user_id,user,token,proxy)
                    logging.info(f"用户：{user['phone']}已开启周报，程序执行完成")
                else:
                    logging.info(f"用户：{user['phone']}未开启周报，程序执行完成")
            else:
                logging.info('自动登录对于用户 {}'.format(user["phone"]))
                user_id = user["user_id"]
                token=user["token"]
                plan_id ,token= get_plan(token, user_id,user,proxy) 
                if plan_id is None or token is None:
                    logging.warning(f"获取plan_id失败，跳过用户user{['phone']}")
                    continue
                logging.info(f"用户:{user['phone']}开始签到")   
                # # 开始签到
                zong(user,user_id,plan_id,token,proxy)  
                # 开始提交周报
                if user['zhobao']==True:
                    zhong(plan_id, user_id,user,token,proxy)
                    logging.info(f"用户：{user['phone']}已开启周报，程序执行完成")
                else:
                    logging.info(f"用户：{user['phone']}未开启周报，程序执行完成")
        except Exception as e:
            logging.error(f"main:处理用户时出错 {user['phone']}: {e}")
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
