#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DDmc_exchange.py
Author: 一风一燕
功能：叮咚买菜积分优惠券兑换
Date: 2021-11-24
cron: 59 23 * * * xF_DDmc_exchange.py
new Env('叮咚买菜积分兑换');

****************叮咚买菜是买菜APP，30分钟内到家，挺快挺专业的。如果没有用过叮咚买菜APP的人，可以TG私聊我，我就叫一风一燕，我发个邀请码给你注册，这样双方都有优惠券，也算是支持一下小风，谢谢各位大佬*******************


【教程】：需要自行用手机抓取cookies和token。
在青龙变量中添加变量DD_token，DD_cookies。
多个账号时，DD_token，DD_cookies用&隔开，例如DD_token=xxxxx&xxxx

手机抓包后，叮咚鱼塘活动，喂食一次，查看URL
搜索station_id=，&前面，=后面的东西就是你需要的token。
例如：https://maicai.api.ddxq.mobi/user/info?api_version=9.1.0&app_client_id=1&station_id=xxxx&native_version=&latitude=23.017158&longitude=113.811603
其中station_id=xxxx，xxxx就是token，cookies的话就要自己去该URL中，查看headers（表头）。
抓取运行正常后，只要手机不退出登录，应该是永远不过期的。

在青龙变量中添加变量DDmc_Coupon。填写说明：直接填写优惠券的名字，暂时支持3元无门槛券，5元无门槛券，8元无门槛券,15元满减券。
例子：DDmc_Coupon="5元无门槛券"


如果是多账号，DDmc_accout="1"，就是账号1抢优惠券，填2，就是账号2抢券。目前只支持单个号抢，后续考虑增加并发抢券功能。默认是抢【账号1】



