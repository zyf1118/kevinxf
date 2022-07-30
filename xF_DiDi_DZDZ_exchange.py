#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_DZDZ_exchange.py
Author: 一风一燕
功能：滴滴app多走多赚签到
Date: 2021-12-19
cron: 1 0 0 * * * xF_DiDi_DZDZ_exchange.py
new Env('滴滴app多走多赚兑换福利金');

2022-1-7 updata:兑换改版，更新脚本

2022-7-30 updata:兑换改版，更新脚本。改兑换需要签到好几天才能进。


****************滴滴出行APP*******************


【教程】：

需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token，用&隔开，例如Didi_jifen_token="xxxxx&xxxx"

手机抓包后，手动点击多看多赚，签到一次后，查看URL，https://res.xiaojukeji.com/sigma/api/step/sign/v2?wsgsig=
再查看表头，ticket就是需要抓的变量了

在青龙变量中添加变量Didi_jifen_token="xxxx",xxx就是上面抓的ticker复制下来就OK了


接下来说一下怎么抓FLJ_exchange_data
如果多个账号，用@或者回车隔开，export FLJ_exchange_data'xxx@xxx'
进入多走多赚，然后点击左上角兑换，兑换一次1福利金，查看https://res.xiaojukeji.com/sigma/api/coin/exchange?wsgsig=
body或者文本，整个复制即可。
如果想兑换50福利金，就将最后的extra_number":4，数字4改为2。

注意：查看福利金对应的数字id，查看https://res.xiaojukeji.com/sigma/api/coin/getCommodityInfo?
响应体中的json数据，id就是对应的extra_number


cron时间填写：1 0 0 * * *


