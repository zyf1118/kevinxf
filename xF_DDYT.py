#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DDYT.py
Author: 一风一燕
功能：叮咚买菜鱼塘活动
Date: 2021-09-16
cron: 22 7,10,17 * * * xF_DDYT.py
new Env('叮咚鱼塘活动');

****************叮咚买菜是买菜APP，30分钟内到家，挺快挺专业的。如果没有用过叮咚买菜APP的人，可以TG私聊我，我就叫一风一燕，我发个邀请码给你注册，这样双方都有优惠券，也算是支持一下小风，谢谢各位大佬*******************


【教程】：需要自行用手机抓取cookies和token。
在青龙变量中添加变量DD_token，DD_cookies。
多个账号时，DD_token，DD_cookies用&隔开，例如DD_token=xxxxx&xxxx

手机抓包后，查看URL
搜索station_id=，&前面，=后面的东西就是你需要的token。
例如：https://maicai.api.ddxq.mobi/user/info?api_version=9.7.3&app_client_id=4&station_id=xxxx&native_version=&latitude=23.017158&longitude=113.811603
其中station_id=xxxx，xxxx就是token，cookies的话就要自己去该URL中，查看headers（表头）。
抓取运行正常后，只要手机不退出登录，应该是永远不过期的。

可以用手机抓包，也可以用微信小程序抓。

cron时间填写：22 7,10,17 * * *

