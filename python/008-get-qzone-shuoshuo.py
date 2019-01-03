#!/usr/bin/env python3
# coding: utf-8

import requests
import time
import re
import os
"""
获取说说列表
https://h5.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msglist_v6?uin={user}&inCharset=utf-8&outCharset=utf-8&hostUin={user}&notice=0&sort=0&pos={pos}&num=20&cgi_host=http%3A%2F%2Ftaotao.qq.com%2Fcgi-bin%2Femotion_cgi_msglist_v6&code_version=1&format=jsonp&need_private_comment=1&g_tk={g_tk}&qzonetoken={qzonetoken}

获取说说明细，评论大于10条，才有意义
https://user.qzone.qq.com/proxy/domain/taotao.qq.com/cgi-bin/emotion_cgi_msgdetail_v6?uin={user}&tid=1deb6e0f15904853a6220200&t1_source=undefined&ftype=0&sort=0&pos=0&num=20&g_tk={g_tk}&callback=_preloadCallback&code_version=1&format=jsonp&need_private_comment=1&qzonetoken={qzonetoken}&g_tk={g_tk}
"""

current_dir = os.path.dirname(os.path.realpath(__file__))
# 只能用账号 密码登录。不能扫码
user = input('输入QQ名:')
pwd = input('输入密码:')
total_page = 20  # 去看自己的qq说说 总的分页数

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
    # 获得 g_tk
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
    for _index in range(total_page):  # qq说说的分页数，每页20个
        tmp_url = url_json.format(
            user=user,
            pos=_index * 20,
            g_tk=tmp_g_tk,
            qzonetoken=tmp_qzonetoken)
        response = session.get(tmp_url)
        f_name = current_dir + "/q_shuoshuo/{:0>2d}.json".format(_index)
        text = response.text
        with open(f_name, 'w+', encoding="utf-8") as __f:
            __f.write(text[10:-2])  # 去掉 jsonp： _Callback( jsonstring );


# 这个函数用来解决腾讯g_tk加密算法的函数
def get_g_tk(cookies):
    hashes = 5381
    for letter in cookies['p_skey']:
        hashes += (hashes << 5) + ord(letter)  # ord()是用来返回字符的ascii码
    return hashes & 0x7fffffff


# 解析 json 文件，返回html
def analysis_json():
    import json
    with open(current_dir + "/shuoshuo.html", "w", encoding="utf-8") as _f:
        _f.write(
            "<html><title>我的说说备份</title><style>td{font-size:12px}img{margin-left:20px;width:50px;height:50px}span{font-weight:bold}.content{color:#1100fd;width:800px;font-size:14px}.time{width:180px}.rereply{margin-left:40px}</style><body>"
        )

        f_list = os.listdir(current_dir + "/q_shuoshuo/")
        _index = 0
        for _single_f in f_list:
            file_content = ""
            with open(
                    current_dir + "/q_shuoshuo/" + _single_f,
                    'r',
                    encoding="utf-8") as f:
                file_content = f.read()

            msglist = json.loads(file_content)["msglist"]
            _index += 1
            retList = shuoshuo_template(msglist, _index)
            _f.write("".join(retList))
        _f.write("</body></html>")


