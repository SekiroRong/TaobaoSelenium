# -*- coding = utf-8 -*-
# @Time : 2/2/2021 19:09
# @Author : 戎昱
# @File : main.py
# @Software : PyCharm
from selenium import webdriver
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import xlwt
import time
import datetime
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import pickle
import os

def slider_kill(browser):
    try:
        sour = browser.find_element_by_id("nc_1_n1z")  # 获取滑块
        ele = browser.find_element_by_id("nc_1__scale_text")  # 获取整个滑块框
        if sour:
            try:
                print("存在滑块")
                print(ele.size, ele.location['x'])

                action = ActionChains(browser)
                action.click_and_hold(on_element=sour).perform()
                print(sour.size)
                print(sour.location['x'])
                time.sleep(0.15)
                ActionChains(browser).move_to_element_with_offset(to_element=sour, xoffset=30, yoffset=0).perform()
                time.sleep(1)
                print(30, sour.location['x'], sour.location['y'])
                ActionChains(browser).move_to_element_wit_offset(to_element=sour, xoffset=100, yoffset=0).perform()
                time.sleep(0.5)
                print(100, sour.location['x'], sour.location['y'])
                ActionChains(browser).move_to_element_with_offset(to_element=sour, xoffset=170, yoffset=0).perform()
                time.sleep(0.3)
                print(170, sour.location['x'], sour.location['y'])
                ActionChains(browser).move_to_element_with_offset(to_element=sour, xoffset=250, yoffset=0).perform()
                time.sleep(0.2)
                print(250, sour.location['x'], sour.location['y'])
                ActionChains(browser).move_to_element_with_offset(to_element=sour, xoffset=290,
                                                                  yoffset=0).release().perform()
                print(290, sour.location['x'], sour.location['y'])
                print("滑块完成")
                # browser.refresh()
                # time.sleep(0.1)
                # slider_kill(browser)
            except:
                print("滑块验证码失败")
                slider_kill(browser)
    except:
        print("不存在滑块验证码")

def time_server():
    # 获取淘宝服务器的时间戳
    r1 = requests.get(url='http://api.m.taobao.com/rest/api3.do?api=mtop.common.getTimestamp',
                      headers={
                          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 UBrowser/6.2.4098.3 Safari/537.36'}
                      ).json()['data']['t']
    # 把时间戳格式/1000 获取毫秒
    timeNum = int(r1) / 1000
    # 格式化时间 (小数点后6为)
    time1 = datetime.fromtimestamp(timeNum)
    print(time1)
    return time1
def login(browser):
    # button = browser.find_element_by_class_name("sn-login")
    # button.click()
    # time.sleep(0.5)
    #
    # myindex = browser.find_element_by_id("J_loginIframe")  # 处理内嵌的网页链接
    # browser.get(myindex.get_attribute("src"))
    username = browser.find_element_by_id("fm-login-id")
    username.send_keys("15850502589")
    time.sleep(0.1)
    cipher = browser.find_element_by_id("fm-login-password")
    cipher.send_keys("rongyu123")
    time.sleep(0.1)
    button = browser.find_element_by_class_name("fm-btn")
    button.click()
    slider_kill(browser)
    print("登录完成")
    #time.sleep(30)
def purchase(browser):
    button = browser.find_element_by_id("J_LinkBasket")
    button.click()
    time.sleep(1)
    # suspend = browser.find_element_by_class_name("tm-mcRoot")# 鼠标悬停
    # ActionChains(browser).move_to_element(suspend).perform()
    # # time.sleep(1)
    # button = browser.find_element_by_class_name("tm-mcCartBtn")
    # button.click()
    # time.sleep(1)
    button = browser.find_element_by_class_name("sn-cart-link")
    button.click()
    time.sleep(1)
    button = browser.find_element_by_class_name("cart-checkbox")
    button.click()
    time.sleep(1)
    button = browser.find_element_by_class_name("btn-area")
    button.click()
    # button = browser.find_element_by_class_name("go-btn")
    # button.click()
def main():
    start_time = '2021-02-03 20:00:00'
    timeArray = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    #now = time_server()
    # print(now)
    url = "https://cart.taobao.com/cart.htm"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=options)
    #browser.maximize_window()
    wait = WebDriverWait(browser, 10)

    browser.get(url)
    time.sleep(1)
    login(browser)
    time.sleep(2)
    #print(browser.page_source)
    # time.sleep(1)
    # browser.refresh()
    # time.sleep(0.5)
    # purchase(browser)
    #
    # browser.refresh()
    # time.sleep(5)
    button = browser.find_element_by_class_name("cart-checkbox")
    button.click()
    print("全选购物车")
    jiesuan = browser.find_element_by_class_name("btn-area")
    #print(browser.page_source)
    i = 0
    start = 1
    while start:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(now)
        # 判断时间服务器时间是否大于或等于输入的时间
        if now >= start_time:
            start = 0
    print("开始抢购")
    # button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cart-checkbox')))
    # button.click()
    # print("全选购物车")
    while True:
        try:
            if (browser.current_url == url):
                print("尝试结算")
                jiesuan.click()
                browser.switch_to.window(browser.window_handles[1])
            # slider_kill(browser)
            else:   # 进入结算界面
                print("进入结算界面")
                slider_kill(browser)
                try:
                    button = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                    button.click()
                    print("付款")
                    #slider_kill(browser)
                    break
                except:
                    browser.refresh()
                    print("付款失败")
                    try:
                        button = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                        button.click()
                        print("付款")
                        break
                        #slider_kill(browser)
                    except:
                        browser.refresh()
                        print("付款失败")
                        try:
                            button = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                            button.click()
                            print("付款")
                            break
                            #slider_kill(browser)
                        except:
                            print("抢购失败")
                            break
        except:
            print("出错了")
            # print("找不到结算")
            # time.sleep(3)
            # slider_kill(browser)
            # button = browser.find_element_by_class_name("cart-checkbox")
            # #button = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cart-checkbox')))
            # button.click()
            # print("全选购物车")
            continue
    print("抢购成功请付款")
    time.sleep(500)
    browser.close()




if __name__ == '__main__':
    # for i in range(0,5):
    #     main(i)
    main()