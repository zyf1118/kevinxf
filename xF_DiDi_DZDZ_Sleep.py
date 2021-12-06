#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_DZDZ_Sign.py
Author: 一风一燕
功能：滴滴app多走多赚签到
Date: 2021-11-23
cron: 1 6,22 * * * xF_DiDi_DZDZ_Sign.py
new Env('滴滴app多走多赚签到');



****************滴滴出行APP*******************


【教程】：需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token，用&隔开，例如Didi_jifen_token="xxxxx&xxxx"

手机抓包后，手动点击多看多赚，签到一次后，查看URL，https://res.xiaojukeji.com/sigma/api/step/sign/v2?wsgsig=
再查看表头，tiket就是需要抓的变量了

在青龙变量中添加变量Didi_jifen_token="xxxx",xxx就是上面抓的ticker复制下来就OK了


cron时间填写：1 6,22 * * *


'''


Didi_jifen_token = ''



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
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()


pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"


nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
today = datetime.datetime.now().strftime('%Y-%m-%d')
mor_time = '07:00:00.00000000'
after_time = '23:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)
sleeptime = '{} {}'.format (today, after_time)







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
    if len (os.environ["Didi_jifen_token"]) > 419:
        tokens = os.environ["Didi_jifen_token"]
        # tokens = tokens.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境Didi_jifen_token")
    else:
        Didi_jifen_token = os.environ["Didi_jifen_token"]
else:
    print("检查变量Didi_jifen_token是否已填写")



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
        res = response.headers['Location']                                  #获取响应请求头
        # print(res)
        r = re.compile (r'root_xpsid=(.*?)&appid', re.M | re.S | re.I)
        xpsid = r.findall (res)
        xpsid = xpsid[0]
        print(xpsid)
        return xpsid
    except Exception as e:
        print(e)
        msg("获取xpsid失败，可能是表达式错误")

#睡觉
def sleep(Didi_jifen_token,xpsid,account,wsgsig):
    try:
        url = f'https://res.xiaojukeji.com/sigma/api/sleep/sleep/v2?wsgsig={wsgsig}'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Host": "res.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "ticket":f"{Didi_jifen_token}",
            "Content-Type":"application/json",
        }
        data = r'{"xbiz":"240300","prod_key":"ut-walk-bonus","xpsid":"1265f6d94e3e48f686f1be0245c27fd2","dchn":"aXxR1oB","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"1265f6d94e3e48f686f1be0245c27fd2","xpsid_from":"","xpsid_share":"","version":1,"source_from":"app","ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","env":{"ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","cityId":"21","longitude":113.81250027126737,"latitude":23.016204427083334,"newAppid":10000,"isHitButton":true,"ddfp":"99d8f16bacaef4eef6c151bcdfa095f0","deviceId":"99d8f16bacaef4eef6c151bcdfa095f0","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"city_id":"21"}'
        # print(data)
        response = requests.post (url=url, headers=heards,verify=False,data=data)
        result = response.json()
        print (result)
        errmsg = result['errmsg']
        if "睡觉状态错误" in errmsg:
            msg("【账号{0}】睡觉状态错误".format(account))
        elif errmsg == 'success':
            msg("【账号{0}】已执行睡觉命令".format(account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】执行睡觉命令失败,可能是ticket过期".format (account))

#睡醒
def wakeup(Didi_jifen_token,xpsid,account,wsgsig):
    try:
        url = f'https://res.xiaojukeji.com/sigma/api/sleep/wake/v2?wsgsig={wsgsig}'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Host": "res.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "ticket":f"{Didi_jifen_token}",
            "Content-Type":"application/json",
        }
        data = r'{"xbiz":"240300","prod_key":"ut-walk-bonus","xpsid":"46c633fd0c98480e858b4a0a414ef717","dchn":"aXxR1oB","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"281474990465673","xenv":"passenger","xspm_from":"","xpsid_root":"46c633fd0c98480e858b4a0a414ef717","xpsid_from":"","xpsid_share":"","version":1,"source_from":"app","ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","env":{"ticket":"Ag8aVeRbZ1yee4AsBI69GkodAzZQRoQqykuols0cKZEkzDluAzEMQNG7_JoYkKJESWzT5w5ZJkujADFcDXx3Y-z-4R0sJfFNN0VYRpqwCmmqqsJy0nqbJbxajDJdWJW0qK16jNaF1UheXhHeSBDeyTKs9jqn1mjRXfgkp7CTB5e_6__HTupN-Dor7xH6qL5JzNvQMaJrIPw8y9-T3wMAAP__","cityId":"21","longitude":113.81259847005208,"latitude":23.01628173828125,"newAppid":10000,"isHitButton":true,"ddfp":"99d8f16bacaef4eef6c151bcdfa095f0","deviceId":"99d8f16bacaef4eef6c151bcdfa095f0","appVersion":"6.2.4","userAgent":"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0","fromChannel":"1"},"city_id":"21"}'
        # print(data)
        response = requests.post (url=url, headers=heards,verify=False,data=data)
        result = response.json()
        print (result)
        errmsg = result['errmsg']
        if "起床状态错误" in errmsg:
            msg("【账号{0}】当前在睡醒状态,无法领取健康豆".format(account))
        elif errmsg == 'success':
            message_text = result['data']['message_text']
            if "只有多多休息" in message_text:
                msg ("【账号{0}】当前在睡醒状态,无法领取健康豆".format (account))
            else:
                bonus_amount = result['data']['bonus_amount']
                msg("【账号{0}】已执行睡醒命令,获取{1}健康豆".format(account,bonus_amount))

    except Exception as e:
        print (e)
        msg ("【账号{0}】执行睡醒命令失败,可能是ticket过期".format (account))


if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行滴滴多走多赚睡觉脚本==============")
    print(Didi_jifen_token)

    if Didi_jifen_token != '':
        xpsid = get_xpsid ()
        nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
        if nowtime > moringtime and nowtime < sleeptime:
            sleep (Didi_jifen_token,xpsid,account,wsgsig)
        else:
            wakeup (Didi_jifen_token, xpsid, account,wsgsig)
    elif tokens == '' :
        print("检查变量Didi_jifen_token是否已填写")
    elif len(tokens) > 1 :
        account = 1
        for i in tokens:             #同时遍历两个list，需要用ZIP打包
            xpsid = get_xpsid ()
            nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
            if nowtime > moringtime and nowtime < sleeptime:
                sleep (i,xpsid,account,wsgsig)
            else:
                wakeup (i, xpsid, account,wsgsig)
            account += 1

    if "命令" in msg_info:
        send("滴滴多走多赚睡觉", msg_info)
    elif "过期" in msg_info:
        send("滴滴多走多赚睡觉", msg_info)
    elif "状态" in msg_info:
        send ("滴滴多走多赚睡觉", msg_info)