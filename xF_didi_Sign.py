#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢CurtinLV提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_didi_Sign.py
Author: 一风一燕
功能：滴滴出行积分签到+抽奖
Date: 2021-11-4
cron: 22 5,10 * * * xF_didi_Sign.py
new Env('滴滴app积分签到+抽奖');



****************滴滴出行APP*******************


【教程】：需要自行用手机抓取Didi_jifen_token。
在青龙变量中添加变量Didi_jifen_token
多个账号时，Didi_jifen_token，用&隔开，例如Didi_jifen_token=xxxxx&xxxx

手机抓包后，积分签到一次，查看URL，https://gsh5act.xiaojukeji.com/dpub_data_api/activities/9612/signin?signin_user_token=xxxx
其中URL中的9612，这数字是会变的，以前每期签到都不一样，但是你按照我的路径去找，就能找到token
搜索signin_user_token=，就是你需要的token。

如果想用积分抽奖，在青龙变量中添加变量do_lottery=true，默认是false。
抽奖id如何抓取：
手机抓包后，点击我的，点击积分商城，再点击抽奖赚积分，进入到抽奖界面后，查看URL，https://dpubstatic.udache.com/static/dpubimg/dpub2_project_xxxxx/index_xxxxx.json?r=0.6781450893324913?ts=1637987237802&app_id=common
xxxx是会变的，按路径找就行了。然后查看josn里面的activity_id，就是lottery_lid。

青龙添加变量lottery_lid='8fnkiv4b'，8fnkiv4b这个就是上面抓包得到的activity_id。

这个抽奖的lottery_lid，需要每周一自行抓包更新才能抽，所以我设置了是否抽奖的开关。

cron时间填写：22 7,10 * * *

特别说明：本脚本需要从星期一签到，作为第一天签到，如果今天是星期二，你之前没签到过，那脚本是不能签到的。

