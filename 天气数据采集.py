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

#全国城市天气
url = []
for i in range(1,32):
    if (i<10):
        if (i<5):
            url.append("http://www.weather.com.cn/weather/101"+"0"+str(i)+"0100.shtml")
        else:
            for j in range(1,15):
                if (j<10):
                    url.append("http://www.weather.com.cn/weather/101"+"0"+str(i)+"0"+str(j)+"01.shtml")           
                else:
                    url.append("http://www.weather.com.cn/weather/101"+"0"+str(i)+str(j)+"01.shtml")
        
    else:
        for j in range(1,15):
            if (j<10):
                url.append("http://www.weather.com.cn/weather/101"+str(i)+"0"+str(j)+"01.shtml")           
            else:
                url.append("http://www.weather.com.cn/weather/101"+str(i)+str(j)+"01.shtml")

data_today_all = pd.DataFrame(columns=["地区","时间","温度","风向","风级","降水量",
                                "相对湿度","空气质量"])
data_week_all = pd.DataFrame(columns=["地区","时间","天气","温度","风向","风级"])
num=1
for i in range(0,len(url)):
    #判断当前网页能否访问
    dic = get_url(url[i])
    if (dic==-1):
        continue
    data1 = get_data(dic)
    result1=seven_days(url[i])
    data2 = seven_days_data(result1["7d"],dic)
    
    data_today_all = data_today_all.append(data1)
    data_week_all = data_week_all.append(data2)
    print("第%d个城市"%num)
    num = num+1
data_today_all = data_today_all.reset_index(drop=True)   #当天数据
data_week_all = data_week_all.reset_index(drop=True)     #未来七天数据

from pyecharts import Map, Geo
# 世界地图数据
value = [95.1, 23.2, 43.3, 66.4, 88.5]
attr= ["China", "Canada", "Brazil", "Russia", "United States"]

# 省和直辖市
province_distribution = {'河南': 45.23, '北京': 37.56, '河北': 21, '辽宁': 12, '江西': 6, '上海': 20, '安徽': 10, '江苏': 16, '湖南': 9, '浙江': 13, '海南': 2, '广东': 22, '湖北': 8, '黑龙江': 11, '澳门': 1, '陕西': 11, '四川': 7, '内蒙古': 3, '重庆': 3, '云南': 6, '贵州': 2, '吉林': 3, '山西': 12, '山东': 11, '福建': 4, '青海': 1, '舵主科技，质量保证': 1, '天津': 1, '其他': 1}
provice=list(province_distribution.keys())
values=list(province_distribution.values())

#全国主要城市温度热力图
data = data_today_CN[["地区","温度"]].groupby("地区").min().reset_index()
region = data["地区"].values
temp = data["温度"].values
list_data = []
for i in range(len(region)):
    list_tup = []
    list_tup.append(region[i])
    list_tup.append(temp[i])
    list_tup = tuple(list_tup)
    list_data.append(list_tup)
data = list_data

attr, value = Geo.cast(data)

geo = Geo("全国主要城市温度热力图", title_color="#fff", title_pos="center", width=1500, height=750, background_color='#404a59')

