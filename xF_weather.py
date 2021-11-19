# -*- coding: utf-8 -*-
"""
cron: 0 7 * * *
new Env('天气预报');
"""

"""

浏览器输入：https://github.com/baichengzhou/weather.api/blob/master/src/main/resources/citycode-2019-08-23.json
搜索想查看的城市对应的city_code，复制下来，填写在青龙环境变量即可。
city_numb="1234"，多个城市用&隔开，例如city_numb="1234&5678"



"""




try:
    import requests
    import json,sys,os,re
    import time,datetime
except Exception as e:
    print(e)


city_numb = []

def printT(s):
    print("[【{0}】]: {1}".format(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), s))
    sys.stdout.flush()


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


if "city_numb" in os.environ:
    print(len (os.environ["city_numb"]))
    if len (os.environ["city_numb"]) > 8:
        city_numb = os.environ["city_numb"]
        # print(city_numb)
        city_numb = city_numb.split ('&')
        # city_numb = temporary[0]
        printT ("已获取并使用Env环境city_numb")
    else:
        city_numb = os.environ["city_numb"]
else:
    print("检查变量city_numb是否已填写")



def weather(city_numb):
    """
    获取天气信息。网址：https://www.sojson.com/blog/305.html
    :return:
    """
    msg = ''
    msg_result = ''
    for city_name in city_numb:
        weather_url = f"http://t.weather.itboy.net/api/weather/city/{city_name}"
        response = requests.get(url=weather_url)
        if response.status_code == 200 and response.json().get("status") == 200:
            result = response.json()
            msg = (
                "\n城市："
                + result["cityInfo"]["parent"]
                + " "
                + result["cityInfo"]["city"]
                + "\n日期："
                + result["data"]["forecast"][0]["ymd"]
                + " "
                + result["data"]["forecast"][0]["week"]
                + "\n天气："
                + result["data"]["forecast"][0]["type"]
                + "\n温度："
                + result["data"]["forecast"][0]["high"]
                + " "
                + result["data"]["forecast"][0]["low"]
                + "\n湿度："
                + result["data"]["shidu"]
                + "\n空气质量："
                + result["data"]["quality"]
                + "\nPM2.5："
                + str(result["data"]["pm25"])
                + "\nPM10："
                + str(result["data"]["pm10"])
                + "\n风力风向："
                + result["data"]["forecast"][0]["fx"]
                + " "
                + result["data"]["forecast"][0]["fl"]
                + "\n感冒指数："
                + result["data"]["ganmao"]
                + "\n温馨提示："
                + result["data"]["forecast"][0]["notice"]
                + "\n更新时间："
                + result["time"]
                )
            print(msg)
        msg_result += msg + "\n\n"
    return msg_result


if __name__ == "__main__":
    # city_numb =["101281601","101280101","101280501"]
    res = weather(city_numb)
    send("天气预报", res)
