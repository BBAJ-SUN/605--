import requests
import re
from bs4 import BeautifulSoup
import bs4
import pandas as pd
from ast import literal_eval
import ast

#得到当天的数据
def get_url(url):
    r1=requests.get(url)
    r1.encoding = r1.apparent_encoding
    soup = BeautifulSoup(r1.text, 'html.parser')
    result = soup.findAll('div',attrs={'class':'left-div'})
    result = result[2].find("script").string
    #正则表达式
    r_content=r"=\s(.*);"
    result = re.compile(r_content).findall(result)
    #将字符串列表(字符串字典)转换成列表(字典)
    result = literal_eval(result[0])
    return result
def get_data(dic):
    frame=pd.DataFrame(columns=["地区","时间","温度","风向","风级","降水量",
                                "相对湿度","空气质量"])
    time = []
    temp = []
    wind_dir = []
    wind_level = []
    rainfall = []
    humidity = []
    air_quality = []
    count=-1
    for i in range(len(dic["od"]["od2"])-1):
        time.append(dic["od"]["od2"][count]["od21"])
        temp.append(dic["od"]["od2"][count]["od22"])
        wind_dir.append(dic["od"]["od2"][count]["od24"])
        wind_level.append(dic["od"]["od2"][count]["od25"])
        rainfall.append(dic["od"]["od2"][count]["od26"])
        humidity.append(dic["od"]["od2"][count]["od27"])
        air_quality.append(dic["od"]["od2"][count]["od28"])
        count = count-1
    frame["时间"]=time
    frame["地区"]=dic["od"]["od1"]
    frame["温度"]=temp
    frame["风向"]=wind_dir
    frame["风级"]=wind_level
    frame["降水量"]=rainfall
    frame["相对湿度"]=humidity
    frame["空气质量"]=air_quality
    frame=frame[["地区","时间","温度","风向","风级","降水量",
                                "相对湿度","空气质量"]]
    return frame
#未来七天数据
def seven_days(url):
    r1 = requests.get(url)
    r1.encoding = r1.apparent_encoding
    #正则表达式
    r_content=r"hour3data=(.*)"
    result = re.compile(r_content).findall(r1.text)
    result = literal_eval(result[0])
    return result
def seven_days_data(result,dic):
    data = pd.DataFrame(columns=["地区","时间","天气","温度","风向","风级"])
    time = []
    weather = []
    temp = []
    wind_dir = []
    wind_level = []
    for i in range(7):
        for j in range(len(result[i])):
            data_str = result[i][j]
            data_str = data_str.split(",")
            time.append(data_str[0])
            weather.append(data_str[2])
            temp.append(data_str[3])
            wind_dir.append(data_str[4])
            wind_level.append(data_str[5])
    data["时间"]=time
    data["天气"]=weather
    data["温度"]=temp
    data["风向"]=wind_dir
    data["风级"]=wind_level
    data["地区"]=dic["od"]["od1"]
    data=data[["地区","时间","天气","温度","风向","风级"]]
    return data
    
url = []
for i in range(1,12):
    if (i<10):
        url.append("http://www.weather.com.cn/weather/10124"+"0"+str(i)+"01.shtml")
    else:
        url.append("http://www.weather.com.cn/weather/10124"+str(i)+"01.shtml")


data_today_JX = pd.DataFrame(columns=["地区","时间","温度","风向","风级","降水量",
                                "相对湿度","空气质量"])
data_week_JX = pd.DataFrame(columns=["地区","时间","天气","温度","风向","风级"])
for i in range(0,11):
    dic = get_url(url[i])
    data1 = get_data(dic)
    result1=seven_days(url[i])
    data2 = seven_days_data(result1["7d"],dic)
    
    data_today_JX = data_today_JX.append(data1)
    data_week_JX = data_week_JX.append(data2)
    data_today_JX = data_today_JX.reset_index(drop=True)   #当天数据
    data_week_JX = data_week_JX.reset_index(drop=True)     #未来七天数据


data_today_CN = pd.DataFrame(columns=["地区","时间","温度","风向","风级","降水量",
                                "相对湿度","空气质量"])
data_week_CN = pd.DataFrame(columns=["地区","时间","天气","温度","风向","风级"])
for i in range(0,31):
    dic = get_url(url[i])
    data1 = get_data(dic)
    result1=seven_days(url[i])
    data2 = seven_days_data(result1["7d"],dic)
    
    data_today_CN = data_today_CN.append(data1)
    data_week_CN = data_week_CN.append(data2)
    data_today_CN = data_today_CN.reset_index(drop=True)   #当天数据
    data_week_CN = data_week_CN.reset_index(drop=True)     #未来七天数据

data_today_CN["时间"]=data_today_CN["时间"]+"h"
data_today_JX["时间"]=data_today_JX["时间"]+"h"