'''


Didi_jifen_token = ''

FLJ_exchange_data = ''

'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens = ''
account = 1

try:
    import requests
    import json,sys,os,re
    import time,datetime
    from urllib.parse import quote, unquote
    import threading
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"
today = datetime.datetime.now().strftime('%Y-%m-%d')
tomorrow=(datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')

#开始抢兑时间
starttime='00:00:03.00000000'
#结束时间
endtime='00:00:30.00000000'

qgtime = '{} {}'.format (tomorrow, starttime)
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
#    ck = f.read()
#    tokens = ck
#    if "Didi_jifen_token" in ck:
#        r = re.compile (r'Didi_jifen_token="(.*?)"', re.M | re.S | re.I)
#        tokens = r.findall(ck)
#        tokens = tokens[0].split ('&')
#        if len (tokens) == 1:
#            Didi_jifen_token = tokens[0]
#            tokens = ''
#            # print(tokens)
#            # tokens = cookies[3]
#        else:
#            pass
#    printT ("已获取并使用ck环境 token")

########################################################################

if "Didi_jifen_token" in os.environ:
    if len (os.environ["Didi_jifen_token"]) > 319:
        tokens = os.environ["Didi_jifen_token"]
        tokens = tokens.split ('&')
        # tokens = tokens.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境Didi_jifen_tokens")
    else:
        Didi_jifen_token = os.environ["Didi_jifen_token"]
else:
    print("检查变量Didi_jifen_token是否已填写")

if "FLJ_exchange_data" in os.environ:
    if "@" in os.environ["FLJ_exchange_data"]:
        FLJ_exchange_datas = os.environ["FLJ_exchange_data"]
        FLJ_exchange_datas = FLJ_exchange_datas.split("@")
        print(FLJ_exchange_datas)
        printT ("已获取并使用Env环境FLJ_exchange_datas")
    elif "\n" in os.environ["FLJ_exchange_data"]:
        FLJ_exchange_datas = os.environ["FLJ_exchange_data"]
        FLJ_exchange_datas = FLJ_exchange_datas.split("\n")
        print(FLJ_exchange_datas)
        printT ("已获取并使用Env环境FLJ_exchange_datas")
    else:
        FLJ_exchange_data = os.environ["FLJ_exchange_data"]
        printT (f"已获取并使用Env环境FLJ_exchange_data")
else:
    print("变量FLJ_exchange_data未填写")

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


#获取xpsid
def get_xpsid():
    try:
        url = f'https://v.didi.cn/p/DpzAd35?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812538&maptype=soso&os=iOS&utc_offset=480&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016271&origin_id=1&client_type=1&terminal_id=1&sig=8503d986c0349e40ea10ff360f75d208c78c989a'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head (url=url, headers=heards, verify=False)    #获取响应请求头
        result = response.headers['Location']                                  #获取响应请求头
        # print(result)
        # r = re.compile (r'root_xpsid=(.*?)&channel_id')
        r = re.compile (r'root_xpsid=(.*?)&xspm_from=&xenv')
        xpsid = r.findall (result)
        xpsid = xpsid[0]
        print(xpsid)
        return xpsid
    except Exception as e:
        print(e)
        msg("获取xpsid失败，可能是表达式错误")

#查看兑换商品
def get_info(Didi_jifen_token,xpsid,account):
    url = r'https://res.xiaojukeji.com/sigma/api/coin/getCommodityInfo?wsgsig=dd03-hqkZU%2B6uB7Cr8A0PptE2YKwpcysW4VJionZLSuFOcysX7ryuwc92YKLZCNCX79n%2FOgxev49rDp%2BUHFvSSGxLS4FSD77W7AuVYcO3Z4wxCo%2BjJADPSGrJYyFOf7L'
    heards = {
        "Host": "res.xiaojukeji.com",
        "Accept":"application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://page.udache.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":"keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "ticket":f"{Didi_jifen_token}",
        "User-Agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://page.udache.com/",
        # "Content-Length": "1013"
    }
    data = r'{"xbiz":"","prod_key":"ut-walk-bonus","xpsid":"","dchn":"aXxR1oB","xoid":"6b4a2e3b-2f92-4531-a37a-8207703537c0","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + '","xpsid_from":"' + f"{xpsid}" + '","xpsid_share":"","version":1,"source_from":"app","type":0,"page":1,"page_size":12,"city_id":"21"}'
    response = requests.post (url=url, headers=heards, verify=False, data=data)
    result = response.json ()



#兑换福利金
def exchange(Didi_jifen_token,xpsid,account,data):
    flag = 0
    url = r'https://res.xiaojukeji.com/sigma/api/coin/exchange?wsgsig=dd03-Aw6B%2FgNq%2B4AVxniq68arSjgl6vqsZbvs8R9kYsfi6vqtwf%2BQM%2BZrSc8tLKAtwXGq2KdTpD4tLRHlSCjm8pPVYtcVL4Lqw03ZHp2tTGKWN7MiwCNZ7z6rTGKVLy9q'
    heards = {
        "Host": "res.xiaojukeji.com",
        "Accept":"application/json, text/plain, */*",
        "Content-Type": "application/json",
        "Origin": "https://page.udache.com",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection":"keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "ticket":f"{Didi_jifen_token}",
        "User-Agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        "Referer": "https://page.udache.com/",
        # "Content-Length": "1013"
    }
    printT("抢兑换开始时间为：{}".format (qgtime))
    printT (f"正在等待兑换时间，请勿终止退出...")
    try:
        while True:
            nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
            if nowtime < qgtime:
                    response = requests.post (url=url, headers=heards,verify=False,data=data)
                    # print(response.text)
                    result = response.json()
                    print(result)
                    errmsg = result['errmsg']
                    if errmsg == 'success':
                        msg("【账号{0}】福利金兑换成功".format(account))
                        flag = 1
                        break
                    elif "代币兑换错误" in errmsg:
                        print("【账号{0}】今日兑换福利金可能已达上限".format(account))
                        if flag == 1:
                            break
            if nowtime > qgendtime:
                msg ("【账号{0}】福利金兑换失败".format (account))
                break

    except Exception as e:
        print (e)


if __name__ == '__main__':
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n")
    print("============执行滴滴多走多赚兑换脚本==============")
    # print(Didi_jifen_token)
    if Didi_jifen_token != '':
        xpsid = get_xpsid ()
        get_info (Didi_jifen_token, xpsid, account)
        exchange (Didi_jifen_token, xpsid, account, FLJ_exchange_data)
    elif tokens == '' :
        print("检查变量Didi_jifen_token是否已填写")
    elif len(tokens) > 1 :
        account = 1
        ttt = []
        for i,j in zip(tokens,FLJ_exchange_datas):             #同时遍历两个list，需要用ZIP打包
            xpsid = get_xpsid ()
            thread = threading.Thread(target=exchange, args=(i, xpsid, account, j))
            ttt.append (thread)
            thread.start ()
            account += 1
        for thread in ttt:
            thread.join ()
    if "已兑换" in msg_info:
        send("滴滴多走多赚兑换", msg_info)
    elif "过期" in msg_info:
        send("滴滴多走多赚兑换", msg_info)
