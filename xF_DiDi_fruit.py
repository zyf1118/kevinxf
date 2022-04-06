#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_fruit.py
Author: 一风一燕
功能：滴滴app水果自动任务
Date: 2021-11-23
cron: 43 0-3,8,9,12,15,18,22 * * * xF_DiDi_fruit.py
new Env('滴滴app水果自动任务');



****************滴滴出行APP*******************



【教程】：方法一：
需要自行用手机抓取Didi_jifen_token。
Didi_jifen_token如何抓，请看didi_Sign说明

方法二：
手机抓包后，自己浇水一次，查看URL路径，https://game.xiaojukeji.com/api/game/plant/watering?wsgsig=xxxx
然后查看headers，D-Header-T对应的数值，就是token


在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token，用&隔开，例如Didi_jifen_token=xxxxx&xxxx

cron时间填写：43 0-3,8,12,15,18,22 * * *


'''

Didi_jifen_token = ''

'''


=================================以下代码不懂不要随便乱动=================================


'''
tokens = ''
account = 1
id = ''
try:
    import requests
    import json, sys, os, re
    import time, datetime,random
except Exception as e:
    print (e)

requests.packages.urllib3.disable_warnings ()

pwd = os.path.dirname (os.path.abspath (__file__)) + os.sep
path = pwd + "env.sh"

nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
today = datetime.datetime.now ().strftime ('%Y-%m-%d')
time1 = '08:00:00.00000000'
time2 = '12:00:00.00000000'
time3 = '15:00:00.00000000'
time4 = '17:00:00.00000000'
get_time1 = '{} {}'.format (today, time1)
get_time2 = '{} {}'.format (today, time2)
get_time3 = '{} {}'.format (today, time3)
get_time4 = '{} {}'.format (today, time4)

wsgsig=['dd03-vx9tq2onDp0IZqcYVoABxTjsa%2BXNwlstUQ6fOSmVa%2BX%2BZhfRmNkDw6zkAz0%2BZA8rsJ2%2BzMKjCoJLpecxVoEAOMK%2FBzf2SAJmXo6ax6Nre%2BnNYVNkX72aP6KjAJE',
        'dd03-67TGcdCHNXqCW0FVDMhX%2B%2F%2B650AFtbkyCIqj4r3350AEWfAm9TIW%2B9cKMnqEWXIwEPUQLAXc%2BWT0%2FiFqd1%2Fn%2Be36LslfUXIyD61n%2BAgNL096XnZxBMZUNl%2BN%2BXO',
        'dd03-rxqml47pGugrvrGTzy%2FbOp8ud3nWyknnyQTDxoGxd3nXv%2FDzSNEfP8%2BSFQgXvBJlYJP3Q%2BvlFR3UTdGPxKw9RJGuE3%2BtZa8rPod9xp3uF3KrvEbhPolCP3KkEQ9',
        'dd03-%2FbmamzeJR3QXGQJTThyOOv18ZuJqDzvOpFvUyJM1ZuJrGv%2BqxrbhQvEIOJQrGJGQPVzxPRAHQ3WnfpjwpEQmzRLaPJyXE%2BcyYhyiy763PujiGJiPSrWnRN28xJQV',
        'dd03-UfTkqudHf%2B4nfF8UZV2awyM6Epv%2Fc9oqvBqBO%2BL3Epvhfd3OPVIdwyFKe84hfVcsxrU1zoBJg%2BKXGAWkvAwBxo2KBQgPfebhZqxdwRMHB%2BcjfF%2BtuFhMxReNd3Ct',
        'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
        'dd03-aScF%2FD3Xy4FqxzWqMzcXogciSvVXYQRtNv7%2FYmClSvVWxo8R58nVS0KUxKFWx8frH43PpggVz3HVRJ3x2z8wYgNlxR6yPzfqM%2BNhZg7%2FzKHjx3Nr2z7kTXDVwKE',
        'dd03-CugL8XzfY9YxloS582DSCDiDQ%2F1u%2Fv656T3ZgbXEQ%2F1vlzPd%2BIjSDtoevAYvlNq74M7qAjmev9YTVReH6ScSftv0o%2Fqul7%2F6JP4RCcm9uqLZkvw48SGzfjzAZ9YY',
        'dd03-NEvAAAqxzcF7%2B%2B%2Fqb0pV6dhOTjV2J3xtacmlHlYpTjV1%2B7IRDn8q5EhywDF1%2BpArgjiS8drvwbH42uLxbbRXIkhWyD5M4z1rb0ok6hZWwjl4MpFhcnXVIalvPDH',
        'dd03-DUXVE0SysCEZ%2BS1O7nX62jMR%2FsUyJZPj5jQ9LikS%2FsUz%2Bx6vNgDF1DxxrbEz%2BLdh3coI4cPvqjIw221TJXgA1tVvlnaPM2APJXba1tURrbhPMLBt7ntC1DhYks9',
        'dd03-wDXIwYa7Z54GDovErARRsS5KRwvBGvJAtdQwkMILRwvADzyHh%2FDPqwA6uL4ADNnCVkoVtSd5vMfDe4v7sevTrwh%2Bu5baf4zBrAXPqLEEYICcD7j3kqcRsSA4YL1',
        'dd03-y3uI01tMPCX7nJYRt2No3SQ1vs02i8IprMnw%2BTv8vs01n4xXjP7P45iNQbX1nQkTXTjV1LW%2BRcQ4rzYhq5iP42QgRgRBt8xzsZmQ%2BSj3O0R8t3PzsSs%2F4SWLyCq',
        'dd03-%2Fep12zdOxaJXJ8w9TGpxE42xphQq%2BJMdpCsTaJLuphQrJNZ5xWKYFvFRyBJrJz%2FfPsWkGRapzA0s5QwJTjQSFKAzRhci73VGSjvvFK9zzkgl7%2BYgoDuPaoLzRaL',
        'dd03-z6%2BZsOikr8p3Z5vssNK6z5jrjz%2B6wIJZqJCLQ6QWjz%2B5ZMyhioR2yStns%2Bp5ZwnvWQGexwnmtNs8pPvXsv87yZnnm3n6T2oPtNbMzwtlnJj6vwGPsRbKzwgonJk',
        'dd03-0%2F1PtGPrF8UO5avU3tAazsYkgzEp2EJz1Xe5RjhjgzEo5AynJDwIzCYsG%2BUo5hnx70aFwbSt0NPTJUvr3fHNzgSsb3wpHdop4tF6ybYqcJYp7hGp3GF4ybLvcJw',
        'dd03-rDByxRBD9w%2BsAUn7w966q%2BEfC5pVFhGFydLKl72aC5pUAliMS%2FV7rp9AcS%2BUAEv0YkHbszEBbTCXfan4wVa2ruEA0ZgVdrsex95Jqz9CGPcVCEJewl5LqzU2GPd',
        'dd03-gUaMGbSXHChPMWOhInVo1fTi3saoHj2QHj5YNXkl3sapMnTs3glT3fxUKbhpMGUONc1r2GPqJcwS4cOkKbHv1fMV8sVQLW9Q8nBlNWIUKiYwLWSoIsEz%2BfOhJXq',
        'dd03-ZB27DIBhLttb1gkuUiIX8TLU7DDe6CFyWfdRKw2t7DDd1Ghmkixy8M9i%2Bjtd1nYwqm9i56EmNiogNskqUgESKTBU%2BfiC1glSUnHO8xBr3DbG2ihpUgIW76Um3jq',
        'dd03-20QwPlA2%2FILbbHoaEks8lhBLsPSeg68eG9XIrA1KsPSdb2R6dkN5lha3j2LdbOsgA%2Ft9mrF7i1BgExoK9dzMldHNWIIA9TWN9ao2qkICWL9ebHs%2B0d71khHIiL5',
        'dd03-35eouVsWdxONxlnc0%2BaNWavjG6HIYqGHFK14i9ukG6HHxUiAgphNWrjVgTOHxevJDR5CVhXrfSVKRAnf0QMHUURrg1x6OF%2BcE3H4iaujgYkaOFpcbQA8WrnqgHY',
        'dd03-qRg6qKKGw8DUhpRWx14yy%2BGcozttku3szw3OOycdoztshyoQT1jxw%2B3Fz%2BDsh%2BXqZ57hz8NBzoNrX3RwPYNpxuNERz8tUztXwOsOxQbCzuf%2FV3nWx1sSy%2BJGx%2BE',
        'dd03-zzyKkOo5PQ82t3sQsSuQOLnIvJz7W%2BchqOjyw6mNvJz8tKXZiL3ROSz8Qu88tuojWHnXRwR5QRb5lpspswWSQSJNQJc4tzultPnYx5R3QzKGrzzrswzuw2v8zQd',
        'dd03-XGGZ8J%2FbhAtQdOYFue33BNV0tqDTaxI7YaKLgzOAtqDSdZxfQls2DNrai9tSdHk5yh%2BeA7ldiaopC6YAue4JB7SA%2FAtkf1rLulKLfyqCWVnldOTKul4KgvYC%2F9S',
        'dd03-DOgz5gRWq%2FAYTS%2F26v82Acsji9qzOZBC5z3Jdsjki9qyTxlJN4j8AcuVtqAyTLwA387cDDoXsrMxv2%2F5KKfKAfX%2Fs9HyTIYG8NK0BtnjrV5uZ5LDJvfKAWWUrq5',
        'dd03-kQNDYoKdpT7kl4cdP27UVJJBxMyj%2FNsaRxDm%2F4cGxMyilJf2Z2QtUQ3gSx7ilv8cT60pXuNdSwchtoc%2BPINqUJcETYN%2Fr7DdOSbqU3JgTO%2BqrRJEQP%2B%2FV%2BbfSTd',
        'dd03-RnANOxOD1Z3H9sJdnUHQlIrfJ2u%2Ben09kqMvqH%2FaJ2uN9jj1WEUokZZA4P3N9CubiAIsnPrD4OgMGgmNmd5plZPCN2NIF0zGlUBwqLxCNPNHaitCnE6xlZqa2ZA'
        ]

uid = ''.join(random.sample('01234567890123456789', 15))


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
    print (len (os.environ["Didi_jifen_token"]))
    if len (os.environ["Didi_jifen_token"]) > 319:
        tokens = os.environ["Didi_jifen_token"]
        # tokens = tokens.split ('&')
        # cookies = temporary[0]
        printT ("已获取并使用Env环境Didi_jifen_token")
    else:
        Didi_jifen_token = os.environ["Didi_jifen_token"]
else:
    print ("检查变量Didi_jifen_token是否已填写")


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
nowtime = int (round (time.time () * 1000))




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


# 获取xpsid
def get_xpsid():
    try:
        url = f'https://v.didi.cn/p/DpzAd35?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812538&maptype=soso&os=iOS&utc_offset=480&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016271&origin_id=1&client_type=1&terminal_id=1&sig=8503d986c0349e40ea10ff360f75d208c78c989a'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head (url=url, headers=headers, verify=False)  # 获取响应请求头
        res = response.headers['Location']  # 获取响应请求头
        # print(res)
        r = re.compile (r'root_xpsid=(.*?)&channel_id')
        xpsid = r.findall (res)
        xpsid = xpsid[0]
        print (xpsid)
        return xpsid
    except Exception as e:
        print (e)
        msg ("获取xpsid失败，可能是表达式错误")


# 获取小动物id
def get_pet_id(Didi_jifen_token, xpsid,wsgsig):
    try:
        url = f'https://game.xiaojukeji.com/api/game/plant/enter?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = '{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","assist_type":0,"encode_uid":"","is_old_player":true,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print(result)
        pet_id = result['data']['lam_uid']

        return pet_id
    except Exception as e:
        print (e)
        msg ("获取pet_id失败，可能是token过期")


# 获取任务列表
def get_missons(Didi_jifen_token, xpsid,wsgsig):
    missons_list = []
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/get?xbiz=240301&prod_key=didi-orchard&xpsid={xpsid}&dchn=O9aM923&xoid=aA%2Fiet7vTTmdKCRAgoHwyg&uid=' + f'{uid}' + f'&xenv=passenger&xspm_from=&xpsid_root={xpsid}&xpsid_from=&xpsid_share=&game_id=23&loop=0&platform=1&token={Didi_jifen_token}&wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Accept": "application/json, text/plain, */*",
        }
        response = requests.get (url=url, headers=headers, verify=False)
        result = response.json ()
        # print(result)
        missons = result['data']['missions']
        # print(missons)
        for i in range (len (missons)):
            title = missons[i]['title']
            missons_list.append (title)

        return missons_list
    except Exception as e:
        print (e)
        msg ("获取missoins_list失败，可能是token过期")


# 签到
def do_sign(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/plant/sign?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if "今天已经签过到" in errmsg:
            msg ("【账号{}】今天已经签到，跳出执行签到环节".format (account))
        if errmsg == 'success':
            name = result['data']['rewards'][0]['name']
            num = result['data']['rewards'][0]['num']
            sign_times = result['data']['sign_times']
            msg ("【账号{3}】今天签到成功，获取{0}{1},已连续签到{2}天".format (name, num, sign_times, account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】执行签到失败,可能是token过期".format (account))


# 领取宝箱
def get_treasure(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        for i in range (100):
            id = wsgsig[random.randint (0,25)]
            url = f'https://game.xiaojukeji.com/api/game/plant/recCommonBox?wsgsig={id}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://fine.didialift.com/",
                "Host": "game.xiaojukeji.com",
                "Origin": "https://fine.didialift.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "D-Header-T": f"{Didi_jifen_token}",
                "Content-Type": "application/json",
            }
            data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","is_fast":false,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
            # print(data)
            response = requests.post (url=url, headers=headers, verify=False, data=data)
            result = response.json ()
            # print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                name = result['data']['rewards'][0]['name']
                num = result['data']['rewards'][0]['num']
                i += 1
                msg ("【账号{2}】成功领取第{3}个宝箱奖励,获得{0}{1}".format (name, num, account, i))
                time.sleep (1)
            else:
                break

    except Exception as e:
        print (e)
        msg ("【账号{0}】领取宝箱失败,可能是token过期".format (account))


# 领取任务（固定入口进入游戏）
def get_misson1(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":255,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】固定入口进入游戏任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【固定入口进入游戏】任务失败,可能是token过期".format (account))


# 领取任务（【浏览晒单区】任务）
def get_misson2(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":32,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【浏览晒单区】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浏览晒单区】任务失败,可能是token过期".format (account))


# 领取任务（访问公交车页面任务）
def get_misson3(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":256,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【访问公交车页面任务】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问公交车页面任务】任务失败,可能是token过期".format (account))


# 领取任务（成长会员主页）
def get_misson4(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":258,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【访问公交车页面任务】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问公交车页面任务】任务失败,可能是token过期".format (account))


# 领取任务（积分商城）
def get_misson5(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":257,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【访问公交车页面任务】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问公交车页面任务】任务失败,可能是token过期".format (account))


# 领取任务（学会技能）
def get_misson6(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":31,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【学会技能】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【学会技能】任务失败,可能是token过期".format (account))


# 领取任务（果园入口）
def get_misson7(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":29,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【果园入口】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【果园入口】任务失败,可能是token过期".format (account))


# 领取任务（浇水100g）
def get_misson8(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":250,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))
        elif "任务未达到领奖条件" in errmsg:
            msg("【账号{}】【浇水100g】未达到领奖条件".format(account))
        else:
            msg ("【账号{}】【浇水100g】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浇水100g】任务失败,可能是token过期".format (account))


# 领取任务（肥料200g）
def get_misson9(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":100,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}袋".format (title, name, count, account))
        elif "任务未达到领奖条件" in errmsg:
            msg("【账号{}】【浇水200g】未达到领奖条件".format(account))
        else:
            msg ("【账号{}】【浇水200g】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浇水200g】任务失败,可能是token过期".format (account))


# 领取任务（肥料500g）
def get_misson10(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":101,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}袋".format (title, name, count, account))
        elif "任务未达到领奖条件" in errmsg:
            msg("【账号{}】【浇水500g】未达到领奖条件".format(account))
        else:
            msg ("【账号{}】【浇水500g】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浇水500g】任务失败,可能是token过期".format (account))


# 领取任务（去除蚂蚱）
def get_misson11(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":15,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【去除蚂蚱】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【去除蚂蚱】任务失败,可能是token过期".format (account))


# 领取7点41分后的水滴
def get_misson12(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/plant/recExtWater?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            rec_water = result['data']['rec_water']
            msg ("【账号{1}】成功领取每日水滴，获取{0}g水滴".format (rec_water, account))

        else:
            msg ("【账号{}】【每日水滴】早已领取，跳过领取环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】领取【每日水滴】失败,可能是token过期".format (account))


# 领取集水
def get_misson13(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/plant/recBucketWater?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            rec_water = result['data']['rec_water']
            msg ("【账号{1}】成功领取集水滴，获取{0}g水滴".format (rec_water, account))

        else:
            msg ("【账号{}】水滴不足1g，跳过领取集水滴环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】领集水滴失败,可能是token过期".format (account))


# 领取肥料
def get_misson14(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/plant/receivePer?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()


    except Exception as e:
        print (e)
        msg ("【账号{0}】领取肥料失败,可能是token过期".format (account))


# 领取饭点水滴8-10,12-14，15-17
def get_misson15(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        if nowtime > get_time1 and nowtime < get_time2:
            fdsd_id = 251
        elif nowtime > get_time2 and nowtime < get_time3:
            fdsd_id = 252
        elif nowtime > get_time3 and nowtime < get_time4:
            fdsd_id = 253
        else:
            return 0
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":' + f"{fdsd_id}" + r',"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】领取{0}，获得{1}{2}g".format (title, name, count, account))
        else:
            msg ("【账号{}】未到时间领取【饭点水滴】，跳过执行环节".format (account))
    except Exception as e:
        print (e)
        msg ("【账号{0}】领取饭点水滴失败,可能是token过期".format (account))

# 领取任务（浏览滴水贷首页6秒）
def get_misson16(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://act.xiaojukeji.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://act.xiaojukeji.com/",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":42,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【浏览滴水贷首页6秒】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浏览滴水贷首页6秒】任务失败,可能是token过期".format (account))

# 领取任务（浏览果园商城15秒）
def get_misson17(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://act.xiaojukeji.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://act.xiaojukeji.com/",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":46,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【浏览果园商城15秒】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浏览果园商城15秒】任务失败,可能是token过期".format (account))

# 领取任务（浏览充值中心）
def get_misson18(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://act.xiaojukeji.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://act.xiaojukeji.com/",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":41,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【浏览充值中心】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【浏览充值中心】任务失败,可能是token过期".format (account))

# 领取任务（访问消消赚）
def get_misson19(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        url = f'https://game.xiaojukeji.com/api/game/mission/award?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://act.xiaojukeji.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://act.xiaojukeji.com/",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":261,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            title = result['data']['title']
            name = result['data']['reward'][0]['name']
            count = result['data']['reward'][0]['count']
            msg ("【账号{3}】完成{0}任务，获取{1}{2}g水滴".format (title, name, count, account))

        else:
            msg ("【账号{}】【访问消消赚】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问消消赚】领取奖励失败,可能是token过期".format (account))

# 固定入口进入游戏
def do_misson1(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":255,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【固定入口进入游戏】任务已完成".format (account))
        else:
            msg ("【账号{}】【固定入口进入游戏】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【固定入口进入游戏】任务失败,可能是token过期".format (account))


# 【浏览晒单区】任务
def do_misson2(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":32,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【【浏览晒单区】任务】任务已完成".format (account))
        else:
            msg ("【账号{}】【【浏览晒单区】任务】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【【浏览晒单区】任务】任务失败,可能是token过期".format (account))


# 访问公交车页面任务
def do_misson3(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":256,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【访问公交车页面】任务已完成".format (account))
        else:
            msg ("【账号{}】【访问公交车页面】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问公交车页面】任务失败,可能是token过期".format (account))


# 访问成长会员任务
def do_misson4(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":258,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【访问成长会员】任务已完成".format (account))
        else:
            msg ("【账号{}】【访问成长会员】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问成长会员】任务失败,可能是token过期".format (account))


# 访问积分商城任务
def do_misson5(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":257,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【访问积分商城】任务已完成".format (account))
        else:
            msg ("【账号{}】【访问积分商城】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【访问积分商城】任务失败,可能是token过期".format (account))


# 学会技能任务
def do_misson6(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":31,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        # print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【学会技能】任务已完成".format (account))
        else:
            msg ("【账号{}】【学会技能】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【学会技能】任务失败,可能是token过期".format (account))


# 点击果园任务
def do_misson7(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":29,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            msg ("【账号{}】【点击果园任务】任务已完成".format (account))
        elif "服务内部错误" in errmsg:
            msg ("【账号{}】【点击果园任务】任务执行失败".format (account))
        else:
            msg ("【账号{}】【点击果园任务】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【点击果园任务】任务失败,可能是token过期".format (account))


# 去除蚂蚱任务
def do_misson8(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        for i in range (2):
            id = wsgsig[random.randint (0,25)]
            nowtime = int (round (time.time () * 1000))
            url = f'https://game.xiaojukeji.com/api/game/plant/killWorm?wsgsig={id}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://fine.didialift.com/",
                "Host": "game.xiaojukeji.com",
                "Origin": "https://fine.didialift.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "D-Header-T": f"{Didi_jifen_token}",
                "Content-Type": "application/json",
            }
            data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","friend_id":null,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
            response = requests.post (url=url, headers=headers, verify=False, data=data)
            result = response.json ()
            print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                worm_num = result['data']['worm_num']
                if worm_num == 0:
                    msg ("【账号{}】【去除蚂蚱】任务已完成".format (account))
            elif "服务内部错误" in errmsg:
                msg ("【账号{}】【去除蚂蚱】任务执行失败".format (account))
            else:
                msg ("【账号{}】【去除蚂蚱】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{}】【去除蚂蚱】任务早已完成，跳过执行环节".format (account))


# 早起分享
def do_misson9(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        wsgsig = wsgsig[random.randint (0,25)]

        url = f'https://game.xiaojukeji.com/api/game/plant/shareEarlyBird?wsgsig={wsgsig}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://fine.didialift.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://fine.didialift.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        time.sleep (0.2)
        if errmsg == 'success':
            url = f'https://game.xiaojukeji.com/api/game/plant/recEarlyBird?wsgsig={wsgsig}'
            data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","is_fast":false,"water_status":0,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
            response = requests.post (url=url, headers=headers, verify=False, data=data)
            result = response.json ()
            print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                msg("【账号{}】【早起分享】任务执行成功，获得100g水滴".format(account))
            elif "对应奖励已领取" in errmsg:
                msg ("【账号{}】【早起分享】早已完成，跳过执行环节".format (account))
            elif "请稍后再试" in errmsg:
                msg ("【账号{}】【早起分享】异常，请重新执行".format (account))
            elif "当前条件还不满足" in errmsg:
                msg("【账号{}】【早起分享】异常，请在中午12点前执行一次脚本".format(account))
        elif "今天已经分享" in errmsg:
            msg ("【账号{}】【早起分享】早已完成，跳过执行环节".format (account))
        else:
            msg("【账号{}】请在中午12点前查看手机APP上时候有早起鸟分享活动".format(account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】【分享任务】任务失败,可能是token过期".format (account))


# 使用肥料
def do_misson10(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        for i in range (100):
            id = wsgsig[random.randint (0,25)]
            nowtime = int (round (time.time () * 1000))
            url = f'https://game.xiaojukeji.com/api/game/plant/fertilizer?wsgsig={id}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://fine.didialift.com/",
                "Host": "game.xiaojukeji.com",
                "Origin": "https://fine.didialift.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "D-Header-T": f"{Didi_jifen_token}",
                "Content-Type": "application/json",
            }
            data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","count":1,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
            response = requests.post (url=url, headers=headers, verify=False, data=data)
            result = response.json ()
            print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                tree_nutrient = result['data']['tree_nutrient']  # 当前肥力
                pack_fer = result['data']['pack_fer']
                if tree_nutrient > 90:
                    msg ("【账号{0}】当前果树肥力{1}，非常旺盛，无需使用肥料，剩余肥料{2}袋".format (account, tree_nutrient, pack_fer))
                    break
                if pack_fer == 0:
                    msg ("【账号{0}】当前果树肥力{1}，肥料不足1袋，无法使用。".format (account, tree_nutrient))
                    break
                msg ("【账号{0}】使用肥料{1}次,当前果树肥力{2}，剩余肥料{3}袋".format (account, i + 1, tree_nutrient, pack_fer))
            elif "服务内部错误" in errmsg:
                msg ("【账号{}】【使用肥料】执行失败".format (account))
                break
            else:
                msg ("【账号{}】【使用肥料】数量不足，无法使用".format (account))
                break
            time.sleep (5)
    except Exception as e:
        print (e)
        msg ("【账号{0}】【使用肥料】任务失败,可能是token过期".format (account))

# 浏览滴水贷首页6秒
def do_misson11(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        id = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/accept?wsgsig={id}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://act.xiaojukeji.com/",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://act.xiaojukeji.com/",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json;charset=utf-8",
            "Accept":"application/json, text/plain, */*",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":42,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            errno = result['errno']
            if errno == 0:
                time.sleep(8)
                msg ("【账号{}】【浏览滴水贷首页6秒】任务已完成".format (account))
        elif "服务内部错误" in errmsg:
            msg ("【账号{}】【浏览滴水贷首页6秒】任务执行失败".format (account))
        else:
            msg ("【账号{}】【浏览滴水贷首页6秒】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{}】【浏览滴水贷首页6秒】任务早已完成，跳过执行环节".format (account))

# 浏览果园商城15秒
def do_misson12(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        id = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={id}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json;charset=utf-8",
        }
        data = r'{"xbiz":"","prod_key":"","xpsid":"","dchn":"","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"didi-orchard.none.none.none","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"' + f'{xpsid}' + r'","xpsid_share":"","source_id":"z10000","partition_id":"1002","token":"' + f'{Didi_jifen_token}' + r'","mission_id":46,"game_id":23,"platform":1}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            errno = result['errno']
            if errno == 0:
                time.sleep(18)
                msg ("【账号{}】【浏览果园商城15秒】任务已完成".format (account))
        elif "服务内部错误" in errmsg:
            msg ("【账号{}】【浏览果园商城15秒】任务执行失败".format (account))
        else:
            msg ("【账号{}】【浏览果园商城15秒】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{}】【浏览果园商城15秒】任务早已完成，跳过执行环节".format (account))

# 浏览充值中心
def do_misson13(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        id = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={id}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json;charset=utf-8",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":41,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            errno = result['errno']
            if errno == 0:
                msg ("【账号{}】【浏览充值中心】任务已完成".format (account))
        elif "服务内部错误" in errmsg:
            msg ("【账号{}】【浏览充值中心】任务执行失败".format (account))
        else:
            msg ("【账号{}】【浏览充值中心】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{}】【浏览充值中心】任务早已完成，跳过执行环节".format (account))

# 访问消消赚
def do_misson14(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        id = wsgsig[random.randint (0,25)]
        nowtime = int (round (time.time () * 1000))
        url = f'https://game.xiaojukeji.com/api/game/mission/update?wsgsig={id}'
        headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com",
            "Host": "game.xiaojukeji.com",
            "Origin": "https://page.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "D-Header-T": f"{Didi_jifen_token}",
            "Content-Type": "application/json;charset=utf-8",
        }
        data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","mission_id":261,"game_id":23,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
        response = requests.post (url=url, headers=headers, verify=False, data=data)
        result = response.json ()
        print (result)
        errmsg = result['errmsg']
        if errmsg == 'success':
            errno = result['errno']
            if errno == 0:
                msg ("【账号{}】【访问消消赚】任务已完成".format (account))
        elif "服务内部错误" in errmsg:
            msg ("【账号{}】【访问消消赚】任务执行失败".format (account))
        else:
            msg ("【账号{}】【访问消消赚】任务早已完成，跳过执行环节".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{}】【访问消消赚】任务失败，可能是token过期".format (account))

# 浇水
def watering(Didi_jifen_token, xpsid, account,wsgsig):
    try:
        i = 1
        water = 0
        while True:
            id = wsgsig[random.randint (0,25)]
            url = f'https://game.xiaojukeji.com/api/game/plant/watering?wsgsig={id}'
            headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Referer": "https://fine.didialift.com/",
                "Host": "game.xiaojukeji.com",
                "Origin": "https://fine.didialift.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "D-Header-T": f"{Didi_jifen_token}",
                "Content-Type": "application/json",
            }
            data = r'{"xbiz":"240301","prod_key":"didi-orchard","xpsid":"' + f'{xpsid}' + r'","dchn":"O9aM923","xoid":"aA/iet7vTTmdKCRAgoHwyg","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f'{xpsid}' + r'","xpsid_from":"","xpsid_share":"","is_fast":false,"platform":1,"token":"' + f'{Didi_jifen_token}' + r'"}'
            # print(data)
            response = requests.post (url=url, headers=headers, verify=False, data=data)
            result = response.json ()
            print (result)
            errmsg = result['errmsg']
            if errmsg == 'success':
                i += 1
                pack_water = result['data']['pack_water']  # 剩余多少g水

                tree_progress = float (100.00) - float (result['data']['tree_progress'])  # 升级进度
                # print(tree_progress)
                water_times = result['data']['water_times']  # 浇水次数
                next_box_progress = result['data']['next_box_progress']  # 下一次领取宝箱需多少g水
                water = i * 10
                if pack_water < 300:
                    msg ("【账号{0}】剩余水滴{1}g，退出浇水".format (account, pack_water))
                    break
                time.sleep (5)
            elif "果实已成熟" in errmsg:
                msg ("【帐号{}】果树已成熟，请自行上线领取".format (account))
                break
            else:
                break
        msg (
            "【账号{5}】本次浇水共{0}g水滴，剩余{1}g水滴，今日一共浇水次数为{2}次，距离果树升级进度{3}%，下一次领取宝箱需浇水{4}".format (water, pack_water, water_times,tree_progress,next_box_progress, account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】浇水异常，请稍后再试试".format (account))


if __name__ == '__main__':
    global msg_info
    print ("============脚本只支持青龙新版=============\n")
    print ("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print ("============执行滴滴果园自动脚本==============")
    # print(Didi_jifen_token)
    missons_list = []
    nowtime = datetime.datetime.now ().strftime ('%Y-%m-%d %H:%M:%S.%f8')
    if Didi_jifen_token != '':
        xpsid = get_xpsid ()
        missons_list = get_missons (Didi_jifen_token, xpsid,wsgsig)
        pet_id = get_pet_id (Didi_jifen_token, xpsid,wsgsig)
        get_treasure (Didi_jifen_token, xpsid, account,wsgsig)
        time.sleep (0.2)
        watering (Didi_jifen_token, xpsid, account,wsgsig)
        if nowtime > get_time1 and nowtime < get_time2:
            do_misson9(Didi_jifen_token, xpsid, account,wsgsig)
        for k in missons_list:
            if "浏览" in k:
                do_sign (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson10 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson1 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson2 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson3 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson4 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson5 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson6 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson7 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson8 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                do_misson11 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                do_misson12 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                do_misson13 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                do_misson14 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)

                get_misson1 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson2 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson3 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson4 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson5 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson6 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson7 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson11 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson16 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                get_misson17 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                get_misson18 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)
                get_misson19 (Didi_jifen_token, xpsid, account, wsgsig)
                time.sleep (0.2)


        for k in missons_list:
            if "每日浇水" in k:
                get_misson8 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson9 (Didi_jifen_token, xpsid, account,wsgsig)
                time.sleep (0.2)
                get_misson10 (Didi_jifen_token, xpsid, account,wsgsig)
                break
        time.sleep (0.2)
        get_misson12 (Didi_jifen_token, xpsid, account,wsgsig)
        time.sleep (0.2)
        get_misson13 (Didi_jifen_token, xpsid, account,wsgsig)
        time.sleep (0.2)
        get_misson14 (Didi_jifen_token, xpsid, account,wsgsig)
        time.sleep (0.2)
        get_misson15 (Didi_jifen_token, xpsid, account,wsgsig)
        time.sleep (0.2)
    elif tokens == '':
        print ("检查变量Didi_jifen_token是否已填写")
    elif len (tokens) > 1:
        account = 1
        for i in tokens:  # 同时遍历两个list，需要用ZIP打包
            xpsid = get_xpsid ()
            missons_list = get_missons (i, xpsid,wsgsig)
            pet_id = get_pet_id (i, xpsid,wsgsig)
            get_treasure (i, xpsid, account,wsgsig)
            time.sleep (0.2)
            watering (i, xpsid, account,wsgsig)
            if nowtime > get_time1 and nowtime < get_time2:
                do_misson9 (i, xpsid, account, wsgsig)
            for k in missons_list:
                if "浏览" in k:
                    do_sign (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson10 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson1 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson2 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson3 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson4 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson5 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson6 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson7 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson8 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    do_misson11 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    do_misson12 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    do_misson13 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    do_misson14 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)

                    get_misson1 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson2 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson3 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson4 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson5 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson6 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson7 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson11 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson16 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    get_misson17 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    get_misson18 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)
                    get_misson19 (i, xpsid, account, wsgsig)
                    time.sleep (0.2)

            for k in missons_list:
                if "每日浇水" in k:
                    get_misson8 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson9 (i, xpsid, account,wsgsig)
                    time.sleep (0.2)
                    get_misson10 (i, xpsid, account,wsgsig)
                    break
            time.sleep (0.2)
            get_misson12 (i, xpsid, account,wsgsig)
            time.sleep (0.2)
            get_misson13 (i, xpsid, account,wsgsig)
            time.sleep (0.2)
            get_misson14 (i, xpsid, account,wsgsig)
            time.sleep (0.2)
            get_misson15 (i, xpsid, account,wsgsig)
            account += 1

    if "饭点领水滴" in msg_info:
        send ("滴滴水果活动", msg_info)
    if "已成熟" in msg_info:
        send ("滴滴水果活动", msg_info)
    elif "过期" in msg_info:
        send ("滴滴水果活动", msg_info)
