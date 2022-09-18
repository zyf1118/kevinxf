#!/bin/env python3
# -*- coding: utf-8 -*
'''

感谢Curtin提供的其他脚本供我参考
感谢aburd ch大佬的指导抓包
项目名称:xF_sfsy.py
Author: 一风一燕
功能：顺丰速递app自动任务
Date: 2022-03-18
cron: 6 13 * * * xF_sfsy.py
new Env('顺丰速递app自动任务');


updata:2022-07-24
修复签到
updata:2022-09-18
修复签到和所有任务


【教程】：需要自行用手机抓取cookies

手机抓包后，自行签到一次，然后查看URL，https://mcs-mimp-web.sf-express.com/mcs-mimp/integralTaskSignService/automaticSignFetchPackage
查看hearders里面的cookie，只需要sessionId=xxxxxx即可。
青龙变量export SF_cookie='sessionId=xxxxxx'

变量do_Treasure='false'，不参与夺宝活动，不设置默认不参与。
变量black_list = 'xxx&xxx&xxx'，过滤夺宝活动，部分不参与。可以参考我的，然后自己修改。
export black_list='13元顺丰优惠券&18元顺丰优惠券&8折同城券&顺丰定制三轮车车模&顺丰定制电动车模型'


cron时间填写：6 13 * * * xF_sfsy.py

'''


SF_cookie = ''
do_Treasure = 'false'
black_list = ''
account = 1
cookies = ''
'''


=================================以下代码不懂不要随便乱动=================================


'''


try:
    import requests
    import json,sys,os,re
    import time,datetime,random
    import hashlib
except Exception as e:
    print(e)

requests.packages.urllib3.disable_warnings()

if "@" in black_list:
    black_list = black_list.split ('@')
pwd = os.path.dirname(os.path.abspath(__file__)) + os.sep
path = pwd + "env.sh"
today = datetime.datetime.now().strftime('%Y-%m-%d')
mor_time ='08:00:00.00000000'
moringtime = '{} {}'.format (today, mor_time)
nowtime = int (round (time.time () * 1000))

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
        cookies = SF_cookie.split('&')
        account = len(cookies)
        printT ("已获取并使用Env环境cookies")
    else:
        printT ("已获取并使用Env环境cookie")
else:
    print("检查变量SF_cookie是否已填写")

if "do_Treasure" in os.environ:
        do_Treasure = os.environ["do_Treasure"]
        printT ("已获取并使用Env环境do_Treasure")
else:
    print("检查变量do_Treasure未填写，默认参与夺宝活动")

if "black_list" in os.environ:
    black_list = os.environ["black_list"]
    if "@" in black_list:
        black_list = black_list.split('@')
        printT ("已获取并使用Env环境black_list")
else:
    print("检查变量black_list未填写，默认夺宝活动不过滤")


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

def md5_encode(encode_data):

    # print(encode_data)

    md5=hashlib.md5()   # 应用MD5算法

    data = encode_data

    md5.update(data.encode('utf-8'))

    # print(md5.hexdigest().upper())

    return md5.hexdigest()


#执行积分签到
def do_sign(SF_cookie,sign_data,timestamp,account):
    try:
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/integralTaskSignPlusService/automaticSignFetchPackage'
        data = '{"comeFrom":"vioin","channelFrom":"SFAPP"}'
        hearders = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
            "cookie":SF_cookie,
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh-Hans;q=0.9",
            "accept": "application/json, text/plain, */*",
            "Host": "mcs-mimp-web.sf-express.com",
            "content-type": "application/json;charset=utf-8",
            "timestamp":f"{timestamp}",
            "signature":sign_data,
            "syscode":"MCS-MIMP-CORE",
            "origin":"https://mcs-mimp-web.sf-express.com",
        }
        response = requests.post(url=url,headers=hearders,data=data,verify=False)
        result = response.json()
        print(result)
        hasFinishSign = result['obj']['hasFinishSign']
        if hasFinishSign == 1:
            msg("【账号{0}】今日已签到，无需重复签到".format(account))
        else:
            countDay = result['obj']['countDay']
            commodityName = result['obj']['integralTaskSignPackageVOList'][0]['commodityName']
            msg("【账号{0}】今日签到成功，连续签到{1}天，获得【{2}】".format(account,countDay,commodityName))

    except Exception as e:
        print(e)
        msg("【账号{}】签到失败，可能是Cookie过期".format(account))


