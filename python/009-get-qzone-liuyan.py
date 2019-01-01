import requests
from selenium import webdriver
import time
import os
import re
import json
from selenium.webdriver.chrome.options import Options
URL = 'https://user.qzone.qq.com/'
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
user = input('输入QQ名:')
pwd = input('输入密码:')


##过滤HTML中的标签
#将HTML中标签等信息去掉
#@param htmlstr HTML字符串.
def filter_tags(htmlstr):
    #先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  #匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>',
                           re.I)  #Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>',
                          re.I)  #style
    re_br = re.compile('<br\s*?/?>')  #处理换行
    re_h = re.compile('</?\w+[^>]*>')  #HTML标签
    re_comment = re.compile('<!--[^>]*-->')  #HTML注释
    s = re_cdata.sub('', htmlstr)  #去掉CDATA
    s = re_script.sub('', s)  #去掉SCRIPT
    s = re_style.sub('', s)  #去掉style
    s = re_br.sub('\n', s)  #将br转换为换行
    s = re_h.sub('', s)  #去掉HTML 标签
    s = re_comment.sub('', s)  #去掉HTML注释
    #去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replaceCharEntity(s)  #替换实体
    return s


##替换常用HTML字符实体.
#使用正常的字符替换HTML中特殊的字符实体.
#你可以添加新的实体字符到CHAR_ENTITIES中,处理更多HTML字符实体.
#@param htmlstr HTML字符串.
def replaceCharEntity(htmlstr):
    CHAR_ENTITIES = {
        'nbsp': ' ',
        '160': ' ',
        'lt': '<',
        '60': '<',
        'gt': '>',
        '62': '>',
        'amp': '&',
        '38': '&',
        'quot': '"',
        '34': '"',
    }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(htmlstr)
    while sz:
        entity = sz.group()  #entity全称，如&gt;
        key = sz.group('name')  #去除&;后entity,如&gt;为gt
        try:
            htmlstr = re_charEntity.sub(CHAR_ENTITIES[key], htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
        except KeyError:
            #以空串代替
            htmlstr = re_charEntity.sub('', htmlstr, 1)
            sz = re_charEntity.search(htmlstr)
    return htmlstr


def repalce(s, re_exp, repl_string):
    return re_exp.sub(repl_string, s)


# res = requests.get(URL,headers=headers)
# print(res.text)
def get_g_tk(cookie):
    hashes = 5381
    for letter in cookie['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff


def back_session(realCookie):
    session = requests.session()
    c = requests.utils.cookiejar_from_dict(
        realCookie, cookiejar=None, overwrite=True)
    session.headers = headers
    session.cookies.update(c)
    return session


def get_allQQ(mysession, g_tk, qzonetoken):
    # 获取好友QQ的网址
    url_friend = 'https://user.qzone.qq.com/proxy/domain/r.qzone.qq.com/cgi-bin/tfriend/friend_ship_manager.cgi?' \
                 'uin=' + user + '&do=1&fupdate=1&clean=1&g_tk=' + str(g_tk) + '&qzonetoken=' + qzonetoken

    friendIdpat = '"uin":(.*?),'
    friendNamepat = '"name":(.*?),'
    resp = mysession.get(url_friend)
    friendIdlist = re.compile(friendIdpat).findall(resp.text)
    friendNameList = re.compile(friendNamepat).findall(resp.text)
    nvs = zip(friendNameList, friendIdlist)
    nvDict = dict((name, value) for name, value in nvs)
    time.sleep(3)
    return nvDict


def saveWords(session, gtk, token, start=0, limit=10):
    print('当前下载第%d页数据' % (start / 10 + 1))
    url = 'https://user.qzone.qq.com/proxy/domain/m.qzone.qq.com' \
          '/cgi-bin/new/get_msgb?uin=%s&hostUin=%s&start=%s' \
          '&s=0.1698142305644994&format=jsonp&%s=10&inCharset=utf-8' \
          '&outCharset=utf-8&g_tk=%s&qzonetoken=%s&g_tk=%s' % (user, user, start, limit, gtk, token, gtk)
    res = session.get(url)
    text = res.text
    text = text[10:-3]
    j = json.loads(text)
    total = j['data']['total']

    with open("D:/q_shuoshuo/liuyan.txt", 'a', encoding='UTF-8') as f:
        if start == 0:
            f.write('总共有%s条留言\n' % total)
        f.write('当前下载第%d页数据\n' % (start / 10 + 1))
        for value in j['data']['commentList']:
            cont = str(value['pubtime']) + ' ' + str(value['uin']) + '-' + str(
                value['nickname']) + ':' + str(value['htmlContent']) + '\n'
            f.write(filter_tags(cont))

    if start >= total:
        return
    start = start + 10
    saveWords(session, gtk, token, start)


def begin():
    driver = webdriver.Chrome(executable_path="D:\\Wzl\\chromedriver.exe")
    driver.get(URL)
    driver.switch_to_frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').send_keys(user)
    driver.find_element_by_id('p').send_keys(pwd)
    driver.find_element_by_id('login_button').click()
    time.sleep(4)
    html = driver.page_source
    xpat = r'window\.g_qzonetoken = \(function\(\)\{ try{return \"(.*)";'
    qzonetoken = re.compile(xpat).findall(html)[0]
    cookies = driver.get_cookies()
    realCookie = {}
    print(cookies)
    for elem in cookies:
        realCookie[elem['name']] = elem['value']
    g_tk = get_g_tk(realCookie)
    session = back_session(realCookie)
    driver.close()
    print(g_tk, realCookie, session.cookies)
    friend_list = get_allQQ(session, g_tk, qzonetoken)
    print(friend_list)
    saveWords(session, g_tk, qzonetoken)


begin()
