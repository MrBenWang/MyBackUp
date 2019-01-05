#!/usr/bin/env python3
#coding: utf-8

import requests
import os
import io
import json
import time


current_dir = os.path.dirname(os.path.realpath(__file__))
img_dir = current_dir + "/weibo_imgs/"
json_dir = current_dir + "/weibo_jsons/"
# 定义要爬取的微博的微博ID
weibo_id="1791072903"

#获取微博主页的containerid，爬取微博内容时需要此id
def get_containerid():
    data=requests.get("https://m.weibo.cn/api/container/getIndex?type=uid&value="+weibo_id)
    _json_data=json.loads(data.content)
    if _json_data["ok"]!=1:
        raise Exception("get containerid error!!!!!")

    content=_json_data.get("data")
    for data in content.get("tabsInfo").get("tabs"):
        if(data.get("tab_type")=="weibo"):
            containerid=data.get("containerid")
            break
    return containerid

#获取微博内容信息,并保存到文本中，内容包括：每条微博的内容、微博详情页面地址、点赞数、评论数、转发数等
def get_weibo():
    containerid = "1076031791072903" # get_containerid()
    with io.open(current_dir+"/my_weibo.html", "a", encoding="utf-8") as _f:
        #_f.write("<html><title>我的sina微博备份</title><style>td{font-size:12px}img{margin-left:20px;width:50px;height:50px}span{font-weight:bold}.content{color:#1100fd;width:800px;font-size:14px}.time{width:180px}.rereply{margin-left:40px}</style><body>")
        get_weibo_by_page(containerid,_f)
        _f.write("</body></html>")

# 把json文件保存在本地
def get_weibo_to_json():
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    _get_index=0
    while True:
        _get_index+=1
        weibo_url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+weibo_id+"&containerid="+containerid+"&page="+str(_get_index)

        response=requests.get(weibo_url)
        cards=json.loads(response.content).get("data").get("cards")
        if(len(cards)>0):
            with open("{0}/{1:0>2d}.json".format(json_dir,_get_index), "w", encoding="utf-8") as _f:
                _f.write(response.text.encode("utf8"))
        else:
            return

def get_weibo_by_page(containerid,_f):
    _get_index=0
    while True:
        _get_index+=1
        weibo_url="https://m.weibo.cn/api/container/getIndex?type=uid&value="+weibo_id+"&containerid="+containerid+"&page="+str(_get_index)
        try:
            response=requests.get(weibo_url)
            cards=json.loads(response.content).get("data").get("cards")
            if(len(cards)>0):
                retstring=[]
                retstring.append(
        "<hr /><div style='font-size:18px;color: #e927e9;font-weight: 900;'>第{0:0>2d}页内容：</div><table border='1'>"
        .format(_get_index))
                for card in cards:
                    card_type=card.get("card_type")
                    if(card_type==9):
                        mblog=card.get("mblog")
                        text=mblog.get("text") # 内容 
                        created_at=mblog.get("created_at") # 时间 2017-07-01 没有分钟
                        if (not text) or text =="转发微博": # 纯转发的，不要
                            continue
                        
                        retstring.append("<tr><td>内容：</td><td class='content' colspan='3'>")
                        retstring.append(text)
                        pics=mblog.get("pics") # 大图链接 
                        retstring.append(html_pics_string(pics,created_at))

                        retweeted_status=mblog.get("retweeted_status") # 判断这条微博 是否是转发的
                        if retweeted_status:
                            retstring.append("<br />转发：<br />"+retweeted_status.get("text"))
                            retweeted_pics=retweeted_status.get("pics")
                            html_pics_string(retweeted_pics,created_at)

                        # 来源-微博时间， 评论数 转发数
                        retstring.append(
                            "<tr><td>时间：</td><td class='time'>{source}:{time}</td><td>其他信息：</td><td>点赞数【{attitudes}】；评论数【{comments}】；转发数【{reposts}】</td></tr>"
                            .format(
                                time=created_at,
                                source=mblog.get("source"),
                                attitudes=mblog.get("attitudes_count"),
                                comments=mblog.get("comments_count"),
                                reposts=mblog.get("reposts_count")))
                
                retstring.append("</table>")
                _f.write("".join(retstring))
            else:
                break
        except Exception as e:
            print(e)
            pass

# 返回 图片相关 html ，并下载
def html_pics_string(pics,created_at):
    retstring=[]
    if pics:
        __timeStruct = time.strptime(created_at,"%Y-%m-%d")  # 时间格式转换
        _index_pic = 0
        for _pic in pics:
            _index_pic += 1
            img_name="{create}_{now}_{index}.jpg".format(
                create=created_at,
                now=time.strftime("%H%M%S", time.localtime()),
                index=_index_pic)
            download_image(_pic.get("large").get("url"), img_name)
            retstring.append("<img src='./weibo_imgs/{0}' />".
                        format(img_name))
    return "".join(retstring)

# 下载图片 文件
def download_image(img_url, img_name):
    response = requests.get(img_url)
    with open(img_dir+img_name, 'wb') as __f:
        __f.write(response.content)

if __name__=="__main__":
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    #get_weibo()