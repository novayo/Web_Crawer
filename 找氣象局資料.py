'''    建鋒請改這裡    '''
start_time = "2016-01-01" # 輸入起始時間
end_time   = "2017-12-31" # 輸入結束時間

# 輸入網址，記得把後面的時間改掉
url = "http://e-service.cwb.gov.tw/HistoryDataQuery/DayDataController.do?command=viewMain&station=C0K530&stname=%25E8%2587%25BA%25E8%25A5%25BF&datepicker="

# 輸入想預設的資料夾名稱（限英文）
dir_name = "Data"
#######################################



##### 程式開始 #####
import urllib.request
import re, os, csv, time


##### 先建立方資料的資料夾 #####
path = os.getcwd() + "/" + dir_name
if not os.path.isdir(path):
    os.mkdir(path)


# 固定的所需的欄位（https://i.imgur.com/1iXaiji.png）
data = [["ObsTime", "StnPres", "SeaPres", "Temperature", "Td dew point", "RH", "WS", "WD", "WSGust", "WDGust", "Precp", "PrecpHour", "SunShine", "GloblRad", "Visb", "UVI", "Cloud Amount"]]
start_time_in_s = time.mktime(time.strptime(start_time,'%Y-%m-%d')) # 將起始時間轉成時間戳（1970年為起點）
end_time_in_s   = time.mktime(time.strptime(end_time,'%Y-%m-%d'))   # 將結束時間轉成時間戳（1970年為起點）


##### 開始爬蟲 #####
while(start_time_in_s <= end_time_in_s):
    # 將時間戳轉回"2018-09-01" 這種形式（網址跟檔名都用得到）
    tmp = time.localtime(start_time_in_s)
    time_in_str = str(tmp.tm_year) + "-" + ("" if tmp.tm_mon>9 else "0") + str(tmp.tm_mon) + "-" + ("" if tmp.tm_mday>9 else "0") + str(tmp.tm_mday)

    # 爬網站拿到html
    new_url = url + time_in_str
    content = urllib.request.urlopen(new_url)
    html_str = content.read().decode("utf-8")

     # 拿到 測站 的名字（檔名需要）
    pattarn = '<tr>[\s\S]*</tr>'
    result = re.findall(pattarn, html_str)
    name_of_file = result[0].split(":")[1].split("&")[0]
    
    # 拿到 資料 的html，下面做分析
    pattarn = '<tbody>[\s\S]*?</tbody>'
    result = re.findall(pattarn, html_str) 
    
    # 分析html，拿到表格資料
    tmp_list = []
    data_partition = result[0].split('<td')
    for i in range(1, len(data_partition)):
        tmp_par = data_partition[i].split(">")[1].split("<")[0].split("&")[0]
        tmp_list.append(tmp_par)
        # 取17為一循環是因為一列總共有17個，之後再換下一行
        if i%17 == 0:
            tmp_list.append(tmp_par)
            data.append(tmp_list)
            tmp_list = []
    
    
    ##### 寫資料進去CSV #####
    f = open(path + "/" + name_of_file + "-" + time_in_str + ".csv", "w", encoding = 'utf_8_sig')  #寫檔案
    writer = csv.writer(f)
    for i in range(0, len(data)):
        writer.writerow(data[i])
    f.close()
    
    
    ##### 繼續下一天 #####
    start_time_in_s = start_time_in_s + 86400.0 # 往後加一天
    del data[1:] # 1是留下第25行的資料
    print("已完成" + time_in_str + "的查詢")