'''


Didi_jifen_token = ''
do_lottery = 'false'
lottery_lid = ''

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
today = datetime.datetime.now().strftime('%Y-%m-%d')
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


if "do_lottery" in os.environ:
    do_lottery = os.environ["do_lottery"]
    printT ("已获取并使用Env环境do_lottery")
else:
    print("do_lottery为fasle，不进行积分抽奖")

if "lottery_lid" in os.environ:
    lottery_lid = os.environ["lottery_lid"]
    printT ("已获取并使用Env环境lottery_lid")


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
            # print(Didi_jifen_token)

        else:
            pass

def get_xpsid():
    try:
        url = f'https://v.didi.cn/p/DpzAd35?appid=10000&lang=zh-CN&clientType=1&trip_cityid=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&channel=102&appversion=6.2.4&trip_country=CN&TripCountry=CN&lng=113.812538&maptype=soso&os=iOS&utc_offset=480&access_key_id=1&deviceid=99d8f16bacaef4eef6c151bcdfa095f0&phone=UCvMSok42+5+tfafkxMn+A==&model=iPhone11&lat=23.016271&origin_id=1&client_type=1&terminal_id=1&sig=8503d986c0349e40ea10ff360f75d208c78c989a'
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
        }
        response = requests.head (url=url, headers=heards, verify=False)  # 获取响应请求头
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


#获取v.didi.cn的url
def get_v_url(Didi_jifen_token):
    nowtime = int (round (time.time () * 1000))
    url = f'https://common.diditaxi.com.cn/common/v5/usercenter/me?_t={nowtime}&access_key_id=1&appversion=6.2.4&channel=102&city_id=21&datatype=101&imei=99d8f16bacaef4eef6c151bcdfa095f0&lang=zh-CN&maptype=soso&model=iPhone&networkType=WIFI&os=15.0&sig=c783e6e425a59349309ad10a4c1843a54fc9e82c&terminal_id=1&token={Didi_jifen_token}&v6x_version=1'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
    }
    response = requests.get (url=url, headers=heards, verify=False)    #获取响应请求头
    result = response.json()                                       #获取响应请求头
    # print(result)
    bottom_items = result['data']['cards'][3]['bottom_items']
    for i in range(len(bottom_items)):
        title = bottom_items[i]['title']
        if "积分商城" in title:
            link = bottom_items[i]['link']
            # print(link)
            v_url = link[18:]
            print(v_url)
    return v_url
    # print(json.dumps(result,sort_keys=True,indent=4,ensure_ascii=False))         #格式化后的json

#获取s.didi.cn的url
def get_s_url():
    nowtime = int (round (time.time () * 1000))
    url = f'https://v.didi.cn/K0gkogR'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
    }
    response = requests.head (url=url, headers=heards, verify=False)            #获取响应请求头
    result = response.headers['Location']                                       #获取响应请求头
    # print(result)
    s_url = result[18:]
    s_url = s_url[:6]
    # print(s_url)
    return s_url


#获取url
def get_url(s_url):
    url = f'https://s.didi.cn/{s_url}?channel_id=72%2C278%2C80537&entrance_channel=7227880537&xsc=&dchn=K0gkogR&prod_key=custom&xbiz=&xpsid=cc2e4bc570d74253ad56b6c927473c0d&xenv=passenger&xspm_from=&xpsid_from=&xpsid_root=cc2e4bc570d74253ad56b6c927473c0d'
    heards = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
    }
    response = requests.head (url=url, headers=heards, verify=False)    #获取响应请求头
    res = response.headers['location']                                  #获取响应请求头
    # print(res)
    r = re.compile (r'dpubimg/(.*?)/index.html', re.M | re.S | re.I)
    url_id = r.findall (res)
    url_id = url_id[0]
    print(url_id)
    return url_id

#获取签到ID
def get_id(url_id):
    try:
        day = time.localtime ()
        day = time.strftime ("%w", day)  # 今天星期几，0代表星期天
        day = int (day)
        url = f'https://dpubstatic.udache.com/static/dpubimg/{url_id}/index.html?channel_id=72%2C278%2C80537&dchn=K0gkogR&entrance_channel=7227880537&prod_key=custom&xbiz=&xenv=passenger&xpsid=9ef4ad1c8e3d42fab6d9823bc4f9838b&xpsid_from=&xpsid_root=9ef4ad1c8e3d42fab6d9823bc4f9838b&xsc=&xspm_from='
        heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "https://page.udache.com/",
            "Host": "dpubstatic.udache.com",
            "Origin": "https://dpubstatic.udache.com",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        }
        response = requests.get (url=url, headers=heards,verify=False)
        result = response.content.decode('utf-8')
        # print (result)
        r = re.compile (r',"activity_id":"(.*?)","dpubConfigId"', re.M | re.S | re.I)
        numb = r.findall (result)
        numb = numb[0]
        # print(numb)
        if int (day) == 0:
            day = int (day) + 7
        if day == 1 or day == 2:
            r = re.compile (r'{"day":1,"prize_type":2,"prize_id":"(.*?)"', re.M | re.S | re.I)
            id = r.findall (result)
            id = id[0]
        elif day == 3:
            r = re.compile (r'{"day":3,"prize_type":2,"prize_id":"(.*?)"', re.M | re.S | re.I)
            id = r.findall (result)
            id = id[0]
        elif day == 4:
            r = re.compile (r'{"day":4,"prize_type":2,"prize_id":"(.*?)"', re.M | re.S | re.I)
            id = r.findall (result)
            id = id[0]
        elif day == 5 or day == 6:
            r = re.compile (r'{"day":5,"prize_type":2,"prize_id":"(.*?)"', re.M | re.S | re.I)
            id = r.findall (result)
            id = id[0]
        else:
            r = re.compile (r'{"day":7,"prize_type":2,"prize_id":"(.*?)"', re.M | re.S | re.I)
            id = r.findall (result)
            id = id[0]
        return numb,id,day
    except Exception as e:
        print (e)
        msg ("【账号{0}】获取签到ID失败,可能是表达式错误".format (account))

#获取个人信息
def get_activity_info(Didi_jifen_token,day,numb,account):
    try:

        do_sign_url = f'https://gsh5act.xiaojukeji.com/dpub_data_api/activities/{numb}/signin'
        data = r'{"signin_day":' + f"{day}" + r',"signin_type":0,"signin_user_token":' + '"' + f'{Didi_jifen_token}' + r'"}'
        # print(data)
        do_sign_heards = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "Referer": "https://dpubstatic.udache.com/",
            "Host": "gsh5act.xiaojukeji.com",
            "Origin": "https://dpubstatic.udache.com",
            "Accept-Language": "zh-cn",
        }
        response = requests.post (url=do_sign_url, headers=do_sign_heards, data=data, verify=False)
        do_sign_ = response.json ()
        print (do_sign_)
        code = do_sign_['errmsg']
        if "已结束" in code:
            msg("【账号{}】获取签到ID异常".format(account))
        elif "已经" in code:
            print (do_sign_)
            msg ("【账号{}】今日已签到，跳过签到环节".format(account))
        elif code == '':
            msg ("【账号{}】今日签到成功".format (account))

    except Exception as e:
        print (e)
        msg ("【账号{0}】获取签到信息失败,可能是cookies过期".format (account))

#获取积分
def reward(Didi_jifen_token,day,numb,account,id):

    try:
        while True:
            nowtime = int (round (time.time () * 1000))
            info_url = f'https://gsh5act.xiaojukeji.com/dpub_data_api/activities/{numb}/reward_lottery'
            info_headers = {
                "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "Referer": "https://dpubstatic.udache.com",
                "Host": "gsh5act.xiaojukeji.com",
                "Origin": "https://dpubstatic.udache.com",
                "Accept-Language": "zh-CN,zh-Hans;q=0.9",
                "content-type":"application/json; charset=utf-8",
                "content-length":"272",
            }
            data = '{'+ f'"user_token":"{Didi_jifen_token}","signin_day":{day},"lottery_id":"{id}"' +'}'
            response = requests.post(url=info_url, headers=info_headers, verify=False,data=data)
            list = response.json()
            print(list)
            flag = list['errmsg']
            if "签到当天奖励" in flag:
                break
            elif "未完成签到次数" in flag:
                msg("请从星期一开始运行此脚本，请看脚本最上面的说明")
                break
            elif "activity is not" in flag:
                numb += 2
                if numb == 12000:
                    msg("签到异常")
                    break
            else:
                reward = list['lottery']['prize']['name']
                # print(reward)
                total_reward = list['lottery']['userinfo']['current_point']  #总积分
                # print(total_reward)
                msg("【账号{2}】本次签到获取{0},账号共有{1}积分".format(reward,total_reward,account))
                break
    except Exception as e:
        print(e)
        # msg ("【账号{0}】获取积分失败,可能是cookies过期".format(account))


#获取抽奖lid
def get_lid():
    try:
        nowtime = int (round (time.time () * 1000))     #13位
        info_url = f'https://dpubstatic.udache.com/static/dpubimg/dpub2_project_1275480/index_VYom0.json?r=0.07526362250404772?ts={nowtime}&app_id=common'
        info_headers = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 didi.passenger/6.2.4 FusionKit/1.2.20 OffMode/0",
            "Accept": "application/json, text/plain, */*",
            "Referer": "https://page.udache.com/",
            "Host": "dpubstatic.udache.com",
            "Origin": "https://page.udache.com",
        }
        response = requests.get(url=info_url, headers=info_headers, verify=False)
        result = response.json()
        print(result)
        activity_id = result['activity_id']
        return activity_id
    except Exception as e:
        print(e)
        msg ("【账号{0}】获取获取抽奖lid失败,可能是cookies过期".format(account))


#抽奖活动
def do_Lottery(Didi_jifen_token,lottery_lid,account):
    try:
        flag = 6
        # nowtime = int (round (time.time () * 1000))
        while True:
            do_Lottery_url = f'https://bosp-api.xiaojukeji.com/bosp-api/lottery/draw?lid={lottery_lid}&token={Didi_jifen_token}&env=%7B%22longitude%22%3A113.81251003689236%2C%22latitude%22%3A23.016395128038194%2C%22cityId%22%3A%2221%22%2C%22deviceId%22%3A%2299d8f16bacaef4eef6c151bcdfa095f0%22%2C%22ddfp%22%3A%2299d8f16bacaef4eef6c151bcdfa095f0%22%2C%22appVersion%22%3A%226.2.4%22%2C%22wifi%22%3A1%2C%22model%22%3A%22iPhone%2011%22%2C%22timeCost%22%3A637425%2C%22userAgent%22%3A%22Mozilla%2F5.0%20(iPhone%3B%20CPU%20iPhone%20OS%2015_0%20like%20Mac%20OS%20X)%20AppleWebKit%2F605.1.15%20(KHTML%2C%20like%20Gecko)%20Mobile%2F15E148%20didi.passenger%2F6.2.4%20FusionKit%2F1.2.20%20OffMode%2F0%22%2C%22isHitButton%22%3Atrue%7D'
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
                msg("【账号{}】抽奖次数已达上限，跳出抽奖环节".format(account))
                break
            elif code == 20017:
                msg("【账号{}】抽奖操作过频，稍后再试".format(account))
                break
            elif code == 20008:
                msg("【账号{}】抽奖lid过期，请重新抓包更新".format(account))
                break
            elif code == 20010:
                msg ("【账号{}】积分不足9分，跳出抽奖环节".format (account))
                break
            else:
                draw_times = result['data']['userinfo']['draw_times']
                flag = 6 - int(draw_times)
                name = result['data']['prize']['name']
                current_point = result['data']['userinfo']['current_point']
                msg("【账号{3}】第{0}次抽奖获得{1},现账号共有{2}积分".format(flag,name,current_point,account))
                time.sleep(5)
    except Exception as e:
        print(e)
        msg ("【账号{0}】抽奖失败,可能是cookies过期".format(account))


if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行滴滴积分签到脚本==============")
    # xpsid = get_xpsid()
    s_url = get_s_url()
    url_id = get_url (s_url)
    numb,id,day = get_id(url_id)

    # numb = 9620
    # v_url = get_v_url (Didi_jifen_token)
    if Didi_jifen_token != '':
        get_activity_info(Didi_jifen_token,day,numb,account)
        reward(Didi_jifen_token,day,numb,account)
        # activity_id = get_lid ()
        if do_lottery == 'true':
            do_Lottery (Didi_jifen_token,lottery_lid,account)

    elif tokens == '' :
        print("检查变量Didi_jifen_token，DD_cookies是否已填写")
    elif len(tokens) > 1 :
        account = 1
        for i in tokens:             #同时遍历两个list，需要用ZIP打包
            get_activity_info (i, day,numb,account)
            reward (i, day,numb,account,id)
            # activity_id = get_lid()
            if do_lottery == 'true':
                do_Lottery (i,lottery_lid,account)
            account += 1

    if "签到" in msg_info:
        send("滴滴积分签到", msg_info)
    elif "过期" in msg_info:
        send("滴滴积分签到", msg_info)
