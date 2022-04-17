#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DDmc_Sign
Author: 一风一燕
功能：叮咚买菜积分签到功能
Date: 2021-09-16
cron: 22 7,10 * * * xF_DDmc_Sign
new Env('叮咚买菜积分活动');

****************叮咚买菜是买菜APP，30分钟内到家，挺快挺专业的。如果没有用过叮咚买菜APP的人，可以TG私聊我，我就叫一风一燕，我发个邀请码给你注册，这样双方都有优惠券，也算是支持一下小风，谢谢各位大佬*******************


【教程】：需要自行用手机抓取cookies和token。
在青龙变量中添加变量DD_token，DD_cookies。
多个账号时，DD_token，DD_cookies用&隔开，例如DD_token=xxxxx&xxxx

手机抓包后，喂食一次，查看URL
搜索station_id=，&前面，=后面的东西就是你需要的token。
例如：https://maicai.api.ddxq.mobi/user/info?api_version=9.1.0&app_client_id=1&station_id=xxxx&native_version=&latitude=23.017158&longitude=113.811603
其中station_id=xxxx，xxxx就是token，cookies的话就要自己去该URL中，查看headers（表头）。
抓取运行正常后，只要手机不退出登录，应该是永远不过期的。





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
    import time,datetime
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"
today = datetime.datetime.now().strftime('%Y-%m-%d')
mor_time ='08:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)


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
    if len (os.environ["DD_cookies"]) > 40:
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
        # print (tokens)
        tokens = tokens.split ('&')
        if len (tokens) == 1:
            DD_token = tokens[0]

        else:
            pass

if cookies != '':
    # if "DD_cookies" in cookies:
    #     r = re.compile (r'DD_cookies="(.*?)"', re.M | re.S | re.I)
    #     cookies = r.findall (ck)
    #     print(cookies)
        cookies = cookies.split ('&')
        if len (cookies) == 1:
            DD_cookies = cookies[0]

        else:
            pass


#获取个人信息
def get_info(DD_token,DD_cookies):
    try:
        info_url = f'https://maicai.api.ddxq.mobi/user/info?api_version=9.1.0&app_client_id=4&station_id={DD_token}&stationId={DD_token}&native_version=&app_version=0&OSVersion=&CityId=1117&latitude=23.018&longitude=113.758948&lat=23.018&lng=113.758948&device_token='
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
        msg ("{0}获取个人信息失败,可能是cookies过期".format(DD_token))


#执行积分签到
def do_sign(name,DD_token,DD_cookies):
    try:
        do_sign_url = f'https://sunquan.api.ddxq.mobi/api/v2/user/signin/'
        data = f'api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id={DD_token}&native_version=9.33.0&city_number=1117&latitude=23.017158&longitude=113.811603'
        do_sign_heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
            "Cookie": DD_cookies,
            "Referer": "https://activity.m.ddxq.mobi/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://activity.m.ddxq.mobi",
            "accept-language": "zh-cn",
            "accept": "*/*",
            "content-type": "application/x-www-form-urlencoded",
        }
        response = requests.post(url=do_sign_url,data=data,headers=do_sign_heards,verify=False)
        do_sign_ = response.json()
        #print(do_sign_)
        today_point = do_sign_['data']['point']   #本次签到获得的积分
        time.sleep(1)

        nowtime = int (round (time.time () * 1000))

        url = f'https://maicai.api.ddxq.mobi/point/home?api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id={DD_token}&native_version=9.33.0&city_number=1117&latitude=23.017158&longitude=113.811603&_={nowtime}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 xzone/9.33.0 station_id/{DD_token}",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://activity.m.ddxq.mobi/",
            "Host": "maicai.api.ddxq.mobi",
            "Cookie": DD_cookies,
            "Origin": "https://activity.m.ddxq.mobi",
        }
        response = requests.get(url=url,headers=headers,verify=False)
        result = response.json()
        #print(result)
        point_num = result['data']['point_num']         #查看当前积分
        expire_point_display = result['data']['expire_point_display']   #查看积分有效期

        nowtime = int (round (time.time () * 1000))
        cheak_sign_url = f'https://maicai.api.ddxq.mobi/point/home?api_version=9.7.3&app_version=1.0.0&app_client_id=3&station_id={DD_token}&native_version=9.33.0&city_number=1117&latitude=23.017158&longitude=113.811603'
        cheak_ =  requests.get(url=cheak_sign_url,headers=headers,verify=False)
        cheak_sign = cheak_.json()
        #print(cheak_)
        success = cheak_sign['data']['user_sign']['is_today_sign']  #查看是否已签到
        sign_series = cheak_sign['data']['user_sign']['sign_series']    #查看连续签到多久

        if success == True:
            #print("{1}成功签到，已连续签到{3}天，当前积分为：{0}分。".format(point_num,name2,expire_point_display,sign_series))
            msg("{3}成功签到,本次获得积分{4}，已连续签到{1}天，当前积分为：{0}积分。{2}".format(point_num,sign_series,expire_point_display,name,today_point))
            # if '成功签到' in msg_info:
            #     send("(叮咚买菜)",msg_info)

    except Exception as e:
        print(e)
        msg ('（叮咚买菜积分签到）{}异常，可能是token过期'.format (name))
        send ("叮咚买菜积分签到", msg_info)

if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行叮咚积分签到脚本==============")
    if DD_token != '' and DD_cookies != '':
        name,uid = get_info(DD_token,DD_cookies)
        do_sign (name,DD_token,DD_cookies)

    elif tokens == '' or  cookies == '':
        print("检查变量DD_token，DD_cookies是否已填写")
    else:
        for i,j in zip(tokens,cookies):             #同时遍历两个list，需要用ZIP打包
            name, uid = get_info (i, j)
            do_sign (name, i, j)

    if "成功签到" in msg_info:
        send("叮咚买菜积分签到", msg_info)
    elif "过期" in msg_info:
        send("叮咚买菜积分签到", msg_info)
