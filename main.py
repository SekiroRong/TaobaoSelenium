# -*- coding = utf-8 -*-
# @Time : 1/2/2021 11:00
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

# 刷新页面
# browser.refresh()
def slider_kill(browser):
    try:
        sour = browser.find_element_by_id("nc_1_n1z")  # 获取滑块
        ele = browser.find_element_by_id("nc_1__scale_text")  # 获取整个滑块框
        if sour:
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
        print("不存在滑块")
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
    button = browser.find_element_by_class_name("sn-login")
    button.click()
    time.sleep(0.5)

    myindex = browser.find_element_by_id("J_loginIframe")  # 处理内嵌的网页链接
    browser.get(myindex.get_attribute("src"))
    username = browser.find_element_by_id("fm-login-id")
    username.send_keys("17798533596")
    time.sleep(0.1)
    cipher = browser.find_element_by_id("fm-login-password")
    cipher.send_keys("spidertest123")
    time.sleep(0.1)
    button = browser.find_element_by_class_name("fm-btn")
    button.click()
    slider_kill(browser)
    print("登录完成")
    time.sleep(30)
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
    start_time = '2021-02-01 19:59:59'
    timeArray = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
    now = time_server()
    print(now)
    url = "https://chaoshi.detail.tmall.com/item.htm?spm=a3204.17709488.5400028360.2.1985c6c0P7dSLo&id=20739895092&from_scene=B2C"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    browser = webdriver.Chrome(options=options)
    #browser.maximize_window()
    wait = WebDriverWait(browser, 10)

    browser.get(url)
    time.sleep(1)
    login(browser)
    time.sleep(5)
    #print(browser.page_source)
    # time.sleep(1)
    # browser.refresh()
    # time.sleep(0.5)
    # purchase(browser)
    #
    browser.refresh()
    time.sleep(5)
    #print(browser.page_source)
    i = 0
    start = 1
    while start:
        # 判断时间服务器时间是否大于或等于输入的时间
        if time_server() >= timeArray:
            start = 0
    print("开始抢购")
    while True:
        try:
            button = browser.find_element_by_id("J_LinkBasket")
            button.click()
            print("尝试加入购物车")
            weight = browser.find_element_by_xpath('.//a[@class="tm-mcWeightTotal"]/strong')
            print("Weight="+weight.text)
            if (weight.text != '0'):
                print("加入购物车成功")
                button = browser.find_element_by_class_name("sn-cart-link")
                button.click()
                print("进入购物车")
                slider_kill(browser)
                try:
                    tjdd = wait.until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'cart-checkbox')))
                    tjdd.click()
                    print("全选购物车")
                    button = browser.find_element_by_class_name("btn-area")
                    time.sleep(1)
                    button.click()
                    print("结算")
                    slider_kill(browser)
                    try:
                        button = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                        button.click()
                        print("付款")
                        slider_kill(browser)
                    except:
                        browser.refresh()
                        print("付款失败")
                        try:
                            button = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                            button.click()
                            print("付款")
                            slider_kill(browser)
                        except:
                            browser.refresh()
                            print("付款失败")
                            try:
                                button = wait.until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                button.click()
                                print("付款")
                                slider_kill(browser)
                            except:
                                print("抢购失败")
                                break
                except:
                    browser.refresh()
                    print("结算失败")
                    try:
                        tjdd = wait.until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'cart-checkbox')))
                        tjdd.click()
                        print("全选购物车")
                        time.sleep(1)
                        button = browser.find_element_by_class_name("btn-area")
                        button.click()
                        print("结算")
                        slider_kill(browser)
                        try:
                            button = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                            button.click()
                            print("付款")
                            slider_kill(browser)
                        except:
                            browser.refresh()
                            print("付款失败")
                            try:
                                button = wait.until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                button.click()
                                print("付款")
                                slider_kill(browser)
                            except:
                                browser.refresh()
                                print("付款失败")
                                try:
                                    button = wait.until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                    button.click()
                                    print("付款")
                                    slider_kill(browser)
                                except:
                                    print("抢购失败")
                                    break
                    except:
                        browser.refresh()
                        print("结算失败")
                        try:
                            tjdd = wait.until(
                                EC.presence_of_element_located((By.CLASS_NAME, 'cart-checkbox')))
                            tjdd.click()
                            print("全选购物车")
                            time.sleep(1)
                            button = browser.find_element_by_class_name("btn-area")
                            button.click()
                            print("结算")
                            slider_kill(browser)
                            try:
                                button = wait.until(
                                    EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                button.click()
                                print("付款")
                                slider_kill(browser)
                            except:
                                browser.refresh()
                                print("付款失败")
                                try:
                                    button = wait.until(
                                        EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                    button.click()
                                    print("付款")
                                    slider_kill(browser)
                                except:
                                    browser.refresh()
                                    print("付款失败")
                                    try:
                                        button = wait.until(
                                            EC.presence_of_element_located((By.CLASS_NAME, 'go-btn')))
                                        button.click()
                                        print("付款")
                                        slider_kill(browser)
                                    except:
                                        print("抢购失败")
                                        break
                        except:
                            print("抢购失败")
                            break
            else:
                button = browser.find_element_by_id("J_LinkBasket")
                button.click()
                print("尝试加入购物车")
                time.sleep(0.2)
        except:
            print("找不到购物车")
            browser.refresh()
            slider_kill(browser)
            continue
    time.sleep(500)
    browser.close()




if __name__ == '__main__':
    # for i in range(0,5):
    #     main(i)
    main()