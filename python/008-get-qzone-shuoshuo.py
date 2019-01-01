#!/usr/bin/env python3
#coding: utf-8

import requests

"""
https://blog.csdn.net/qq_41861526/article/details/80194266

"""

cookie_path=r"C:\Users\asus\Desktop\cookies.txt"
session =requests.session()
user=input('输入登录的qq号:')

def login():
    from selenium import webdriver # 调用这个模块
    driver = webdriver.Firefox()
    driver.get('https://user.qzone.qq.com/') # 获取qq登录界面
    global session # 这里的话，是将session变成全局变量，这样子就能保证整个程序里面sesssion的cookie都是一样
    time.sleep(30) # 这里给30秒，是给时间给你扫码，或者输入时间进行登录，因为selenium是不知道你什么时候输入密码完成的，所以必须要自己去管
    with open(cookie_path, 'w+') as f: # 这里是将得到的cookie进行保存，这样就不用每次启动程序都要登录
        for cookie in driver.get_cookies():
            print(cookie)
            f.write(cookie['name']+'=='+cookie['value']+'\n')
    f.close()

def cookielogin():
    global session # 设置全局变量
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0',
               'Referer': 'https://qzone.qq.com/',
               'Host': 'user.qzone.qq.com'}
    with open(cookie_path, 'r') as f: # 从文本中获取到cookies并且变成可使用的cookies的格式
        ans = f.readlines()
 
    for an in ans:
        an = an.replace('\n', '')
        a = an.split('==')
        cookies[a[0]] = a[1]
    cookies['_qz_referrer'] = 'i.qq.com'
    requests.utils.add_dict_to_cookiejar(session.cookies,cookies) # 这里就是将cookie和session绑定在一起
    r=session.get('https://user.qzone.qq.com/%s/infocenter'%(user),headers=headers,verify=False)

    if not re.findall('QQ空间-分享生活，留住感动',r.text): # 判断是否有这个，来判断是否登录成功
        return True
    else:
        return False



if __name__=="__main__":
    if not cookielogin():
        login()
