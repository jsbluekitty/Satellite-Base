from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.select import Select
import requests
import time
import re
import pandas as pd
import csv
import numpy as np
import os

# select选项
def select(y):
    s = Select(driver.find_element_by_xpath('//*[@id="ctl00_cph1_ddlYear"]'))
    year = 2021 - int(y)
    s.select_by_index(year)
# checkbox选项
def check():
    c = driver.find_element_by_xpath('//*[@id="ctl00_cph1_chkEO"]')
    c.click()
# submit选项1
def submit():
    sb = driver.find_element_by_xpath('//*[@id="ctl00_cph1_btnNameSearch"]')
    sb.click()
def click1():
    c1=driver.find_element_by_xpath('// *[ @ id = "ctl00_cph1_GridView1"] / tbody / tr[22] / td / table / tbody / tr / td[2] / a')
# 爬取卫星编号
def get():
    for i in range(2, 22):
        list = []
        for a in range(1, 7):
            xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr' + str([i]) + '/td' + str([a])
            content = driver.find_elements_by_xpath(xpath)
            for u in content:
                x = u.text
                if x != '':
                    list.append(x)
                else:
                    pass
        if list == []:
            exit()
        print(list)
        with open(csv_file1, "a+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(list)

def get_inf():
    for i in range(2, 22):
        inf_list = []
        driver.find_element_by_xpath('//*[@id="ctl00_cph1_GridView1"]/tbody/tr' + str([i]) + '/td[2]')
        inf.click()
        time.sleep(2)
        # 进入详情界面爬
        for l in range(1, 4):
            inf_path = '//*[@id="aspnetForm"]/table/tbody/tr[3]/td[1]/table[2]/tbody/tr/td[1]/div/table[3]/tbody/tr' + str([l]) + '/td[2]'
            inf_content = driver.find_elements_by_xpath(inf_path)
            for f in inf_content:
                z = f.text
                if z != '':
                    inf_list.append(z)
                else:
                    pass
        print(inf_list)
        driver.back()
        with open(csv_file2, "a+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(inf_list)

def get_inf2():
    no_list = []
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr' + str([i]) + '/td[1]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            no = u.text
            # print(no)
            no_list.append(no)
    for q in no_list:
        inf_url =  "https://heavens-above.com/SatInfo.aspx?satid=" + str(q) + "&lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT"
        driver.get(inf_url)
        inf_list = []
        for l in range(1, 4):
            inf_path = '//*[@id="aspnetForm"]/table/tbody/tr[3]/td[1]/table[2]/tbody/tr/td[1]/div/table[3]/tbody/tr' + str([l]) + '/td[2]'
            inf_content = driver.find_elements_by_xpath(inf_path)
            for f in inf_content:
                z = f.text
                if z != '':
                    z = z.replace("\n","").replace('\r','')
                    z = z.strip(',')
                    inf_list.append(z)
                elif z == '':
                    print('检测到一个秃子')
                    inf_list.append(z)
        print(inf_list)
        driver.back()
        with open(csv_file2, "a+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(inf_list)

def do_it(mode):
    pag = 1
    if mode == 1:
        csv_file = csv_file1
        row_name = ['卫星编号', '名称', '运行状态', '审定名', '空间飞行器目录名称', '轨道']
    elif mode == 2:
        csv_file = csv_file2
        row_name = ['日期', '发射场', '发射用火箭']
    with open(csv_file, "a+", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(row_name)
    while taget_page > pag:
        for n in range(2, taget_page):
            print(f'===开始爬取第{str(pag)}页===')
            if mode == 1:
                get()
            elif mode == 2:
                get_inf2()
            else:
                print('mlgb你他妈有病？')
            pag += 1
            #page = driver.find_element_by_xpath('//*[@id="ctl00_cph1_GridView1"]/tbody/tr[22]/td/table/tbody/tr/td' + str([n]))
            js = "__doPostBack('ctl00$cph1$GridView1','Page$"+ str(n)+"')"
            driver.execute_script(js)
            if taget_page < pag:
                break
            #page.click()

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径
        print("---  创建新文件夹成功  ---")
    else:
        print('---  文件夹已存在，请检查  ---')

option = webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
#driver = webdriver.Chrome()
driver.get('https://heavens-above.com/Satellites.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT')  # 打开网页
time.sleep(5)
i = 2
yr = input('年份：')
mkdir("./data/"+yr)
csv_file1 = "./data/"+yr+"/test1.txt"  # 保存数据文件名
csv_file2 = "./data/"+yr+"/test2.txt"
csv_file3 = "./data/"+yr+"/test3.txt"
select(yr)
check()
submit()
taget_page = int(input('请输入目标页数:')) + 1
do_it(1)