geo.add("温度热力图", attr, value, visual_range=[0, 35], type='heatmap',visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
geo.show_config()
geo.render(path="C:/Users/22524/Desktop/全国主要城市温度热力图.html")

# 空气质量评分
data = data_today_CN.groupby("地区")["空气质量"].mean().reset_index()
indexs = data["地区"].values
values = data["空气质量"].values


geo = Geo("全国主要城市空气质量评分", title_color="#fff", title_pos="center", width=1500, height=750, background_color='#404a59')

# type="effectScatter", is_random=True, effect_scale=5  使点具有发散性
geo.add("空气质量评分", indexs, values, type="effectScatter", is_random=True, effect_scale=5, visual_range=[0, 100],visual_text_color="#fff", symbol_size=15, is_visualmap=True, is_roam=False)
geo.show_config()
geo.render(path="C:/Users/22524/Desktop/全国主要城市空气质量评分.html")

import plotly
import plotly.graph_objects as go
import plotly.io as pio
import psutil
import plotly.offline

#当天的温度等的变化情况
def today_line(city):
    #折线图
    line0 = go.Scatter(x=data_today_CN[data_today_CN["地区"]==city]["时间"],
                       y=data_today_CN[data_today_CN["地区"]==city]["温度"],
                       name="温度",
                       mode = 'lines+markers'
                      )
    line1 = go.Scatter(x=data_today_CN[data_today_CN["地区"]==city]["时间"],
                       y=data_today_CN[data_today_CN["地区"]==city]["相对湿度"],
                       name="相对湿度",
                       mode = 'lines+markers'
                      )
    line2 = go.Scatter(x=data_today_CN[data_today_CN["地区"]==city]["时间"],
                       y=data_today_CN[data_today_CN["地区"]==city]["空气质量"],
                       name="空气质量",
                       mode = 'lines+markers'
                      )
    line3 = go.Scatter(x=data_today_CN[data_today_CN["地区"]==city]["时间"],
                       y=data_today_CN[data_today_CN["地区"]==city]["降水量"],
                       name="降水量",
                       mode = 'lines+markers'
                      )
    fig = go.Figure([line0,line1,line2,line3])
    fig.update_layout(
        title = "温度,相对湿度，空气质量，降水量变化情况"+"("+city+")",
        xaxis_title = "时间",
        yaxis_title = "数值"
    )
    #将图像写入html文件中
    plotly.offline.plot(fig,filename='C:/Users/22524/Desktop/当天/'+city+'_1.html')
    #fig.show()
#未来七天的温度变化情况
def seven_future(city):
    data = data_week_CN.copy()
    data["温度"] = data["温度"].apply(lambda x: x[:-1])
    line = go.Scatter(x=data[data["地区"]==city]["时间"],
                       y=data[data["地区"]==city]["温度"],
                       name="温度",
                       mode = 'lines+markers'
                      )
    fig = go.Figure(line)
    fig.update_layout(
        title = "温度变化情况"+"("+city+")",
        xaxis_title = "时间",
        yaxis_title = "温度"
    )
    #将图像写入html文件中
    plotly.offline.plot(fig,filename='C:/Users/22524/Desktop/未来七天/'+city+'_7.html')
    #fig.show()

# 将各个城市的图像写入html
city_list = list(data_today_CN["地区"].unique())
for city in city_list:
    today_line(city)
    seven_future(city)
    
#历史天气爬取
list_city = ["beijing","shanghai","tianjin","chongqing","haerbin","changchun",
 "shenyang","huhehaote","shijiazhuang","taiyuan","xian","jinan","wulumuqi",
 "lasa","xining","lanzhou","yinchuan","zhengzhou","nanjing","wuhan","hangzhou",
 "hefei","fuzhou","nanchang","changsha","guiyang","chengdu","guangzhou","kunming",
 "nanning","haikou"]
list_city1 = ['北京', '上海', '天津', '重庆', '哈尔滨', '长春', '沈阳', '呼和浩特', '石家庄', '太原',
       '西安', '济南', '乌鲁木齐', '拉萨', '西宁', '兰州', '银川', '郑州', '南京', '武汉', '杭州',
       '合肥', '福州', '南昌', '长沙', '贵阳', '成都', '广州', '昆明', '南宁', '海口']

def get_result(url):
    r1 = requests.get(url)
    r1.encoding = r1.apparent_encoding
    if r1.status_code!=200:
        return -1
    soup = BeautifulSoup(r1.text, 'html.parser')

    all_days = []

    for tr in soup.find('table').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            tda = tds[0].find_all('a')
            if len(tda) >= 1:
                r_content="http://www.tianqihoubao.com/lishi/(.*)/month.*"
                zero = re.compile(r_content).findall(url)[0]
                one = tda[0].string
                two = tds[1].string
                three = tds[2].string
                four = tds[3].string
                one = one.replace('\r\n', "")
                one = one.replace(' ', "")
                two = two.replace('\r\n', "")
                two = two.replace(' ', "")
                three = three.replace('\r\n', "")
                three = three.replace(' ', "")
                four = four.replace('\r\n', "")
                four = four.replace(' ', "")
                all_days.append([zero,one, two, three, four])
    return all_days
#提取出最高温度最低温度
def deal_data(data):
    data["温度"] = data["温度"].apply(lambda x: x.split("/"))
    data["最高温度"] = data["温度"].apply(lambda x: x[0])
    data["最低温度"] = data["温度"].apply(lambda x: x[1])
    data["最高温度"] = data["最高温度"].apply(lambda x: x.replace("℃",""))
    data["最低温度"] = data["最低温度"].apply(lambda x: x.replace("℃",""))
    data["地区"].replace(to_replace=list_city,value=list_city1,inplace=True)
    del data["温度"]
    
    return data
date = []
weather = []
temp = []
url = []
for city in list_city:
    for year in range(2011,2020):
        for month in range(1,13):
            if month<10:
                url.append("http://www.tianqihoubao.com/lishi/"+city+"/"+"month/"+str(year)+"0"+str(month)+".html")
            else:
                url.append("http://www.tianqihoubao.com/lishi/"+city+"/"+"month/"+str(year)+str(month)+".html")     
 
data_history = []
num=1
for i in url:
    list1 = get_result(i)
    if list1==-1:
        continue
    else:
        data_history.extend(list1)
    print(num)
    num=num+1

    #将爬取的数据放入对应列表
region = []
date = []
temp = []
for i in range(0,len(data_history)):
    region.append(data_history[i][0])
    date.append(data_history[i][1])
    temp.append(data_history[i][3])
    
#将上面的列表数据放入dataframe
data = pd.DataFrame(columns=["地区","日期","温度"])
data["地区"] = region
data["日期"] = date
data["温度"] = temp
data = deal_data(data
                 
data.to_csv("C:/Users/22524/Desktop/全国省会历史天气.csv",index=False,
            encoding="utf-8-sig")

                 


