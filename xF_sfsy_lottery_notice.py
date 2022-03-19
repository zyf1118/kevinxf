#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_sfsy_lottery_notice.py
Author: 一风一燕
功能：顺丰速递app抽奖奖品通知脚本
Date: 2022-03-18
cron: 6 15 * * * xF_sfsy_lottery_notice.py
new Env('顺丰速递app自动任务');



【教程】：
变量lottery_black_list，屏蔽通知，抽到这些奖励，不通知，可参考我的再自行修改。
export lottery_black_list='同城8折券&2元通用券&3元通用券&1元通用券&腾讯视频月卡&元气森林抵扣券&十倍积分&翻倍积分&5积分'

cron时间填写：6 15 * * * xF_sfsy.py

'''

SF_cookie = ''
lottery_black_list = ''
account = 1
cookies = ''
'''


=================================以下代码不懂不要随便乱动=================================


'''

try:
    import requests
    import json, sys, os, re
    import time, datetime, random
except Exception as e:
    print (e)

requests.packages.urllib3.disable_warnings ()

if "@" in lottery_black_list:
    lottery_black_list = lottery_black_list.split ('@')
pwd = os.path.dirname (os.path.abspath (__file__)) + os.sep
path = pwd + "env.sh"
today = datetime.datetime.now ().strftime ('%Y-%m-%d')
mor_time = '08:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)
nowtime = int (round (time.time () * 1000))


def printT(s):
    print ("[【{0}】]: {1}".format (datetime.datetime.now ().strftime ("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush ()


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
            return float (label)
        elif '&' in label:
            return label.split ('&')
        elif '@' in label:
            return label.split ('@')
        else:
            return int (label)
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


if "SF_cookie" in os.environ:
    SF_cookie = os.environ["SF_cookie"]
    if "&" in SF_cookie:
        cookies = SF_cookie.split ('&')
        account = len (cookies)
        printT ("已获取并使用Env环境cookies")
    else:
        printT ("已获取并使用Env环境cookie")
else:
    print ("检查变量SF_cookie是否已填写")

if "lottery_black_list" in os.environ:
    lottery_black_list = os.environ["lottery_black_list"]
    if "@" in lottery_black_list:
        lottery_black_list = lottery_black_list.split ('@')
        printT ("已获取并使用Env环境lottery_black_list")
else:
    print ("检查变量lottery_black_list未填写，默认中奖列表通知不过滤，全发送")


## 获取通知服务
class msg (object):
    def __init__(self, m=''):
        self.str_msg = m
        self.message ()

    def message(self):
        global msg_info
        printT (self.str_msg)
        try:
            msg_info = "{}\n{}".format (msg_info, self.str_msg)
        except:
            msg_info = "{}".format (self.str_msg)
        sys.stdout.flush ()  # 这代码的作用就是刷新缓冲区。
        # 当我们打印一些字符时，并不是调用print函数后就立即打印的。一般会先将字符送到缓冲区，然后再打印。
        # 这就存在一个问题，如果你想等时间间隔的打印一些字符，但由于缓冲区没满，不会打印。就需要采取一些手段。如每次打印后强行刷新缓冲区。

    def getsendNotify(self, a=0):
        if a == 0:
            a += 1
        try:
            url = 'https://gitee.com/curtinlv/Public/raw/master/sendNotify.py'
            response = requests.get (url)
            if 'curtinlv' in response.text:
                with open ('sendNotify.py', "w+", encoding="utf-8") as f:
                    f.write (response.text)
            else:
                if a < 5:
                    a += 1
                    return self.getsendNotify (a)
                else:
                    pass
        except:
            if a < 5:
                a += 1
                return self.getsendNotify (a)
            else:
                pass

    def main(self):
        global send
        cur_path = os.path.abspath (os.path.dirname (__file__))
        sys.path.append (cur_path)
        if os.path.exists (cur_path + "/sendNotify.py"):
            try:
                from sendNotify import send
            except:
                self.getsendNotify ()
                try:
                    from sendNotify import send
                except:
                    printT ("加载通知服务失败~")
        else:
            self.getsendNotify ()
            try:
                from sendNotify import send
            except:
                printT ("加载通知服务失败~")
        ###################


msg ().main ()

# 查询奖品
def lottery_list(SF_cookie,acccount):
    b = 0
    url = f'https://mcs-mimp-web.sf-express.com/mcs-mimp/lottery/awardedList'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie": f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-Hans;q=0.9",
        "accept": "application/json, text/plain, */*",
        "Host": "mcs-mimp-web.sf-express.com",
        "content-type": "application/json;charset=utf-8",
    }
    data = '{"productType":"","pageSize":20,"pageNo":1}'
    response = requests.post (url=url, headers=hearders, verify=False, data=data)
    result = response.json ()
    success = result['success']
    if success == True:
        list = result['obj']
        for i in range (len (list)):
            listTip = list[i]['listTip']
            if listTip in lottery_black_list:
                b = 1
            else:
                msg ("【账号{0}】抽奖奖品为：【{1}】".format (acccount, listTip))
        if b == 1:
            msg("【账号{0}】无黑名单意外的奖品，不通知".format(acccount))

if __name__ == '__main__':
    global msg_info
    print ("============脚本只支持青龙新版=============\n")
    print ("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print ("============顺丰速运APP抽奖奖品通知脚本==============")
    a = 1
    if cookies != '':
        for SF_cookie in cookies:
            while True:
                if a <= account:
                    lottery_list (SF_cookie,a)
                    a += 1
                else:
                    break
    elif SF_cookie != '':
        lottery_list (SF_cookie,a)

    if '奖品为' in msg_info:
        send ("顺丰速运抽奖奖品", msg_info)