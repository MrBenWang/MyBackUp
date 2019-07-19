#!/usr/bin/env python3
# coding: utf-8

import requests
import time
import re
import os
import json

current_dir = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "q_photos_info")
if not os.path.exists(current_dir):
    os.makedirs(current_dir)
# 只能用账号 密码登录。不能扫码
user = input('输入QQ名:')
pwd = input('输入密码:')

headers = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
    'Referer':
    'https://qzone.qq.com/',
    'Host':
    'user.qzone.qq.com'
}


def login():
    from selenium import webdriver  # 调用这个模块
    driver = webdriver.Chrome(executable_path="C:\\Wzl\\chromedriver.exe")
    driver.get("https://user.qzone.qq.com/")  # 获取qq登录界面
    driver.switch_to_frame('login_frame')
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_id('u').send_keys(user)
    driver.find_element_by_id('p').send_keys(pwd)
    driver.find_element_by_id('login_button').click()
    time.sleep(4)

    # 获取 cookie
    cookies = driver.get_cookies()
    realCookie = {}
    for elem in cookies:
        realCookie[elem['name']] = elem['value']
    # 获得 g_tk
    g_tk = get_g_tk(realCookie)

    # session 缓存
    session = requests.session()
    c = requests.utils.cookiejar_from_dict(
        realCookie, cookiejar=None, overwrite=True)
    session.headers = headers
    session.cookies.update(c)
    driver.close()
    get_images_json(session, g_tk)


# 这个函数用来解决腾讯g_tk加密算法的函数
def get_g_tk(cookies):
    hashes = 5381
    for letter in cookies['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff


# 获取所有图片的json信息
def get_images_json(session, tmp_g_tk):
    download_album_info(session, tmp_g_tk)
    album_list = analysis_album_json()

    for index, value in enumerate(album_list):
        download_photos_info(session, tmp_g_tk, value["id"], value["name"],
                             index)
    analysis_photos_json()


# 下载相册信息
def download_album_info(session, tmp_g_tk):
    url_album = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/fcg_list_album_v3?g_tk={g_tk}&callback=shine0_Callback&t=308388048&hostUin={user}&uin={user}&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&format=jsonp&notice=0&filter=1&handset=4&pageNumModeSort=40&pageNumModeClass=15&needUserInfo=1&idcNum=4&callbackFun=shine0&_=1563442131597"
    tmp_url = url_album.format(user=user, g_tk=tmp_g_tk)
    response = session.get(tmp_url)
    f_name = current_dir + "00-album.json"
    text = response.text
    with open(f_name, 'w+', encoding="utf-8") as __f:
        __f.write(text[16:-2])  # 去掉 jsonp： shine0_Callback( jsonstring );


# 解析 相册信息
def analysis_album_json():
    file_path = current_dir + "00-album.json"
    with open(file_path, 'r', encoding="utf-8") as f:
        file_content = f.read()

    ret_album_list = []
    albumListModeClass = json.loads(file_content)["data"]["albumListModeClass"]
    for _albumListMode in albumListModeClass:
        albumList = _albumListMode["albumList"]
        for _album in albumList:
            ret_album_list.append({"name": _album["name"], "id": _album["id"]})

    return ret_album_list


# 下载所有相册中 相片的信息
def download_photos_info(session, tmp_g_tk, album_id, album_name, album_index):
    dir_name = "{0:0>2d}-{1}".format(album_index, album_name)
    if not os.path.exists(current_dir + dir_name):  # 创建对应的相册文件夹
        os.makedirs(current_dir + dir_name)

    url_photos = "https://h5.qzone.qq.com/proxy/domain/photo.qzone.qq.com/fcgi-bin/cgi_list_photo?g_tk={g_tk}&callback=shine0_Callback&t=413608232&mode=0&idcNum=4&hostUin={user}&topicId={topicId}&noTopic=0&uin={user}&pageStart={pageStart}&pageNum={pageNum}&skipCmtCount=0&singleurl=1&batchId=&notice=0&appid=4&inCharset=utf-8&outCharset=utf-8&source=qzone&plat=qzone&outstyle=json&format=jsonp&json_esc=1&question=&answer=&callbackFun=shine0&_=1563442713415"
    tmp_url = url_photos.format(
        user=user, pageStart=0, pageNum=999, topicId=album_id,
        g_tk=tmp_g_tk)  # 每个相册可以直接获取非常大的数据
    response = session.get(tmp_url)
    f_name = current_dir + "{0}/{0}".format(dir_name)
    text = response.text
    with open(f_name, 'w+', encoding="utf-8") as __f:
        __f.write(text[16:-2])  # 去掉 jsonp： shine0_Callback( jsonstring );


# 解析相片信息
def analysis_photos_json():
    f_list = os.listdir(current_dir)
    for _single_f in f_list:
        dir_path = os.path.join(current_dir, _single_f)
        if not os.path.isdir(dir_path):
            continue  #跳过非文件夹

        if os.path.splitext(_single_f)[1] == "":  # 没有后缀
            file_path = os.path.join(dir_path, _single_f)
            with open(file_path, 'r', encoding="utf-8") as f:
                file_content = f.read()

            photoList = json.loads(file_content)["data"]["photoList"]
            if not photoList:
                continue  # 空相册

            photo_src_name = []
            for _photo in photoList:
                _photo_name = _photo["name"] + "_"  # 相片的名字
                if _photo["rawshoottime"] == 0:  # 是否是原图
                    _photo_name += "0_"
                else:
                    _photo_name += time_to_string(_photo["rawshoottime"]) + "_"

                _photo_name += time_to_string(
                    _photo["uploadtime"]) + ".jpg"  # 如果未知则用 imghdr 来判断图片类型

                _src = _photo["raw"] or _photo["url"]  # 相片的路径，如果有原图用原图
                photo_src_name.append({"src": _src, "name": _photo_name})

            f_name = os.path.join(dir_path, _single_f + ".list")
            with open(f_name, 'w+', encoding="utf-8") as __f:
                __f.write(json.dumps(photo_src_name))


def time_to_string(_datetime):
    timeStruct = time.strptime(_datetime, "%Y-%m-%d %H:%M:%S")
    return time.strftime("%Y%m%d%H%M%S", timeStruct)


def download_photos():
    from threading import Thread
    from concurrent.futures import ThreadPoolExecutor
    #from 20181212-many-files-download import download_files #数字开头的py文件导入有问题
    _download_module = __import__("20181212-many-files-download")

    _thread_pool = ThreadPoolExecutor(5)  #开启线程池
    f_list = os.listdir(current_dir)
    for _single_f in f_list:
        dir_path = os.path.join(current_dir, _single_f)
        if not os.path.isdir(dir_path):
            continue  #跳过非文件夹

        file_path = os.path.join(dir_path, _single_f + ".list")
        if not os.path.isfile(file_path):
            continue  # 不是 list后缀 跳过

        with open(file_path, 'r', encoding="utf-8") as f:
            file_content = json.loads(f.read())

        _thread_pool.submit(_download_module.download_files, file_content,
                            dir_path)


def testprint(name):
    time.sleep(3)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + ":" + name)


if __name__ == "__main__":
    #analysis_photos_json()
    #login()  # 下载json内容
    download_photos()
