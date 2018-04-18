# Download the dingrong wiki, and tranfer to a pdf file!
# For off-line reading.

import requests
import pdfkit
import os
import time
from bs4 import BeautifulSoup

url = "http://192.168.1.105"
UA = ''.join(("Mozilla/5.0 (Windows NT 6.3; WOW64) ",
              "AppleWebKit/537.36 (KHTML, like Gecko) ",
              "Chrome/49.0.2623.13 Safari/537.36"))

global myrequest
myrequest = None
header = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4,zh-TW;q=0.2',
    'Connection': 'keep-alive',
    'Host': '192.168.1.105',
    'User-Agent': UA,
    'Referer': 'http://192.168.1.105/login.action',
}

html_template = """
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


class dr_wikipage(object):

    myrequest = None

    def login_wiki_retUrls(self):
        """
            登录
        """
        self.myrequest = requests.Session()
        postData = {'os_username': 'wzl',
                    'os_password': '123',
                    'login': '登录'}

        self.myrequest.post(url + "/dologin.action",
                            data=postData, headers=header)
        return self.analysis_tree('851970')

    def analysis_tree(self, treeId):
        f_request = self.myrequest
        _url = ''.join((url,
                        '/plugins/pagetree/naturalchildren.action?',
                        'decorator=none&excerpt=false&sort=position&',
                        'reverse=false&disableLinks=false&hasRoot=true&',
                        ('pageId=%s&treeId=0&startDepth=0' % (
                            treeId))))
        myreponse = f_request.get(_url, headers=header)
        html_doc = myreponse.content.decode("utf8")
        soup = BeautifulSoup(html_doc, "html5lib")
        all_a = soup.select("a")
        urls = []
        tmpurl = None
        for single_a in all_a:
            myhref = single_a.get('href')
            if myhref == " ":  # 有子节点的
                myid = single_a.get("id")[9:-2]
                tmpurl = self.analysis_tree(myid)
                urls.extend(tmpurl)
            else:
                tmpurl = url + single_a.get('href')
                urls.append(tmpurl)
        return urls

    def parse_url_to_html(self, url):
        response = self.myrequest.get(url)
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
        html = html_template.format(content=html)
        return html

    def to_pdf(self):
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
        for index, url in enumerate(self.login_wiki_retUrls()):
            f_name = "".join(["./swap_html/", str(index), ".html"])
            with open(f_name, 'w', encoding='utf8') as f:
                f.write(self.parse_url_to_html(url))
                file_names.append(f_name)

        pdfkit.from_file(file_names, "知识库.pdf", options=options)
        for html in file_names:
            os.remove(html)
        total_time = time.time() - start
        print(u"总共耗时：%f 秒" % total_time)


dr_wikipage().to_pdf()
