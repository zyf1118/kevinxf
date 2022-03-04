#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_DiDi_ssz.py
Author: 一风一燕
功能：刷刷赚签到
Date: 2021-12-6
cron: 23 10,15 * * * xF_DiDi_ssz.py
new Env('滴滴app刷刷赚签到');


****************滴滴出行APP*******************


【教程】：需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token用&隔开，例如Didi_jifen_token='xxxxx&xxxx'

手机抓包后，在手机点击，福利中心的明细，查看一次福利金明细后，搜索token=，token=xxxx&city，xxx便是Didi_jifen_token。

或者查看一次福利金明细后，查看URL，
https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?，后面的token=xxxx&city，xxx便是Didi_jifen_token。

cron时间填写：23 10,15 * * *

'''



Didi_jifen_token = ''
account = 1

'''


=================================以下代码不懂不要随便乱动=================================


'''

Didi_jifen_tokens = ''

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
tomorrow = (datetime.datetime.now() + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
mor_time ='08:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)



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
#     if "DiDi_token" in ck:
#         r = re.compile (r'DiDi_token="(.*?)"', re.M | re.S | re.I)
#         tokens = r.findall(ck)
#         tokens = tokens[0].split ('&')
#         if len (tokens) == 1:
#             DiDi_token = tokens[0]
#             tokens = ''
#     #     print(tokens)
#     #     tokens = Didi_jifen_token[3]
#         else:
#             DiDi_token = tokens[0]
#     printT ("已获取并使用ck环境 token")
#
# with open(path, "r+", encoding="utf-8") as f:
#     ck = f.read()
#     Didi_jifen_token = ck
#     if "Didi_jifen_token" in ck:
#         r = re.compile (r'Didi_jifen_token="(.*?)"', re.M | re.S | re.I)
#         Didi_jifen_token = r.findall (ck)
#         Didi_jifen_token = Didi_jifen_token[0].split('&')
#     if len(Didi_jifen_token) == 1:
#         Didi_jifen_token = Didi_jifen_token[0]
#         Didi_jifen_token = ''
#     #     print(Didi_jifen_token)
#     #     Didi_jifen_token = Didi_jifen_token[3]
#     else:
#         Didi_jifen_token = Didi_jifen_token[0]
#     printT ("已获取并使用ck环境 Didi_jifen_token")

########################################################################



if "Didi_jifen_token" in os.environ:
    print(len (os.environ["Didi_jifen_token"]))
    if len (os.environ["Didi_jifen_token"]) > 363:
        Didi_jifen_tokens = os.environ["Didi_jifen_token"]
        # temporary = Didi_jifen_token.split ('&')
        # Didi_jifen_token = temporary[0]
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


if Didi_jifen_tokens != '':
        Didi_jifen_tokens = Didi_jifen_tokens.split ('&')
        # print(Didi_jifen_tokens)


#获取xpsid
def get_xpsid():
    try:
        url = f'https://v.didi.cn/DpQ3dga?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812212&maptype=soso&os=iOS&utc_offset=480&location_cityid=21&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&cityid=21&location_country=CN&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016388&origin_id=1&client_type=1&terminal_id=1&sig=b84826e0429da615f74ec92157c513fa809e9e8b'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head (url=url, headers=heards, verify=False)    #获取响应请求头
        res = response.headers['Location']                                  #获取响应请求头
        # print(res)
        r = re.compile (r'root_xpsid=(.*?)&channel_id')
        xpsid = r.findall (res)
        xpsid = xpsid[0]
        print(xpsid)
        return xpsid
    except Exception as e:
        print(e)
        msg("获取xpsid失败，可能是表达式错误")


#查看福利金
def get_fulijin(Didi_jifen_token,account,wsgsig):
    try:
        wsgsig1 = wsgsig[random.randint (0, 25)]
        nowtime = int (round (time.time () * 1000))
        info_url = f'https://rewards.xiaojukeji.com/loyalty_credit/bonus/getWelfareUsage4Wallet?wsgsig={wsgsig1}&token={Didi_jifen_token}&city_id=21'
        info_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://page.udache.com",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "host": "rewards.xiaojukeji.com",
        }
        response = requests.get (url=info_url, headers=info_headers, verify=False)
        result = response.json()
        print(result)
        balance = result['data']['balance']
        msg("【账号{1}】现总共有{0}福利金".format(balance,account))

    except Exception as e:
        print(e)
        msg ("【账号{}】获取福利金信息失败,可能是Didi_jifen_token过期".format(account))



#执行积分签到
def do_sign(Didi_jifen_token,xpsid,account):
    try:
        uid = ''.join (random.sample ('01234657890123456789', 15))     #281474990465673
        imei = ''.join (random.sample ('123456789abcdef123456789abcdef123456789abcdef123456789abcdef', 32))
        wsgsig1 = wsgsig[random.randint (0, 25)]
        do_sign_url = f'https://bosp-api.xiaojukeji.com/gulfstream/hubble/open/signin/submit?wsgsig={wsgsig1}'
        data = r'{"xbiz":"240200","prod_key":"ut-discover","xpsid":"' + f"{xpsid}" + r'","dchn":"7mPlO68","xoid":"9921f9b4-e3f1-444f-8409-dec4e9af99e4","uid":"' + f'{uid}' + r'","xenv":"passenger","xspm_from":"","xpsid_root":"' + f"{xpsid}" + r'","xpsid_from":"","xpsid_share":"","token":"' + f"{Didi_jifen_token}" + r'","lat":"23.0164990234375","lng":"113.81229031032986","city_id":21,"env":"{\"newTicket\":\"' + f"{Didi_jifen_token}" + r'\",\"latitude\":\"23.0164990234375\",\"longitude\":\"113.81229031032986\",\"cityId\":\"21\",\"userAgent\":\"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0\",\"appVersion\":\"6.2.4\",\"wifi\":\"1\",\"model\":\"iPhone 11\",\"ddfp\":\"'+ f'{imei}' + r'\",\"fromChannel\":\"1\",\"newAppid\":\"10000\",\"isHitButton\":false,\"isOpenWeb\":true,\"timeCost\":36}","openid":"","platform":"na","res_params":"{\"resource_names\":\"didipas_find_feed\",\"appversion\":\"6.2.4\",\"channel_id\":\"\",\"platform_type\":1}"}'
        do_sign_heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Referer": "https://page.udache.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "origin": "https://page.udache.com",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "host":"bosp-api.xiaojukeji.com",
        }
        response = requests.post(url=do_sign_url,data=data,headers=do_sign_heards,verify=False)
        do_sign_ = response.json()
        print(do_sign_)
        code = do_sign_['errno']   #本次签到获得的积分
        if code == 200100:
            msg("【账号{}】今日刷刷赚已签到，无需重复签到".format(account))
        elif code == 0:
            #prize_status = do_sign_['data']['prize_status']   #5天签到周期内签到第几天
            content = do_sign_['data']['content']
            content = content[6:]
            msg("【账号{1}】今日签到成功，获得{0}，".format(content,account))

    except Exception as e:
        print(e)
        msg ('【账号{}】刷刷赚签到异常，可能是token过期'.format (account))








if __name__ == '__main__':

    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行刷刷赚签到脚本==============")
    if Didi_jifen_token != '':
        xpsid = get_xpsid()
        do_sign(Didi_jifen_token,xpsid,account)
        get_fulijin(Didi_jifen_token,account,wsgsig)

    elif Didi_jifen_tokens != '':
        for j in Didi_jifen_tokens:             #同时遍历两个list，需要用ZIP打包
            xpsid = get_xpsid ()
            do_sign(j,xpsid,account)
            get_fulijin (j,account,wsgsig)
            account += 1
    else:
        print ("检查变量Didi_jifen_token是否已填写")

    if "签到成功" in msg_info or "已签到" in msg_info:
        send("滴滴刷刷赚签到", msg_info)
    elif "过期" in msg_info:
        send("滴滴刷刷赚签到", msg_info)