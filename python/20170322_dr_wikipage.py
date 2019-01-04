#!/usr/bin/env python3
#coding: utf-8

"""
Download the dingrong wiki, and tranfer to a pdf file!
For off-line reading.
"""

import os
import time
import requests
import pdfkit
from bs4 import BeautifulSoup


MY_URL = "http://192.168.1.105"
MY_UA = ''.join((
    "Mozilla/5.0 (Windows NT 6.3; WOW64) ",
    "AppleWebKit/537.36 (KHTML, like Gecko) ",
    "Chrome/49.0.2623.13 Safari/537.36"))

MY_HEAD = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': '192.168.1.105',
    'User-Agent': MY_UA,
    'Referer': 'http://192.168.1.105/login.action',
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
</head>
<body>
{content}
</body>
</html>

"""


class _drWikiPage(object):  # pylint: disable=too-few-public-methods
    """下载 wiki的html页面
    """
    myrequest = None

    def __login_wiki_ret_urls(self):
        """
            登录
        """
        self.myrequest = requests.Session()
        post_data = {
            "os_username": "wzl",
            "os_password": "123",
            "login": "登录"
        }

        self.myrequest.post(MY_URL + "/dologin.action",
                            data=post_data, headers=MY_HEAD)
        return self.__analysis_tree('851970')

    def __analysis_tree(self, __tree_id):
        """分析左侧的树行 链接，并且保存

        Args:
            __tree_id:根据单个的id，来获取访问的html
        """
        f_request = self.myrequest
        _url = ''.join((MY_URL,
                        '/plugins/pagetree/naturalchildren.action?',
                        'decorator=none&excerpt=false&sort=position&',
                        'reverse=false&disableLinks=false&hasRoot=true&',
                        ('pageId=%s&treeId=0&startDepth=0' % (
                            __tree_id))))
        myreponse = f_request.get(_url, headers=MY_HEAD)
        html_doc = myreponse.content.decode("utf8")
        soup = BeautifulSoup(html_doc, "html5lib")
        all_a = soup.select("a")
        urls = []
        tmpurl = None
        for single_a in all_a:
            myhref = single_a.get('href')
            if myhref == " ":  # 有子节点的
                myid = single_a.get("id")[9:-2]
                tmpurl = self.__analysis_tree(myid)
                urls.extend(tmpurl)
            else:
                tmpurl = MY_URL + single_a.get('href')
                urls.append(tmpurl)
        return urls

    def __parse_url_to_html(self, __url):
        """下载html页面

        Args:
            __url:需要下载页面的html
        """
        response = self.myrequest.get(__url)
        soup = BeautifulSoup(response.content.decode("utf-8"), "html5lib")
        body = soup.find_all(class_="wiki-content")[0]

        # 加入标题, 居中显示
        title = soup.find(id="title-text").get_text()
        center_tag = soup.new_tag("center")
        title_tag = soup.new_tag('h1')
        title_tag.string = title
        center_tag.insert(1, title_tag)
        body.insert(1, center_tag)

        html = str(body)
        # body中的img标签的src相对路径的改成绝对路径
        # pattern = "(<img .*?src=\")(.*?)(\")"

        # def func(m):
        #     if not m.group(3).startswith("http"):
        #         rtn = "".join(
        #             [m.group(1), self.domain, m.group(2), m.group(3)])
        #         return rtn
        #     else:
        #         return "".join([m.group(1), m.group(2), m.group(3)])

        # html = re.compile(pattern).sub(func, html)
        html = HTML_TEMPLATE.format(content=html)
        return html

    def to_pdf(self):
        """
        最终转换为pdf
        """
        start = time.time()
        options = {
            'page-size': 'Letter',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ],
            'cookie': [
                ('cookie-name1', 'cookie-value1'),
                ('cookie-name2', 'cookie-value2'),
            ],
            'outline-depth': 10,
        }
        file_names = []
        for index, url in enumerate(self.__login_wiki_ret_urls()):
            f_name = "".join(["./swap_html/", str(index), ".html"])
            with open(f_name, 'w', encoding='utf8') as __f:
                __f.write(self.__parse_url_to_html(url))
                file_names.append(f_name)

        pdfkit.from_file(file_names, "知识库.pdf", options=options)
        for html in file_names:
            os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)


if __name__ == '__main__':
    _drWikiPage().to_pdf()