# 执行超值福利签到
def do_sign2(SF_cookie,sign_data,timestamp,account):
    try:
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberActLengthy~redPacketActivityService~superWelfare~receiveRedPacket'
        data = '{"channel":"SignIn"}'
        hearders = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
            "cookie": f"{SF_cookie}",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-CN",
            "accept": "*/*",
            "Host": "mcs-mimp-web.sf-express.com",
            "content-type": "application/json",
            # "timestamp": f"{timestamp}",
            # "signature": sign_data
        }
        response = requests.post (url=url, headers=hearders, data=data, verify=False)
        # print(response.text)
        result = response.json ()
        print (result)
        success = result['success']
        if success == True:
            giftName = result['obj']['giftList'][0]['giftName']
            msg ("【账号{0}】超值福利签到成功，获得【{1}】奖励".format (account,giftName))

    except Exception as e:
        print (e)


#获取任务列表
def task_list(SF_cookie,sign_data,timestamp,account):
    try:
        url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~queryPointTaskAndSignFromES'
        data = '{"channelType":"1"}'
        hearders = {
            "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
            "Cookie": f"{SF_cookie}",
            "Accept-Encoding": "gzip, deflate, br",
            "accept-language": "zh-cn",
            "accept": "application/json, text/plain, */*",
            "Host": "mcs-mimp-web.sf-express.com",
            "content-type": "application/json;charset=utf-8",
            "timestamp": f"{timestamp}",
            "signature": sign_data,
            "syscode": "MCS-MIMP-CORE",
        }
        response = requests.post (url=url, headers=hearders,data=data,verify=False)
        result = response.json()
        # print(result)
        list = result['obj']['taskTitleLevels']
        for i in range(len(list)):
            taskId = list[i]['taskId']
            strategyId = list[i]['strategyId']
            taskCode = list[i]['taskCode']
            title = list[i]['description']
            if "邀请" in title:
                pass
            else:
                do_mission (SF_cookie,title, taskCode,sign_data,timestamp,account)
                reward_mission (SF_cookie,title,strategyId, taskId, taskCode, sign_data,timestamp,account)

    except Exception as e:
        print(e)
        msg ("【账号{0}】获取任务列表失败,可能是cookie过期".format(account))


#做任务
def do_mission(SF_cookie,title,taskCode,sign_data,timestamp,account):
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonRoutePost/memberEs/taskRecord/finishTask'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie":f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-Hans;q=0.9",
        "accept": "*/*",
        "Host": "mcs-mimp-web.sf-express.com",
        "timestamp": f"{timestamp}",
        "signature": sign_data
    }
    data = '{"taskCode":"' + f'{taskCode}' + '"}'
    response = requests.get (url=url, headers=hearders, verify=False,data=data)
    result = response.json()
    print(result)
    success = result['success']
    if success == True:
        printT("【账号{0}】正在执行【{1}】任务，等待20秒".format(account,title))
        time.sleep(20)


#抽奖任务
def do_lottery(SF_cookie,sign_data,timestamp,account):
    url = f'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~multiIntegralLotteryService~lottery'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie":f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-Hans;q=0.9",
        "accept": "application/json, text/plain, */*",
        "Host": "mcs-mimp-web.sf-express.com",
        "content-type":"application/json;charset=utf-8",
        "timestamp": f"{timestamp}",
        "signature": sign_data
    }
    data = '{"lotteryType":"NINE_POINT","continuityLotteryFlag":0}'
    response = requests.post (url=url, headers=hearders, verify=False,data=data)
    result = response.json()
    print(result)
    success = result['success']
    if success == True:
        giftName = result['obj'][0]['commodityName']
        msg("【账号{0}】参与抽奖，获得【{1}】奖励".format(account,giftName))