'''


DD_token = ''
DD_cookies = ''


'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens = ''
cookies = ''

try:
    import requests
    import json,sys,os,re
    import time,datetime,random
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"
today = datetime.datetime.now().strftime('%Y-%m-%d')
mor_time ='08:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)

uuid = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 15))
device_token = ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdefABCDEFGHIJKLMNOPQROTUVWXYZ', 69)) + r"+" + ''.join(random.sample('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 18)) + r"=="


def printT(s):
    print("[【{0}】]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


def getEnvs(label):
    try:
        if label == 'True' or label == 'yes' or label == 'true' or label == 'Yes':
            return True
        elif label == 'False' or label == 'no' or label == 'false' or label == 'No':
            return False
    except:
        pass
    try:
        if '.' in label:
            return float(label)
        elif '&' in label:
            return label.split('&')
        elif '@' in label:
            return label.split('@')
        else:
            return int(label)
    except:
        return label

##############      在pycharm测试ql环境用，实际用下面的代码运行      #########

# with open(path, "r+", encoding="utf-8") as f:
#     ck = f.read()
#     tokens = ck
#     # if "DD_token" in ck:
#     #     r = re.compile (r'DD_token="(.*?)"', re.M | re.S | re.I)
#     #     tokens = r.findall(ck)
#     #     tokens = tokens[0].split ('&')
#     #     if len (tokens) == 1:
#     #         DD_token = tokens[0]
#     #         tokens = ''
#     # #     print(tokens)
#     # #     tokens = cookies[3]
#     #     else:
#     #         DD_token = tokens[0]
#     # printT ("已获取并使用ck环境 token")
#
# with open(path, "r+", encoding="utf-8") as f:
#     ck = f.read()
#     cookies = ck
#     # if "DD_cookies" in ck:
#     #     r = re.compile (r'DD_cookies="(.*?)"', re.M | re.S | re.I)
#     #     cookies = r.findall (ck)
#     #     cookies = cookies[0].split('&')
#     # if len(cookies) == 1:
#     #     DD_cookies = cookies[0]
#     #     cookies = ''
#     # #     print(cookies)
#     # #     cookies = cookies[3]
#     # else:
#     #     DD_cookies = cookies[0]
#     printT ("已获取并使用ck环境 DD_cookies")

########################################################################

if "DD_token" in os.environ:
    print(len (os.environ["DD_token"]))
    if len (os.environ["DD_token"]) > 24:
        tokens = os.environ["DD_token"]
        # temporary = cookies.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境DD_token")
    else:
        DD_token = os.environ["DD_token"]
else:
    print("检查变量DD_token是否已填写")

if "DD_cookies" in os.environ:
    print(len (os.environ["DD_cookies"]))
    if len (os.environ["DD_cookies"]) > 43:
        cookies = os.environ["DD_cookies"]
        # temporary = cookies.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境DD_cookies")
    else:
        DD_cookies = os.environ["DD_cookies"]
else:
    print("检查变量DD_cookies是否已填写")


## 获取通知服务
class msg(object):
    def __init__(self, m=''):
        self.str_msg = m
        self.message()
    def message(self):
        global msg_info
        printT(self.str_msg)
        try:
            msg_info = "{}\n{}".format(msg_info, self.str_msg)
        except:
            msg_info = "{}".format(self.str_msg)
        sys.stdout.flush()           #这代码的作用就是刷新缓冲区。
                                     # 当我们打印一些字符时，并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区，然后再打印。
                                     # 这就存在一个问题，如果你想等时间间隔的打印一些字符，但由于缓冲区没满，不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。
    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get(url)
            if 'curtinlv' in response.text:
                with open('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write(response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify(a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify(a)
            else:
                pass
    def main(self):
        global send
        cur_path = os.path.abspath(os.path.dirname(__file__))
        sys.path.append(cur_path)
        if os.path.exists(cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify()
                try:
                    from sendNotify import send
                except:
                    printT("加载通知服务失败~")
        else:
            self.getsendNotify()
            try:
                from sendNotify import send
            except:
                printT("加载通知服务失败~")
        ###################
msg().main()
nowtime = int(round(time.time() * 1000))


uid = ''

if tokens != '':
    # if "DD_token" in tokens:
        # r = re.compile (r'DD_token="(.*?)"', re.M | re.S | re.I)
        # tokens = r.findall (ck)
        tokens = tokens.split ('&')
        # print(tokens)
        if len (tokens) == 1:
            DD_token = tokens[0]

        else:
            pass

if cookies != '':
    # if "DD_cookies" in cookies:
    #     r = re.compile (r'DD_cookies="(.*?)"', re.M | re.S | re.I)
    #     cookies = r.findall (ck)
        cookies = cookies.split ('&')
        # print(cookies)
        if len (cookies) == 1:
            DD_cookies = cookies[0]

        else:
            pass


#获取个人信息
def get_info(DD_token,DD_cookies):
    try:
        info_url = f'https://maicai.api.ddxq.mobi/user/info?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token='
        info_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "Host": "maicai.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://game.m.ddxq.mobi",
            "Accept-Language": "zh-cn",
        }
        response = requests.get (url=info_url, headers=info_headers, verify=False)
        list = response.json()
        # print(list)
        name = list['data']['name']
        id = list['data']['id']
        return name,id
    except Exception as e:
        print(e)
        msg ("{0}获取个人信息失败,可能是app_client_id过期".format(DD_token))

#获取今日任务列表信息
def tasklist_info(name,uid,DD_token,DD_cookies):
    try:
        tasklist_url = f'https://farm.api.ddxq.mobi/api/v2/task/list?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token=&gameId=1&cityCode=1117'
        view_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": f"https://cms.api.ddxq.mobi/cms-service/client/page/v1/getPageInfo?uuid={uuid}&themeColor=72b1ff&hideShare=true&gameTask=BROWSE_GOODS&s=mine_farm_new&native_city_number=1117",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://cms.api.ddxq.mobi",
        }
        response = requests.get (url=tasklist_url, headers=view_headers, verify=False)
        result = response.json()
        # print(list)
        list = result['data']['userTasks']
        for i in range(len(list)):
            taskName = list[i]['taskName']
            if "翻牌" in taskName:
                lucky_draw_id = list[i]['userTaskLogId']
            if "浏览商品" in taskName:
                view_id = list[i]['userTaskLogId']
        return view_id,lucky_draw_id
    except Exception as e:
        print(e)
        msg ("【{0}】获取任务列表失败,可能是cookies过期".format(name))

def do_feed(name,uid,DD_token,DD_cookies):
    try:
        url = "https://farm.api.ddxq.mobi/api/v2/userguide/detail?api_version=9.7.3&app_client_id=2&native_version=&app_version=9.29.0&gameId=1&guideCode=FISHPOND_NEW"
        headers = {
            "User-Agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15D148 xzone/9.35.1 station_id/{DD_token}",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "cookie": DD_cookies
        }
        r = requests.get (url, headers=headers, verify=False).text
        seedid = re.findall (r'"seedId":"(.*?)"', r)[0]
        feed_url = f'https://farm.api.ddxq.mobi/api/v2/props/feed?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token=&gameId=1&propsId={seedid}&seedId={seedid}&cityCode=1117&feedPro=0&triggerMultiFeed=1'
        #feed_url = f'https://farm.api.ddxq.mobi/api/v2/props/feed?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=9.42.1&OSVersion=15&CityId=1117&uid={uid}&latitude=23.017158&longitude=113.811603&lat=23.017158&lng=113.811603&device_token={device_token}&gameId=1&propsId={seedid}&seedId={seedid}&cityCode=1117&feedPro=0&triggerMultiFeed=1'
        feed_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15D148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://game.m.ddxq.mobi",
        }
        i = 0
        total = 10
        flag = 0
        while True:
            response1_zyf = requests.get(url=feed_url,headers=feed_headers,verify=False)
            feed1_ = response1_zyf.json()
            # print(feed1_)
            code = feed1_['code']
            if code == 1125:
                msg('【{0}】退出喂食，鱼饵不足10g'.format(name))
                break
            elif code == '405':
                msg("【{0}】喂食异常,风控账号，请手动喂食试试".format(name))
                flag = 1
                break
            success1 = feed1_['success']        #是否喂食成功
            if success1 == True:
                amount1 = feed1_['data']['feed']['amount']  # 剩余鱼饵
                is_done = feed1_['data']['seed']['expPercent']  # 完成度
                if amount1 <= 30:
                    printT("【{0}】当前鱼饵不足30g，退出喂食".format(name))
                    #msg ("本次总共成功喂食【{0}】g，剩余鱼饵{1}g，已完成进度{1}%".format (total, amount1, is_done))
                    break
                i += 1
                total = i * 10
                time.sleep(1)
            else:
                break
        if code != 1125 and flag == 0:
            msg("【{0}】本次总共成功喂食{1}g，剩余鱼饵{2}g，已完成进度{3}%".format(name,total,amount1,is_done))

    except Exception as e:
        print (e)
        msg ("【{0}】鱼终于喂饱了，上线领取奖励啦！！".format (name))
        send ("叮咚买菜鱼塘活动", msg_info)

#每日签到任务
def do_sign(name,uid,DD_token,DD_cookies):
    try:
        do_sign1_url = f'https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token=&gameId=1&taskCode=DAILY_SIGN'
        do_sign1_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
            "Cookie": DD_cookies,
        }
        response = requests.get (url=do_sign1_url, headers=do_sign1_headers, verify=False)
        list = response.json()
        print(list)
        success = list['success']     #任务签到
        code = list['code']
        if code == 601:
            printT("【{0}】今日已完成每日签到任务,无需重复签到".format(name))
            return 0
        if success == True:
            #amount = list['data']['rewards']['amount']  # 本次任务获得鱼饵
            amount = list['data']['rewards'][0]['amount']  # 本次任务获得鱼饵
            msg("【{0}】签到任务已完成，获得{1}g鱼饵".format (name,amount))
        elif success == False and code != 601:
            msg("【{0}】每日签到任务失败".format(name))
    except Exception as e:
        print(e)
        # msg("【{0}】每日签到任务失败,可能是cookies过期".format(name))

#连续签到任务
def do_sign2(name,uid,DD_token,DD_cookies):
    try:
        do_sign2_url = f'https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.7.3&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token=&gameId=1&taskCode=CONTINUOUS_SIGN'
        do_sign1_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
            "Cookie": DD_cookies,
        }
        response = requests.get (url=do_sign2_url, headers=do_sign1_headers, verify=False)
        list = response.json()
        success = list['success']  # 连续签到任务
        code = list['code']
        if code == 601:
            printT("【【{0}】】今日已完成连续签到任务,无需重复签到".format(name))
            return 0
        if success == True:
            #amount = list['data']['rewards']['amount']  # 本次任务获得鱼饵
            amount = list['data']['rewards'][0]['amount']  # 本次任务获得鱼饵
            msg("【{0}】连续签到任务已完成，获得{1}g鱼饵".format (name,amount))
        elif success == False and code != 601:
            msg("【{0}】连续签到任务失败".format(name))

    except Exception as e:
        print(e)
        # msg("【{0}】连续签到任务失败,可能是cookies过期".format(name))

def lucky_draw(name,DD_token,DD_cookies):

    i=1
    while True:
        try:
            lucky_draw_url = f'https://farm.api.ddxq.mobi/api/v2/lucky-draw-activity/draw?api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id={DD_token}&native_version=9.35.1&city_number=1117&latitude=23.017158&longitude=113.811603&gameId=1'
            do_sign1_headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
                "Cookie": DD_cookies,
            }
            reward = 0
            response = requests.get (url=lucky_draw_url, headers=do_sign1_headers, verify=False)
            list = response.json ()
            print(list)
            success = list['success']     #天天翻牌，可翻10次
            print(success)
            code = list['code']
            time.sleep(1)
            if success == True:
                reward = list['data']['chosen']['name']
                print('【{0}】第{1}次翻牌，获得{2}'.format(name,i,reward))
                i += 1
                if i == 11:
                    msg("【{0}】已翻牌10次，获取的奖励可查看日志".format(name))
                    break
            elif success == False and code == 1119 and i == 1:
                msg("【{0}】天天翻牌任务已完成，跳过执行环节".format(name))
                break
            elif code == 801:
                msg ("【{0}】鱼饵不足5g，退出翻牌任务".format(name))
                break
            else:
                if success == False:
                    break

        except Exception as e:
            print (e)
            msg("【{0}】天天翻牌任务失败,自行查看是否有翻牌任务".format(name))
            return 0

#领取天天翻牌奖励
def lucky_draw_reward(name,uid,taskid,DD_token,DD_cookies):
    try:
        lucky_draw_reward_url = f'https://farm.api.ddxq.mobi/api/v2/task/reward?api_version=9.7.3&app_client_id=4&station_id={DD_token}&native_version=&app_version=9.35.1&uid={uid}&latitude=23.017158&longitude=113.811603&gameId=1&userTaskLogId={taskid}'
        reward_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://game.m.ddxq.mobi",
        }
        response = requests.get (url=lucky_draw_reward_url, headers=reward_headers, verify=False)
        list = response.json ()
        success = list['success']
        code = list['code']
        if code == 810:
            msg ("【{0}】天天翻牌奖励已领取，去领其他奖励吧".format(name))
        if success == True:
            # amount = list['data']['rewards']['amount']  # 本次任务获得鱼饵
            amount = list['data']['rewards'][0]['amount']  # 本次任务获得鱼饵
            msg ("【{0}】领取天天翻牌奖励{1}g鱼饵".format (name,amount))
    except Exception as e:
        print(e)
        msg("【{0}】领取天天翻牌奖励失败,自行查看是否有翻牌任务".format(name))
#浏览30秒任务
def view_mission(name,uid,DD_token,DD_cookies):
    try:
        view_url = f'https://farm.api.ddxq.mobi/api/v2/task/achieve?latitude=23.018&longitude=113.758948&env=PE&station_id={DD_token}&city_number=1117&api_version=9.44.0&app_client_id=4&native_version=0&h5_source=&page_type=&gameId=1&taskCode=BROWSE_GOODS&'
        view_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": f"https://cms.api.ddxq.mobi/cms-service/client/page/v1/getPageInfo?uuid={uuid}&themeColor=72b1ff&hideShare=true&gameTask=BROWSE_GOODS&s=mine_farm_new&native_city_number=1117",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://cms.api.ddxq.mobi",
        }
        response = requests.get(url=view_url, headers=view_headers, verify=False)
        list = response.json()
        print(list)
        code = list['code']
        if code == 0:
            printT("【{0}】正在执行浏览任务，等待30秒".format(name))
            time.sleep(30)
            msg ("【{0}】浏览任务已完成".format(name))
        if code == 601:
            printT("【{0}】浏览任务早已完成，跳过执行环节".format(name))
    except Exception as e:
        print (e)
        msg ("【{0}】浏览任务失败,可能是cookies过期".format(name))

#领取浏览任务奖励
def do_reward(name,uid,taskid,DD_token,DD_cookies):
    try:
        view_reward_url = f'https://farm.api.ddxq.mobi/api/v2/task/reward?api_version=9.7.3&app_client_id=4&station_id={DD_token}&native_version=&app_version=9.35.1&uid={uid}&latitude=23.017158&longitude=113.811603&gameId=1&userTaskLogId={taskid}'
        reward_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://game.m.ddxq.mobi",
        }
        response = requests.get (url=view_reward_url, headers=reward_headers, verify=False)
        list = response.json ()
        # print(name,list)
        code = list['code']
        if code == 810:
            msg ("【{0}】浏览任务已领取奖励，去领其他奖励吧".format(name))
        elif code == 0:
            amount = list['data']['rewards'][0]['amount']  # 本次任务获得鱼饵
            msg ("【{0}】浏览任务已完成，领取奖励{1}g鱼饵".format(name,amount))
    except Exception as e:
        print (e)
        msg ("【{0}】领取浏览任务奖励失败,可能是cookies过期".format(name))

def fudai_reward(name,uid,DD_token,DD_cookies):
    try:
        fudai_reward_url = f'https://farm.api.ddxq.mobi/api/v2/task/achieve?api_version=9.7.3&app_client_id=4&station_id={DD_token}&native_version=&app_version=9.35.1&uid={uid}&latitude=23.017158&longitude=113.811603&gameId=1&taskCode=LOTTERY'
        reward_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://game.m.ddxq.mobi/index.html",
            "Host": "farm.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://game.m.ddxq.mobi",
        }
        response = requests.get (url=fudai_reward_url, headers=reward_headers, verify=False)
        list = response.json()
        print(list)
        code = list['code']
        if code != 0:
            msg ("【{0}】未到领取福袋时间".format(name))
            return 0
        amount = list['data']['rewards'][0]['amount']  # 本次任务获得鱼饵
        msg ("【{0}】已领取福袋奖励，本时间段获得{1}g鱼饵".format (name,amount))
    except Exception as e:
        print (e)
        msg ("【{0}】领取福袋奖励失败,可能是cookies过期".format(name))
if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行叮咚鱼塘活动脚本==============")
    # print(DD_token,DD_cookies)
    if DD_token != '' and DD_cookies != '':
        name,uid = get_info(DD_token,DD_cookies)
        do_sign (name,uid,DD_token,DD_cookies)
        do_sign2 (name,uid,DD_token,DD_cookies)
        fudai_reward (name,uid,DD_token,DD_cookies)
        lucky_draw(name,DD_token,DD_cookies)
        view_mission (name,uid,DD_token,DD_cookies)
        view_id, lucky_draw_id = tasklist_info (name,uid,DD_token,DD_cookies)
        lucky_draw_reward (name,uid,lucky_draw_id,DD_token,DD_cookies)
        do_reward (name,uid,view_id,DD_token,DD_cookies)
        do_feed (name,uid,DD_token,DD_cookies)
    elif tokens == '' or  cookies == '':
        print("检查变量DD_token，DD_cookies是否已填写")
    else:
        for i,j in zip(tokens,cookies):             #同时遍历两个list，需要用ZIP打包
            name, uid = get_info (i, j)
            do_sign (name, uid, i, j)
            do_sign2 (name, uid, i, j)
            fudai_reward (name, uid, i, j)
            lucky_draw (name, i, j)
            view_mission (name, uid,i, j)
            view_id, lucky_draw_id = tasklist_info (name, uid, i, j)
            lucky_draw_reward (name, uid, lucky_draw_id, i, j)
            do_reward (name,uid, view_id, i, j)
            do_feed (name,uid,i, j)
    if "已完成" in msg_info:
        send("叮咚买菜鱼塘活动", msg_info)
    elif "过期" in msg_info:
        send("叮咚买菜鱼塘活动", msg_info)