# html 模板
def shuoshuo_template(msglist, _index):
    """
msglist[0].tid      内容id ，大于10条的评论时候会用到；
msglist[0].content      内容
msglist[0].created_time      内容 时间戳 需要 转日期  1397779942
msglist[0].pic[0].url3      内容 图片  最大图
msglist[0].lbs.name      内容 发帖地址
msglist[0].source_name      内容 发帖 来自什么手机

msglist[0].rt_con.content      被转发内容
msglist[0].rt_uinname      被转发人
msglist[0].rt_createTime      (被转发内容)的时间

msglist[0].cmtnum       评论数量
msglist[0].commentlist[0].content       评论内容
msglist[0].commentlist[0].createTime2       评论时间 2017-06-01 22:13:40
msglist[0].commentlist[0].name       评论人
msglist[0].commentlist[0].pic[0].hd_url       评论图片

msglist[0].commentlist[0].list_3[0].name       评论回复人
msglist[0].commentlist[0].list_3[0].content       评论回复：@{uin:xx,nick:名字,who:1,auto:1}卧槽
msglist[0].commentlist[0].list_3[0].createTime2       评论回复时间 2017-06-01 22:13:40
    """
    # 创建下载的图片目录
    img_dir = current_dir + "/shuoshuo_images/"
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)

    retstring = []
    retstring.append(
        "<hr /><div style='font-size:18px;color: #e927e9;font-weight: 900;'>第{0}页内容：</div><table border='1'>"
        .format(_index))
    for _msg in msglist:
        # 说说内容
        retstring.append("<tr><td>内容：</td><td class='content' colspan='3'>")
        retstring.append(_msg["content"])

        if "rt_con" in _msg:  # 转发内容
            retstring.append("<br />转发自{author}-[{time}]:{content}".format(
                author=_msg["rt_uinname"],
                time=_msg["rt_createTime"],
                content=_msg["rt_con"]["content"]))

        if "pic" in _msg:  # 图片内容
            retstring.append("<br />")
            _index_pic = 0
            for _s_pic in _msg["pic"]:
                _index_pic += 1
                _img_path = time.strftime("%Y%m%d%H%M%S",
                                          time.localtime(_msg["created_time"])
                                          ) + "{:0>2d}.jpg".format(_index_pic)
                download_image(_s_pic["url2"], img_dir + _img_path)
                retstring.append(
                    "<img src='./shuoshuo_images/{0}' />".format(_img_path))
        retstring.append("</td></tr>")  # 说说内容结束

        # 说说时间，位置等 属性
        retstring.append(
            "<tr><td>时间：</td><td class='time'>{time}</td><td>其他信息：</td><td>地址【{local}】；来自【{phone}】</td></tr>"
            .format(
                time=time.strftime("%Y-%m-%d %H:%M:%S",
                                   time.localtime(_msg["created_time"])),
                local=_msg["lbs"]["name"],
                phone=_msg["source_name"]))

        # 评论
        retstring.append("<tr><td>评论：</td><td colspan='3'>")
        if _msg["cmtnum"] > 0:
            if _msg["cmtnum"] > 10:  # 记录下来，评论大于10的，单独处理
                print("index:{0}, datetime:{1},content:{2}".format(
                    _index, _msg["createTime"], _msg["content"]))

            for _s_comment in _msg["commentlist"]:
                # 一般的评论
                retstring.append(
                    "<div><span>{author}-[{time}]：</span>{content}".format(
                        author=_s_comment["name"],
                        time=_s_comment["createTime2"],
                        content=_s_comment["content"]))
                if "pic" in _s_comment:
                    _index_pic = 0
                    for _s_comm_pic in _s_comment["pic"]:
                        _index_pic += 1
                        __timeStruct = time.strptime(
                            _s_comment["createTime2"],
                            "%Y-%m-%d %H:%M:%S")  # 时间格式转换
                        _img_path = time.strftime(
                            "%Y%m%d%H%M%S",
                            __timeStruct) + "{:0>2d}.jpg".format(_index_pic)
                        download_image(_s_comm_pic["hd_url"],
                                       img_dir + _img_path)
                        retstring.append("<img src='./shuoshuo_images/{0}' />".
                                         format(_img_path))
                retstring.append("</div>")

                # 回复评论的评论
                if "list_3" in _s_comment:
                    for _s_comment_replay in _s_comment["list_3"]:
                        retstring.append(
                            "<div class='rereply'><span>{author}-[{time}]：</span>{content}</div>"
                            .format(
                                author=_s_comment_replay["name"],
                                time=_s_comment_replay["createTime2"],
                                content=_s_comment_replay["content"]))
        retstring.append("</td></tr>")  # 评论结束
    retstring.append("</table>")
    return retstring


def download_image(img_url, img_full_path):
    response = requests.get(img_url)
    with open(img_full_path, 'wb') as __f:
        __f.write(response.content)


if __name__ == "__main__":
    # login()  # 下载json内容
    analysis_json()  # 组织成 html，下载图片
