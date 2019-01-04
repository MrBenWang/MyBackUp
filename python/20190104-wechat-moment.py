import requests
import os
import json
import time
"""
使用 心书-微信书 它的微信抓取功能：https://weixinshu.com/
在 web 上面，抓取数据
"""

current_dir = os.path.dirname(os.path.realpath(__file__))
json_dir = current_dir + "/moment_jsons/"
img_dir = current_dir + "/moment_imgs/"

headers = {
    "Host":
    "weixinshu.com",
    "Connection":
    "keep-alive",
    "Authorization":
    "",  # 改成自己的
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    "Accept":
    "application/json, text/plain, */*",
    "Accept-Encoding":
    "gzip, deflate, br",
    "Accept-Language":
    "zh-CN,zh-TW;q=0.9,zh;q=0.8",
    "Referer":
    "https://weixinshu.com/books/",  # 改成自己的
    "Cookie":
    ""  # 改成自己的
}

mymonthes = json.loads(
    '{"2016": {"months": [1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]}, "2017": {"months": [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]}, "2018": {"months": [1, 5, 7, 8, 9, 10, 11, 12]}, "2019": {"months": [1]}, "2014": {"months": [4, 5, 6, 7, 8, 9, 10, 11, 12]}, "2015": {"months": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]}}'
)  # 这个也要自己的月份列表


def getAllJsonByMonth():
    _all_monthes = []
    for _year in mymonthes:
        for _month in mymonthes[_year]["months"]:
            _all_monthes.append("{year}{month:0>2d}".format(
                year=_year, month=_month))

    url = "https://weixinshu.com/api/book/1734243/month/{month}?book_type=wxbook&author=wzlblair@100"
    session = requests.session()
    session.headers = headers
    for _month in _all_monthes:
        response = session.get(url.format(month=_month))
        with open(json_dir + _month + ".json", 'w', encoding="utf-8") as __f:
            __f.write(response.text)


# 解析 json
def analysis_json():
    f_list = os.listdir(json_dir)
    _index = 0
    with open(
            current_dir + "/wechat-moment.html", "w", encoding="utf-8") as _f:
        _f.write(
            "<html><title>微信备份</title><style>td{font-size:12px}img{margin-left:20px;width:50px;height:50px}span{font-weight:bold}.content{color:#1100fd;width:800px;font-size:14px}.time{width:180px}.rereply{margin-left:40px}</style><body>"
        )
        for _month in f_list:
            file_content = ""
            with open(json_dir + _month, 'r', encoding="utf-8") as _f_json:
                file_content = _f_json.read()
                msglist = json.loads(file_content)
                retList = shuoshuo_template(msglist, _month)
                _f.write("".join(retList))
        _f.write("</body></html>")


def shuoshuo_template(_json, _month):
    _msg_list = {}
    for _index in _json:
        for _element in _index["elements"]:
            if _element["msg_id"] not in _msg_list:
                _msg_list[_element["msg_id"]] = {}
            if _element["type"] == "label":  # 时间
                _msg_list[_element["msg_id"]]["create_time"] = time.strftime(
                    "%Y-%m-%d %H:%M:%S", time.localtime(_element["content"]))
                _msg_list[_element["msg_id"]]["id"] = time.strftime(
                    "%Y%m%d%H%M%S", time.localtime(_element["content"]))
            elif _element["type"] == "text":  # 文本内容
                _moment_text = ""
                for _txt in _element["content"]:
                    _moment_text += _txt["text"]

                if "text" not in _msg_list[_element["msg_id"]]:  # 为了处理字数太多换行
                    _msg_list[_element["msg_id"]]["text"] = ""
                _msg_list[_element["msg_id"]]["text"] += _moment_text
            elif _element["type"] == "image":  # 图片
                if "images" not in _msg_list[_element["msg_id"]]:  # 会有多个图片
                    _msg_list[_element["msg_id"]]["images"] = []

                _img_count = len(_msg_list[_element["msg_id"]]["images"])
                _img_name = "{0}_{1}.jpg".format(
                    _msg_list[_element["msg_id"]]["id"], _img_count)
                download_image(_element["content"], _img_name)

                _msg_list[_element["msg_id"]]["images"].append(_img_name)
            elif _element["type"] == "qrcode":  # 小视频
                _video_name = _msg_list[_element["msg_id"]]["id"] + ".mp4"
                download_image(_element["content"], _video_name)
                _msg_list[_element["msg_id"]]["video"] = _video_name

    retstring = []
    retstring.append(
        "<hr /><div style='font-size:18px;color: #e927e9;font-weight: 900;'>年月 {0} 内容：</div><table border='1'>"
        .format(_month))
    for _index in _msg_list:
        _msg = _msg_list[_index]
        retstring.append("<tr><td>时间：{0}</td><td class='content'>".format(
            _msg["create_time"]))
        if "text" in _msg:
            retstring.append(_msg["text"])
        if "images" in _msg:
            retstring.append("<br />")
            for _img in _msg["images"]:
                retstring.append("<img src='./moment_imgs/" + _img + "' />")
        if "video" in _msg:
            retstring.append("<video src='./moment_imgs/" + _msg["video"] +
                             "' controls='controls'/>")
        retstring.append("</td></tr>")
    retstring.append("</table>")
    return retstring


def download_image(img_url, img_name):
    return
    response = requests.get(img_url)
    with open(img_dir + img_name, 'wb') as __f:
        __f.write(response.content)


if __name__ == "__main__":
    if not os.path.exists(json_dir):
        os.makedirs(json_dir)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    analysis_json()