#领取奖励
def reward_mission(SF_cookie,title,strategyId,taskId,taskCode,sign_data,timestamp,account):
    url = 'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTaskStrategyService~fetchIntegral'
    data = '{"strategyId":' + f"{strategyId}" + ',"taskId":"' + f"{taskId}" + '","taskCode":"' + f"{taskCode}" + '"}'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie":f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-cn",
        "accept": "application/json, text/plain, */*",
        "Host": "mcs-mimp-web.sf-express.com",
        "content-type": "application/json;charset=utf-8",
        "timestamp": f"{timestamp}",
        "signature": sign_data
    }
    response = requests.post (url=url, headers=hearders, data=data, verify=False)
    result = response.json()
    print(result)
    success = result['success']
    if success == True:
        point = result['obj']['point']
        msg("【账号{0}】执行【{2}】任务成功，领取{1}积分".format(account,point,title))
    else:
        errorMessage = result['errorMessage']
        if "已领取" in errorMessage:
            msg ("【账号{0}】【{1}】任务已完成".format (account,title))


#夺宝活动
def Treasure_list(SF_cookie,sign_data,timestamp,account):
    url = f'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTreasureService~queryHomePageInfo'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie":f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-Hans;q=0.9",
        "accept": "application/json, text/plain, */*",
        "Host": "mcs-mimp-web.sf-express.com",
        "content-type":"application/json;charset=utf-8",
        "timestamp": f"{timestamp}",
        "signature": sign_data
    }
    data = '{}'
    response = requests.post (url=url, headers=hearders, verify=False,data=data)
    result = response.json()
    # print(result)
    list = result['obj']['activityInfoList']
    for i in range(len(list)):
        pkgName = list[i]['pkgName']
        flowId = list[i]['flowId']
        if pkgName in black_list:
            pass
        else:
            Treasure(SF_cookie,flowId,pkgName,sign_data,timestamp,account)

#参与夺宝
def Treasure(SF_cookie,flowId,pkgName,sign_data,timestamp,account):
    url = f'https://mcs-mimp-web.sf-express.com/mcs-mimp/commonPost/~memberNonactivity~integralTreasureService~partakeTreasure'
    hearders = {
        "user-agent": f"Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 mediaCode=SFEXPRESSAPP-iOS-ML",
        "Cookie":f"{SF_cookie}",
        "Accept-Encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh-Hans;q=0.9",
        "accept": "application/json, text/plain, */*",
        "Host": "mcs-mimp-web.sf-express.com",
        "content-type":"application/json;charset=utf-8",
        "timestamp": f"{timestamp}",
        "signature": sign_data
    }
    data = '{"flowId":' + f"{flowId}" + r',"partakeNums":1,"points":9}'
    response = requests.post (url=url, headers=hearders, verify=False,data=data)
    result = response.json()
    success = result['success']
    if success == True:
        msg("【账号{0}】参与【{1}】夺宝成功，消耗9积分".format(account,pkgName))
        time.sleep(2)


if __name__ == '__main__':
    global msg_info
    print("============脚本只支持青龙新版=============\n")
    print("具体教程以文本模式打开文件，查看顶部教程\n\n")
    print("============执行顺丰速运APP签到脚本==============")
    a = 1
    timestamp = int (round (time.time () * 1000))
    encode_str = f'token=wwesldfs29aniversaryvdld29&timestamp={timestamp}&sysCode=MCS-MIMP-CORE'
    sign_data = md5_encode (encode_str)
    if cookies != '':
        for SF_cookie in cookies:
                if a <= account:
                    msg ("★★★★★正在执行【账号{}】的任务★★★★★".format (a))
                    do_sign(SF_cookie,sign_data,timestamp,a)
                    do_sign2(SF_cookie,sign_data,timestamp,a)
                    do_lottery (SF_cookie,sign_data,timestamp,a)
                    task_list(SF_cookie,sign_data,timestamp,a)
                    if do_Treasure == 'true':
                        Treasure_list (SF_cookie,sign_data,timestamp,a)
                    a += 1
                else:
                    break
    elif SF_cookie != '':
        do_sign (SF_cookie, sign_data,timestamp,a)
        do_sign2 (SF_cookie, sign_data,timestamp,a)
        do_lottery (SF_cookie, sign_data,timestamp,a)
        task_list (SF_cookie, sign_data,timestamp,a)
        if do_Treasure == 'true':
            Treasure_list (SF_cookie, sign_data,timestamp,a)
    if '成功' in msg_info:
        send ("顺丰速运", msg_info)
    if '过期' in msg_info:
        send ("顺丰速运", msg_info)

