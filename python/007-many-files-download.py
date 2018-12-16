
#!/usr/bin/env python3
#coding: utf-8

import os
import requests

"""
存在一个下载列表，然后需要批量下载
先用js，来获取列表

var retlist=[];
$$("div.desc-info > a").forEach(function(element) {
  element.setAttribute("download",element.innerText);
  retlist.push({"src": element.href,"name": element.innerText});
  console.log("!["+element.innerText+"](/images/0000-find-ths-lost-manhua/"+element.innerText+")\\r\\n");
});

JSON.stringify(retlist);
"""
retlist = [
    {"src": "http://test/asasd.jpg", "name": "01.jpg"},
    {"src": "http://test/asasd.jpg", "name": "02.jpg"},
    {"src": "http://test/asasd.jpg", "name": "03.jpg"}]


def download_files():
    for single in retlist:
        response = requests.get(single["src"])
        f_name = "".join(["D:/wzl/MyBackUp/python/downloads/", single["name"]])
        print(f_name)
        with open(f_name, 'wb') as __f:
            __f.write(response.content)


if __name__ == '__main__':
    download_files()
