from selenium import webdriver
from lxml import etree
from selenium.webdriver.support.select import Select
import requests
import time
import re
import pandas as pd
import csv
import numpy as np
option=webdriver.ChromeOptions()
option.add_argument('headless')
driver = webdriver.Chrome(chrome_options=option)
#driver = webdriver.Chrome()
driver.get('https://heavens-above.com/Satellites.aspx?lat=0&lng=0&loc=Unspecified&alt=0&tz=UCT') #打开网页
time.sleep(5)  #加载等待
i = 2
csv_file = "./test.txt"  # 保存数据文件名
no_list = []
nam_list = []
sta_list = []
rn_list = []
sn_list = []
ob_list = []
list = []
# select选项
def select(y):
    s = Select(driver.find_element_by_xpath('//*[@id="ctl00_cph1_ddlYear"]'))
    year = 2021 - y
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
def num():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr' + str([i]) + '/td[1]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            no = u.text
            # print(no)
            no_list.append(no)
    print(no_list)
# 爬取名称
def names():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr'+ str([i]) +'/td[2]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            nam = u.text
            # print(nam)
            nam_list.append(nam)
    print(nam_list)
# 爬取状态
def state():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr'+ str([i]) +'/td[3]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            sta = u.text
            # print(nam)
            sta_list.append(sta)
    print(sta_list)
# 爬取审定名
def real_name():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr'+ str([i]) +'/td[4]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            rnm = u.text
            # print(nam)
            rn_list.append(rnm)
    print(rn_list)
#
def space_name():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr'+ str([i]) +'/td[5]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            snm = u.text
            # print(nam)
            sn_list.append(snm)
    print(sn_list)
#
def orbits():
    for i in range(2,22):
        xpath = '//*[@id="ctl00_cph1_GridView1"]/tbody/tr'+ str([i]) +'/td[6]'
        content = driver.find_elements_by_xpath(xpath)
        for u in content:
            orb = u.text
            # print(nam)
            ob_list.append(orb)
    print(ob_list)

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
        print(list)
        with open(csv_file, "a+", encoding="utf-8", newline="") as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow(list)
def get_inf():
    inf_list = []
    inf = driver.find_element_by_xpath('//*[@id="ctl00_cph1_GridView1"]/tbody/tr' + str([i]) + '/td[2]')
    inf.click()
    for l in range(1, 4):
        inf_path = '//*[@id="aspnetForm"]/table/tbody/tr[3]/td[1]/table[2]/tbody/tr/td[1]/div/table[3]/tbody/tr' + str(
            [l]) + '/td[2]'
        inf_content = driver.find_elements_by_xpath(inf_path)
        for f in inf_content:
            z = f.text
            if z != '':
                inf_list.append(z)
            else:
                pass
    driver.back()

if __name__ == '__main__':
    select(2020)
    check()
    submit()
    pag = 1
    m = 2
    taget_page = int(input('请输入目标页数:')) + 1
    with open(csv_file, "a+", encoding="utf-8", newline="") as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(['卫星编号', '名称', '运行状态', '审定名', '空间飞行器目录名称', '轨道', '日期', '发射场', '发射用火箭'])
    while taget_page > pag:
        for n in range(m, 12):
            get()
            print(f'===已爬取第{str(pag)}页===')
            pag += 1
            page = driver.find_element_by_xpath('//*[@id="ctl00_cph1_GridView1"]/tbody/tr[22]/td/table/tbody/tr/td' + str([n]))
            page.click()
            if taget_page <= pag:
                break
        m += 1
        if taget_page <= pag:
            break
#//*[@id="ctl00_cph1_GridView1"]/tbody/tr[2]/td[2]
#//*[@id="ctl00_cph1_GridView1"]/tbody/tr[21]/td[2]