'''


DD_token = ''
DD_cookies = ''
DDmc_Coupon = '8元无门槛券'
DDmc_accout = '1'


'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens = ''
cookies = ''

try:
    import requests
    import json,sys,os,re
    import time,datetime
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"


today = datetime.datetime.now().strftime('%Y-%m-%d')
tomorrow=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

#开始抢兑时间
starttime='23:59:59.00000000'
#结束时间
endtime='00:00:10.00000000'

qgtime = '{} {}'.format (today, starttime)
qgendtime = '{} {}'.format (tomorrow, endtime)


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
#     if "DD_token" in ck:
#         r = re.compile (r'DD_token="(.*?)"', re.M | re.S | re.I)
#         tokens = r.findall(ck)
#         tokens = tokens[0].split ('&')
#         if len (tokens) == 1:
#             DD_token = tokens[0]
#             tokens = ''
#     #     print(tokens)
#     #     tokens = cookies[3]
#
#     printT ("已获取并使用ck环境 token")
# #
# with open(path, "r+", encoding="utf-8") as f:
#     ck = f.read()
#     cookies = ck
#     if "DD_cookies" in ck:
#         r = re.compile (r'DD_cookies="(.*?)"', re.M | re.S | re.I)
#         cookies = r.findall (ck)
#         cookies = cookies[0].split('&')
#     if len(cookies) == 1:
#         DD_cookies = cookies[0]
#         cookies = ''
#     #     print(cookies)
#     #     cookies = cookies[3]
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

if "DDmc_Coupon" in os.environ:
    DDmc_Coupon = os.environ["DDmc_Coupon"]
    printT (f"已获取并使用Env环境DDmc_Coupon，兑换{DDmc_Coupon}")
else:
    print("DDmc_Coupon未填写")
    exit(0)

if "DDmc_accout" in os.environ:
    DDmc_accout = os.environ["DDmc_accout"]
    printT ("已获取并使用Env环境DDmc_accout")
else:
    print("DDmc_accout未填写")


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
    tokens = tokens.split ('&')
    DD_token = tokens[int(DDmc_accout)-1]
    if len (tokens) == 1:
        DD_token = tokens[0]
    else:
        pass

if cookies != '':
    cookies = cookies.split ('&')
    DD_cookies = cookies[int(DDmc_accout)-1]
    if len (cookies) == 1:
        DD_cookies = cookies[0]
    else:
        pass

#获取个人信息
def get_info(DD_token,DD_cookies):
    try:
        info_url = f'https://maicai.api.ddxq.mobi/user/info?api_version=9.1.0&app_client_id=1&station_id={DD_token}&native_version=&app_version=9.35.1&latitude=23.017158&longitude=113.811603'
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
        result = response.json()
        # print(result)
        name = result['data']['name']
        id = result['data']['id']
        return name,id
    except Exception as e:
        print(e)
        msg ("{0}获取个人信息失败,可能是DD_token 和 cookies过期".format(DD_token))

#获取activityId
def get_activityId(DD_token,DD_cookies,name):
    try:
        info_url = f'https://gw.api.ddxq.mobi/promocore-service/client/maicai/mcActivityClient/v1/listByStationId'
        info_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.35.1 station_id/{DD_token}",
            "Referer": "https://activity.m.ddxq.mobi/",
            "Host": "gw.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://activity.m.ddxq.mobi",
            "content-type":"application/json;charset=UTF-8",

        }
        data = r'{"api_version":"9.7.3","app_version":"1.0.0","app_client_id":3,"station_id":"' + f'{DD_token}' + r'","native_version":"9.39.1","city_number":"1117","latitude":23.017158,"longitude":113.811603,"biz_type":"POINT_BUY_TICKET"}'
        # print(data)
        response = requests.post (url=info_url, headers=info_headers, verify=False,data=data)
        result = response.json()
        # print(result)
        if DDmc_Coupon == '3元无门槛券':
            activityId = result['data'][3]['prizes'][0]['activityId']
        elif DDmc_Coupon == '5元无门槛券':
            activityId = result['data'][2]['prizes'][0]['activityId']
        elif DDmc_Coupon == '8元无门槛券':
            activityId = result['data'][1]['prizes'][0]['activityId']
        elif DDmc_Coupon == '15元满减券':
            activityId = result['data'][0]['prizes'][0]['activityId']
        else:
            msg("DDmc_Coupon未填写，不兑换")
        # print(activityId)
        return activityId
    except Exception as e:
        print(e)
        msg ("{0}获取优惠券ID失败,可能是DD_token过期".format(name))


#执行兑换
def exchange(name,DD_token,DD_cookies,activityId):
    try:
        printT (f"抢购时间为：{qgtime}")
        printT (f"正在等待兑换时间，请勿终止退出...")
        while True:
            nowtime1 = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
            if nowtime1 > qgtime:
                nowtime = int (round (time.time () * 1000))
                url = f'https://gw.api.ddxq.mobi/promocore-service/client/maicai/mcActivityTrigger/v1/trigger'
                data = f'api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id={DD_token}&native_version=9.39.1&city_number=1117&latitude=23.017158&longitude=113.811603&activityId={activityId}&bizNo={nowtime}'
                # data = f'api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id=60ace35775474200016efe49&native_version=9.39.1&city_number=1117&latitude=23.017158&longitude=113.811603&activityId=AC2020085xw2o0d01ne60000&bizNo=1637683242226'
                heards = {
                    "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
                    "Cookie": DD_cookies,
                    "Referer": "https://activity.m.ddxq.mobi/",
                    "Accept-Encoding": "gzip, deflate, br",
                    "origin": "https://activity.m.ddxq.mobi",
                    "accept-language": "zh-CN,zh-Hans;q=0.9",
                    "accept": "*/*",
                    "content-type": "application/x-www-form-urlencoded",
                    "host":"gw.api.ddxq.mobi",
                    "content-length":"222",
                }
                response = requests.post(url=url,data=data,headers=heards,verify=False)
                result = response.json()
                print(result)
                messge = result['msg']
                code = result['code']
                if code == 0:
                    msg("【账号{0}】兑换{1}成功".format(name,DDmc_Coupon))
                    break
            elif nowtime1 > qgendtime:
                msg("超过兑换时间，退出执行".format(name))
                break

    except Exception as e:
        print(e)
        msg('叮咚积分优惠券兑换{}异常，可能是token过期'.format (name))


if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行叮咚积分优惠券兑换脚本==============")
    print(DD_token)
    print(DD_cookies)
    name,uid = get_info(DD_token,DD_cookies)
    msg (f"单账号兑换模式，兑换【账号{DDmc_accout}{name}】")
    activityId = get_activityId (DD_token, DD_cookies, name)
    exchange(name,DD_token,DD_cookies,activityId)
    if "成功" in msg_info:
        send("叮咚积分优惠券兑换", msg_info)
    elif "过期" in msg_info:
        send("叮咚积分优惠券兑换", msg_info)
