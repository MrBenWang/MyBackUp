#!/usr/bin/env python3
#coding: utf-8

import requests
import time
import re
import os
"""
https://blog.csdn.net/qq_41861526/article/details/80194266

"""

cookie_path = os.path.dirname(os.path.realpath(__file__)) + "\\cookies.txt"
# 只能用账号 密码登录。不能扫码
user = input('输入QQ名:')
pwd = input('输入密码:')

headers = {
    'authority':
    'user.qzone.qq.com',
    'method':
    'GET',
    'scheme':
    'https',
    'accept':
    'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding':
    'gzip, deflate, br',
    'accept-language':
    'zh-CN,zh;q=0.9',
    'cache-control':
    'max-age=1',
    'user-agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
}


def login():
    from selenium import webdriver  # 调用这个模块
    driver = webdriver.Chrome(executable_path="D:\\Wzl\\chromedriver.exe")
    driver.get("https://user.qzone.qq.com/")  # 获取qq登录界面
    driver.switch_to_frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').send_keys(user)
    driver.find_element_by_id('p').send_keys(pwd)
    driver.find_element_by_id('login_button').click()
    time.sleep(4)

    # 生产 qzonetoken
    html = driver.page_source
    xpat = r'window\.g_qzonetoken = \(function\(\)\{ try{return \"(.*)";'
    qzonetoken = re.compile(xpat).findall(html)[0]
    # 获取 cookie
    cookies = driver.get_cookies()
    realCookie = {}
    for elem in cookies:
        realCookie[elem['name']] = elem['value']
    #获得 g_tk
    g_tk = get_g_tk(realCookie)

    # session 缓存
    session = requests.session()
    c = requests.utils.cookiejar_from_dict(
        realCookie, cookiejar=None, overwrite=True)
    session.headers = headers
    session.cookies.update(c)
    driver.close()
    get_shuoshuo_message(session, g_tk, qzonetoken)


# 实际的获取过程
def get_shuoshuo_message(session, tmp_g_tk, tmp_qzonetoken):
    url_json = "https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={user}&inCharset=utf-8&outCharset=utf-8&hostUin={user}&notice=0&sort=0&pos={pos}&num=20&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={g_tk}&qzonetoken={qzonetoken}"
    for _index in range(20):  # qq说说的分页数，每页20个
        tmp_url = url_json.format(
            user=user,
            pos=_index * 20,
            g_tk=tmp_g_tk,
            qzonetoken=tmp_qzonetoken)
        response = session.get(tmp_url)
        f_name = "D:/q_shuoshuo/{:0>2d}.json".format(_index)
        text = response.text
        with open(f_name, 'w+', encoding="utf-8") as __f:
            __f.write(text[10:-2])  # 去掉 jsonp： _Callback( jsonstring );


# 这个函数用来解决腾讯g_tk加密算法的函数
def get_g_tk(cookies):
    hashes = 5381
    for letter in cookies['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff


if __name__ == "__main__":
    login()
