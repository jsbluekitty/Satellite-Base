# coding=utf-8
import requests
from lxml import etree
import time
import os
import csv
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import utils
requests.packages.urllib3.disable_warnings()
csv_file = "./result.csv"  # 保存数据文件名
page = 10  # 总页数
headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Content-Type': 'application/x-www-form-urlencoded',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36'
}
# 获取列表
def get_content(current):
    postData = {
            '__EVENTTARGET': 'ctl00$cph1$GridView1',
            '__EVENTARGUMENT': 'Page$' + str(current),
            '__LASTFOCUS':'',
            '__VIEWSTATE': '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',
            '__VIEWSTATEGENERATOR': 'ADEE68B6',
            '__VIEWSTATEENCRYPTED':'',
            'utcOffset': '0',
            'ctl00$ddlCulture': 'zh',
            'ctl00$cph1$txtName': '*',
            'ctl00$cph1$ddlYear': '2020',
            'ctl00$cph1$txtStartSatID': '1',
            'ctl00$cph1$txtEndSatID': '99999',
            'ctl00$cph1$chkEO': 'off'
        }
    url = "https://heavens-above.com/Satellites.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT"
    html = requests.post(url, data=postData,headers=headers, verify=False)
    print(type(html))
    root = etree.HTML(html.text)
    line = 0
    for r in root.xpath('//table[@class="standardTable"]/tr'):
        if line > 0 and line < len(root.xpath('//table[@class="standardTable"]/tr')) - 1:
            no = r.xpath('./td[1]/text()')[0]
            name = r.xpath('./td[2]/span/a/text()')[0]
            name_url = "https://heavens-above.com/" + r.xpath('./td[2]/span/a/@href')[0]
            state = r.xpath('./td[3]/span/text()')[0]
            verify_name = r.xpath('./td[4]/span/text()')[0]
            fly_name = r.xpath('./td[5]/text()')[0]
            track = r.xpath('./td[6]/span/a/text()')[0]
            track_url = "https://heavens-above.com/" + r.xpath('./td[6]/span/a/@href')[0]
            time.sleep(2)
            html_name = requests.get(name_url, headers=headers,timeout=20)
            root_name = etree.HTML(html_name.text)
            utc_time = root_name.xpath('//table[3]/tr[1]/td[2]/span/text()')[0]
            launch_site	= "".join(root_name.xpath('//table[3]/span[1]/tr/td[2]//text()'))
            launch = root_name.xpath('//table[3]/span[2]/tr/td[2]//text()')[0]
            # 保存数据
            with open(csv_file, "a+", encoding="utf-8-sig", newline="") as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([no, name, state, verify_name, fly_name, track, utc_time, launch_site, launch])
            print(f"============卫星编号【{no}】=============")
            time.sleep(2)
            get_pic(track_url, no)
        line += 1

# 获取图片链接
def get_pic(url, no):
    html = requests.get(url, headers=headers, verify=False,timeout=20)
    root = etree.HTML(html.text)
    for r in root.xpath('//table[2]/tr'):
        for d in r.xpath('./td'):
            pic_name = "".join(d.xpath('./text()')).replace("\r\n", "")
            url_pic = "http:" + d.xpath('./img/@src')[0]
            try:
                path_file = "./" + str(no)
                os.mkdir(path_file)
            except:
                pass
            # 下载图片
            print(f"============下载卫星编号【{no}】图片=============")
            with open(path_file + "/" + str(pic_name) + ".jpg", "wb") as f:
                img = requests.get(url_pic, headers=headers,timeout=20).content
                f.write(img)

if __name__ == '__main__':
    with open(csv_file, "a+", encoding="utf-8-sig", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['卫星编号', '名称', '运行状态', '审定名', '空间飞行器目录名称', '轨道', '日期',
                             '发射场', '发射用火箭'])
    for i in range(1, page + 1):
        print(f"============第【{i}】页=============")
        get_content(i)
