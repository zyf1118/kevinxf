#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_Sign_GZ_G5.py
Author: 一风一燕
功能：滴滴出行积分签到+抽奖
Date: 2021-11-4
cron: 22 5,10 * * * xF_Sign_GZ_G5.py
new Env('广州5号停机坪微信小程序签到');


***********************************


【教程】：需要自行用手机抓取WHTJP_token。
手机抓包后，在URL下，https://m.mallcoo.cn/api/user/user/GetNoticeFavoriteAndCheckinCount，抓取文本或者json文本里面的token，就是该变量了。

在青龙变量中添加变量WHTJP_token="xxxxx"

多个账号时，WHTJP_token，用&隔开，例如WHTJP_token=”xxxxx&xxxx“

这是广州的5号停机坪，不知道别的地方有没有，积分就是能100积分能换3个小时的免费停车。

cron时间填写：22 7,10 * * *

'''


WHTJP_token = ''



'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens = ''


try:
    import requests
    import json,sys,os,re
    import time,datetime
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"


day = time.localtime()



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
#    ck = f.read()
#    tokens = ck
#    if "WHTJP_token" in ck:
#        r = re.compile (r'WHTJP_token="(.*?)"', re.M | re.S | re.I)
#        tokens = r.findall(ck)
#        tokens = tokens[0].split ('&')
#        if len (tokens) == 1:
#            WHTJP_token = tokens[0]
#            tokens = ''
#            # print(tokens)
#            # tokens = cookies[3]
#        else:
#            pass
#    printT ("已获取并使用ck环境 token")

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

if "WHTJP_token" in os.environ:
    print(len (os.environ["WHTJP_token"]))
    if len (os.environ["WHTJP_token"]) > 40:
        tokens = os.environ["WHTJP_token"]
        tokens = tokens.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境WHTJP_token")
    else:
        WHTJP_token = os.environ["WHTJP_token"]
else:
    print("检查变量WHTJP_token是否已填写")


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




if tokens != '':
    # if "WHTJP_token" in tokens:
    # r = re.compile (r'WHTJP_token="(.*?)"', re.M | re.S | re.I)
    # tokens = r.findall (ck)
    # tokens = tokens.split ('&')
    # print(tokens)
    if len (tokens) == 1:
        WHTJP_token = tokens[0]
    else:
        pass


#获取个人信息
def get_info(WHTJP_token,accout):
    try:
        info_url = f'https://m.mallcoo.cn/api/user/user/GetUserAndMallCard'
        data = r'{"MallId":12014,"Header":{"Token":' + f'"{WHTJP_token}"' + r',"systemInfo":{"model":"microsoft","SDKVersion":"2.19.2","system":"Windows 10 x64","version":"3.4.0","miniVersion":"2.5.49"}}}'
        print(data)
        info_heards = {
            "user-agent": f"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxa878c7c2d96608ad/4/page-frame.html",
            "Host": "m.mallcoo.cn",
            "content-type": "application/json",
        }
        response = requests.post (url=info_url, headers=info_heards, data=data, verify=False)
        result = response.json ()
        # print (result)
        Bonus = result['d']['Bonus']
        NickName = result['d']['NickName']
        msg("【账号{0}】现有积分为:{1}".format(NickName,Bonus))
        return NickName

    except Exception as e:
        print (e)
        msg ("【账号{0}】获取个人积分失败,可能是token过期".format (accout))

#签到
def do_sign(WHTJP_token,accout):
    try:
        info_url = f'https://m.mallcoo.cn/api/user/User/CheckinV2'
        info_headers = {
            "user-agent": f"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxa878c7c2d96608ad/4/page-frame.html",
            "Host": "m.mallcoo.cn",
            "content-type": "application/json",
        }
        data = r'{"MallId":12014,"Header":{"Token":' + f'"{WHTJP_token}"' + r',"systemInfo":{"model":"microsoft","SDKVersion":"2.19.2","system":"Windows 10 x64","version":"3.4.0","miniVersion":"2.5.49"}}}'
        # print(data)
        response = requests.post(url=info_url, headers=info_headers, verify=False,data=data)
        result = response.json()
        print(result)
        NickName = result['d']['NickName']
        Msg = result['d']['Msg']
        if "签到成功" in Msg:
            msg("【账号{0}】{1}".format(NickName,Msg))
        return NickName

    except Exception as e:
        print(e)
        msg ("【账号{0}】获取签到失败,可能是token过期".format(accout))


#签到情况
def get_signinfo(WHTJP_token,NickName,accout):
    try:
        sign_info_url = f'https://m.mallcoo.cn/api/user/User/GetCheckinDetail'
        sign_info_headers = {
            "user-agent": f"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36 MicroMessenger/7.0.9.501 NetType/WIFI MiniProgramEnv/Windows WindowsWechat",
            "Referer": "https://servicewechat.com/wxa878c7c2d96608ad/4/page-frame.html",
            "Host": "m.mallcoo.cn",
            "content-type": "application/json",
        }
        data = r'{"MallId":12014,"Header":{"Token":' + f'"{WHTJP_token}"' + r',"systemInfo":{"model":"microsoft","SDKVersion":"2.19.2","system":"Windows 10 x64","version":"3.4.0","miniVersion":"2.5.49"}}}'
        # print(data)
        response = requests.post(url=sign_info_url, headers=sign_info_headers, verify=False,data=data)
        result = response.json()
        print(result)
        sign_days = result['d']['ContinueDay']
        msg("【账号{0}】连续签到{1}天".format(NickName,sign_days))

    except Exception as e:
        print(e)
        msg ("【账号{0}】获取签到情况失败,可能是cookies过期".format(accout))

#抽奖活动
def do_Lottery(WHTJP_token,accout):
    try:
        flag = 6
        # nowtime = int (round (time.time () * 1000))
        while True:
            do_Lottery_url = f'https://bosp-api.xiaojukeji.com/bosp-api/lottery/draw?lid={lid}&token={WHTJP_token}&env=%7B%22longitude%22%3A113.81251003689236%2C%22latitude%22%3A23.016395128038194%2C%22cityId%22%3A%2221%22%2C%22deviceId%22%3A%2299d8f16bacaef4eef6c151bcdfa095f0%22%2C%22ddfp%22%3A%2299d8f16bacaef4eef6c151bcdfa095f0%22%2C%22appVersion%22%3A%226.2.4%22%2C%22wifi%22%3A1%2C%22model%22%3A%22iPhone%2011%22%2C%22timeCost%22%3A637425%2C%22userAgent%22%3A%22Mozilla%2F5.0%20(iPhone%3B%20CPU%20iPhone%20OS%2015_0%20like%20Mac%20OS%20X)%20AppleWebKit%2F605.1.15%20(KHTML%2C%20like%20Gecko)%20Mobile%2F15E148%20didi.passenger%2F6.2.4%20FusionKit%2F1.2.20%20OffMode%2F0%22%2C%22isHitButton%22%3Atrue%7D'
            do_Lottery_headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Accept-Encoding": "gzip, deflate, br",
                # "Connection": "keep-alive",
                "Accept": "application/json, text/plain, */*",
                "Referer": "https://page.udache.com/",
                "Host": "bosp-api.xiaojukeji.com",
                "Origin": "https://page.udache.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                # "content-type":"application/json; charset=utf-8",
                # "content-length":"272",
            }
            response = requests.get(url=do_Lottery_url, headers=do_Lottery_headers, verify=False)
            result = response.json()
            print(result)
            code = result['code']
            if code == 20003:
                msg("【账号{}】抽奖次数已达上限，跳出抽奖环节".format(accout))
                break
            elif code == 20017:
                msg("【账号{}】抽奖操作过频，稍后再试".format(accout))
                break
            elif code == 20008:
                msg("【账号{}】抽奖lid过期，请重新抓包更新".format(accout))
            elif code == 20010:
                msg ("【账号{}】积分不足9分，跳出抽奖环节".format (accout))
                break
            else:
                draw_times = result['data']['userinfo']['draw_times']
                flag = 6 - int(draw_times)
                name = result['data']['prize']['name']
                current_point = result['data']['userinfo']['current_point']
                msg("【账号{3}】第{0}次抽奖获得{1},现账号共有{2}积分".format(flag,name,current_point,accout))
                time.sleep(5)
    except Exception as e:
        print(e)
        msg ("【账号{0}】抽奖失败,可能是cookies过期".format(accout))


if __name__ == '__main__':
    # global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行G5停机坪签到脚本==============")
    if WHTJP_token != '':
        accout = 1
        Nickname = do_sign(WHTJP_token,accout)
        get_signinfo(WHTJP_token,Nickname,accout)
        get_info(WHTJP_token,accout)
    elif tokens == '' :
        print("检查变量WHTJP_token")
    elif len(tokens) > 1 :
        accout = 1
        for i in tokens:             #同时遍历两个list，需要用ZIP打包
            Nickname = do_sign (i, accout)
            get_signinfo (i, Nickname, accout)
            get_info (i, accout)
            accout += 1
    if "签到" in msg_info:
        send("G5停机坪签到", msg_info)
    elif "过期" in msg_info:
        send("G5停机坪签到", msg_info)