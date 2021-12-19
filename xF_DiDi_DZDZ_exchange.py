#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_DZDZ_exchange.py
Author: 一风一燕
功能：滴滴app多走多赚签到
Date: 2021-12-19
cron: 9 15 * * * xF_DiDi_DZDZ_exchange.py
new Env('滴滴app多走多赚兑换福利金');



****************滴滴出行APP*******************


【教程】：

青龙变量exchange_jkd_numb=5的话，兑换5*1000健康豆=50福利金。建议填写6或者7，每天上限7次，按需填写。

需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token，用&隔开，例如Didi_jifen_token="xxxxx&xxxx"

手机抓包后，手动点击多看多赚，签到一次后，查看URL，https://res.xiaojukeji.com/sigma/api/step/sign/v2?wsgsig=
再查看表头，ticket就是需要抓的变量了

在青龙变量中添加变量Didi_jifen_token="xxxx",xxx就是上面抓的ticker复制下来就OK了



cron时间填写：9 15 * * *


'''


Didi_jifen_token = ''
exchange_numb = 1000
exchange_jkd_numb = 1


'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens =''
account = 1
id = ''
try:
    import requests
    import json,sys,os,re
    import time,datetime
    from urllib.parse import quote, unquote
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
    print(len (os.environ["Didi_jifen_token"]))
    if len (os.environ["Didi_jifen_token"]) > 319:
        tokens = os.environ["Didi_jifen_token"]
        # tokens = tokens.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境Didi_jifen_token")
    else:
        Didi_jifen_token = os.environ["Didi_jifen_token"]
else:
    print("检查变量Didi_jifen_token是否已填写")

if "exchange_jkd_numb" in os.environ:
    exchange_jkd_numb = os.environ["exchange_jkd_numb"]
    total_exchange = int(exchange_jkd_numb) * 1000
    printT (f"已获取并使用Env环境exchange_jkd_nnumb，兑换{total_exchange}健康豆")
else:
    print("变量exchange_jkd_numb未填写，默认兑换1000健康豆")

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
    # if "Didi_jifen_token" in tokens:
        # r = re.compile (r'Didi_jifen_token="(.*?)"', re.M | re.S | re.I)
        # tokens = r.findall (ck)
        tokens = tokens.split ('&')
        # print(tokens)
        if len (tokens) == 1:
            Didi_jifen_token = tokens[0]

        else:
            pass

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
        r = re.compile (r'root_xpsid=(.*?)&appid', re.M | re.S | re.I)
        xpsid = r.findall (result)
        xpsid = xpsid[0]
        print(xpsid)
        return xpsid
    except Exception as e:
        print(e)
        msg("获取xpsid失败，可能是表达式错误")


#兑换福利金
def exchange(Didi_jifen_token,xpsid,account,exchange_jkd_numb):
    try:
        exchange_jkd_numb = int(exchange_jkd_numb)
        for i in range(exchange_jkd_numb):
            url = f'https://res.xiaojukeji.com/sigma/api/coin/exchange?wsgsig=dd03-ct%2F4IjT46lMZCt2NNqSuenkN%2BeTy0m9eLkxoBGlI%2BeTzCiU679dvenw17VMzCDTgJdZnfXY17eZPbW1BLlSzeXH88F9TftTf%2BAEvBXZK7e5TAfZN%2BqExBCq78lIY'
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
                "Content-Length": "1013"
            }
            data = r'{"xbiz":"240300","prod_key":"","xpsid":"36f75fd5df6841c2abc13be6ec0a218e","dchn":"DpzAd35","xoid":"f24bac22-d420-493f-ad13-d2749d24c1e2","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"36f75fd5df6841c2abc13be6ec0a218e","xpsid_from":"89367ca938ca4febad1bb272af4984ce","xpsid_share":"","version":1,"source_from":"app","city_id":21,"env":{"ticket":"dvJhibvsyKKWyG_lwfJoVucFLai8HOkVogb-A8aYfpIkzDmKA0EMQNG7_Fg0Ui1SldLJ5w6z9CxJGWwcNb67aZw_3sFSkrrppgjLSBNWIU1VVViVtOizeG3mo8wqrEaat3ALHyGsTvL2jvBBgvBJlmEt2pzavHtU4Zucwk4e3C7369dO6kP4Oas6x5mH8EtitQ8dw0Md4e9V_p_8GQAA__8=","cityId":"21","longitude":113.81221218532986,"latitude":23.016388346354166,"newAppid":10000,"isHitButton":true,"ddfp":"99d8f16bacaef4eef6c151bcdfa095f0","deviceId":"99d8f16bacaef4eef6c151bcdfa095f0","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"type":4,"extra_number":1000}'
            # print(data)
            response = requests.post (url=url, headers=heards,verify=False,data=data)
            res = response.text
            # print(res)
            result = response.json()
            print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                msg("【账号{0}】已兑换{1}健康豆，获得福利金{2}".format(account,exchange_numb,int(exchange_numb)/100))
                time.sleep(2)
            elif "代币兑换错误" in errmsg:
                msg("【账号{0}】今日兑换可能已达上限")
                break
    except Exception as e:
        print (e)
        msg ("【账号{0}】兑换福利金失败,可能是ticket过期".format (account))


if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行滴滴多走多赚兑换脚本==============")
    print(Didi_jifen_token)
    if Didi_jifen_token != '':
        xpsid = get_xpsid ()
        exchange (Didi_jifen_token, xpsid, account, exchange_jkd_numb)

    elif tokens == '' :
        print("检查变量Didi_jifen_token是否已填写")
    elif len(tokens) > 1 :
        account = 1
        for i in tokens:             #同时遍历两个list，需要用ZIP打包
            xpsid = get_xpsid ()
            exchange (i, xpsid, account, exchange_jkd_numb)
            account += 1


    if "签到" in msg_info:
        send("滴滴多走多赚兑换", msg_info)
    elif "过期" in msg_info:
        send("滴滴多走多赚兑换", msg_info)