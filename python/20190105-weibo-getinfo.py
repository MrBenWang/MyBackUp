#!/usr/bin/env python3
#coding: utf-8

import requests
import os
import io
import json
from datetime import datetime

current_dir = os.path.dirname(os.path.realpath(__file__))
img_dir = current_dir + "/weibo_imgs/"
json_dir = current_dir + "/weibo_jsons/"
# 定义要爬取的微博的微博ID
weibo_id = "微博ID"
containerid = "微博内容id"


#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid():
    data = requests.get(
        "https://m.weibo.cn/api/container/getIndex?type=uid&value=" + weibo_id)
    _json_data = json.loads(data.content)
    if _json_data["ok"] != 1:
        raise Exception("get containerid error!!!!!")

    content = _json_data.get("data")
    for data in content.get("tabsInfo").get("tabs"):
        if (data.get("tab_type") == "weibo"):
            containerid = data.get("containerid")
            break
    return containerid


#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo():
    with open(current_dir + "/my_weibo.html", "w", encoding="utf-8") as _f:
        _f.write(
            "<html><title>我的sina微博备份</title><style>td{font-size:12px}img{margin-left:20px;width:50px;height:50px}span{font-weight:bold}.content{color:#1100fd;width:800px;font-size:14px}.time{width:180px}.rereply{margin-left:40px}</style><body>"
        )
        get_weibo_by_page(containerid, _f)
        _f.write("</body></html>")


# 把json文件保存在本地
def get_weibo_to_json():
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    _get_index = 0
    while True:
        _get_index += 1
        weibo_url = "https://m.weibo.cn/api/container/getIndex?type=uid&value=" + weibo_id + "&containerid=" + containerid + "&page=" + str(
            _get_index)

        response = requests.get(weibo_url)
        cards = json.loads(response.content).get("data").get("cards")
        if (len(cards) > 0):
            with open(
                    "{0}/{1:0>2d}.json".format(json_dir, _get_index),
                    "w",
                    encoding="utf-8") as _f:
                _f.write(response.text)
        else:
            return


def get_weibo_by_page(containerid, _f):
    f_list = os.listdir(json_dir)
    for _single_f in f_list:

        # 读取缓存的 json 文件
        cards = {}
        with open(os.path.join(json_dir + _single_f),"r",encoding="utf-8") as _read_json:
            cards = json.load(_read_json).get("data").get("cards")
        
        # 解析过程
        if (len(cards) > 0):
            retstring = []
            retstring.append(
                "<hr /><div style='font-size:18px;color: #27e957;font-weight: 900;'>第{0}页内容：</div><table border='1'>"
                .format(_single_f[:-5]))
            for card in cards:
                card_type = card.get("card_type")
                if (card_type == 9):
                    mblog = card.get("mblog")
                    text = mblog.get("text")  # 内容
                    created_at = mblog.get("created_at")  # 时间 2017-07-01 没有分钟
                    bid = mblog.get("bid")  # 时间 2017-07-01 没有分钟

                    retstring.append(
                        "<tr><td>内容：</td><td class='content' colspan='3'><span style='color:#e927e9;'>")
                    retstring.append(text+"</span><br />")
                    pics = mblog.get("pics")  # 大图链接
                    retstring.append(html_pics_string(pics, created_at,bid))

                    retweeted_status = mblog.get(
                        "retweeted_status")  # 判断这条微博 是否是转发的
                    if retweeted_status:
                        retstring.append("<br /><span style='color:red;'>转发：</span><br />" +
                                         retweeted_status.get("text")+"<br />")
                        retweeted_pics = retweeted_status.get("pics")
                        retstring.append(html_pics_string(retweeted_pics, created_at,bid))

                    # 来源-微博时间， 评论数 转发数
                    retstring.append(
                        "<tr><td>时间：</td><td class='time'>{time}</td><td>来自【{source}】：</td><td>点赞数【{attitudes}】；评论数【{comments}】；转发数【{reposts}】</td></tr>"
                        .format(
                            time=created_at,
                            source=mblog.get("source"),
                            attitudes=mblog.get("attitudes_count"),
                            comments=mblog.get("comments_count"),
                            reposts=mblog.get("reposts_count")))
                else:
                    pass
            retstring.append("</table>")
            _f.write("".join(retstring))
        else:
            break


# 返回 图片相关 html ，并下载
def html_pics_string(pics, created_at,bid):
    retstring = []
    if pics:
        __timeStruct = datetime.strptime(created_at, "%Y-%m-%d")  # 时间格式转换
        _index_pic = 0
        for _pic in pics:
            _index_pic += 1
            img_name = "{create}_{bid}_{index}.jpg".format(
                create=created_at,
                bid=bid,
                #now=datetime.now().strftime("%H%M%S%f"),
                index=_index_pic)
            download_image(_pic.get("large").get("url"), img_name)
            retstring.append("<img src='./weibo_imgs/{0}' />".format(img_name))
    return "".join(retstring)


# 下载图片 文件
def download_image(img_url, img_name):
    if os.path.exists(img_dir + img_name):
        return # 图片存在就不下载了

    response = requests.get(img_url)
    with open(img_dir + img_name, 'wb') as __f:
        __f.write(response.content)


if __name__ == "__main__":
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    # get_weibo_to_json()
    get_weibo()