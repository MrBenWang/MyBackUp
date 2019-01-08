#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'long'

import json
import os

"""
本文代码修改自 ： 

《微信好友大揭秘，使用Python抓取朋友圈数据，通过人脸识别全面分析好友，一起看透你的“朋友圈”》
http://blog.51cto.com/12402007/2178703
"""
# 导入itchat模块，操作微信个人号的接口
import itchat

current_dir = os.path.dirname(os.path.realpath(__file__))
friends_data=current_dir + "/pythonfriends.txt"

# 获取数据
def get_data():
    # 扫描二维码登陆微信，实际上就是通过网页版微信登陆
    itchat.auto_login()
    # 获取所有好友信息
    friends = itchat.get_friends(update=True)  # 返回一个包含用户信息字典的列表
    return friends


# 处理数据
def parse_data(data):
    friends = []
    for item in data[1:]:  # 第一个元素是自己，排除掉
        friend = {
            'NickName': item['NickName'],  # 昵称
            'RemarkName': item['RemarkName'],  # 备注名
            'Sex': item['Sex'],  # 性别：1男，2女，0未设置
            'Province': item['Province'],  # 省份
            'City': item['City'],  # 城市
            'Signature': item['Signature'].replace('\n', ' ').replace(
                ',', ' '),  # 个性签名（处理签名内容换行的情况）
            'StarFriend': item['StarFriend'],  # 星标好友：1是，0否
            'ContactFlag': item[
                'ContactFlag']  # 好友类型及权限：1和3好友，259和33027不让他看我的朋友圈，65539不看他的朋友圈，65795两项设置全禁止
        }
        friends.append(friend)
    return friends

# 存储数据，存储到文本文件
def save_to_txt():
    friends = parse_data(get_data())
    for item in friends:
        with open(friends_data, mode='a', encoding='utf-8') as f:
            f.write('%s,%s,%d,%s,%s,%s,%d,%d\n' % (
                item['NickName'], item['RemarkName'], item['Sex'], item['Province'], item['City'], item['Signature'],
                item['StarFriend'], item['ContactFlag']))


def show_sex():
    # 导入Pie组件，用于生成饼图
    # pip3 install pyecharts
    # 
    from pyecharts import Pie

    # 获取所有性别
    sex = []
    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            sex.append(row.split(',')[2])

    # 统计每个性别的数量
    attr = ['帅哥', '美女', '未知']
    value = [sex.count('1'), sex.count('2'), sex.count('0')]

    pie = Pie('好友性别比例', '好友总人数：%d' % len(sex), title_pos='center')
    pie.add('', attr, value, radius=[30, 75], rosetype='area', is_label_show=True,
            is_legend_show=True, legend_top='bottom')
    #pie.show_config()
    pie.render(current_dir+'/好友性别比例.html') 



# 数据可视化
def render():
    # 获取所有城市
    """ 安装地图文件包
pip install echarts-china-provinces-pypkg # 中国省、市、县、区地图
pip install echarts-china-cities-pypkg
pip install echarts-china-counties-pypkg
pip install echarts-china-misc-pypkg 
pip install echarts-countries-pypkg # 全球国家地图
pip install echarts-united-kingdom-pypkg
    """
    # 导入Counter类，用于统计值出现的次数
    from collections import Counter
    # 导入Geo组件，用于生成地理坐标类图
    from pyecharts import Geo
    # 导入Bar组件，用于生成柱状图
    from pyecharts import Bar
    cities = []
    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            city = row.split(',')[4]
            if city != '':  # 去掉城市名为空的值
                cities.append(city)

    # 对城市数据和坐标文件中的地名进行处理
    handle(cities)

    # 统计每个城市出现的次数
    data = Counter(cities).most_common()  # 使用Counter类统计出现的次数，并转换为元组列表

    # 根据城市数据生成地理坐标图
    geo = Geo('好友位置分布', '', title_color='#fff', title_pos='center', width=1200, height=600,
              background_color='#404a59')
    attr, value = geo.cast(data)
    geo.add('', attr, value, visual_range=[0, 100],
            visual_text_color='#fff', symbol_size=15,
            is_visualmap=True, is_piecewise=True)
    geo.render(current_dir+'/好友位置分布.html')

    # 根据城市数据生成柱状图
    data_top20 = Counter(cities).most_common(20)  # 返回出现次数最多的20条
    bar = Bar('好友所在城市TOP20', '', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top20)
    bar.add('', attr, value, is_visualmap=True, visual_text_color='#fff', is_more_utils=True,
            is_label_show=True)
    bar.render(current_dir+'/好友所在城市TOP20.html')

# 处理地名数据，解决坐标文件中找不到地名的问题
def handle(cities):
    # 获取坐标文件中所有地名
    data = None
    _cities_file_path= r'C:\Users\username\AppData\Local\Programs\Python\Python37-32\Lib\site-packages\pyecharts\datasets\city_coordinates.json'
    with open(
            _cities_file_path,
            mode='r', encoding='utf-8') as f:
        data = json.loads(f.read())  # 将str转换为json

    # 循环判断处理
    data_new = data.copy()  # 拷贝所有地名数据
    for city in set(cities):  # 使用set去重
        # 处理地名为空的数据
        if city == '':
            while city in cities:
                cities.remove(city)
        count = 0
        for k in data.keys():
            count += 1
            if k == city:
                break
            if k.startswith(city):  # 处理简写的地名，如 达州市 简写为 达州
                data_new[city] = data[k]
                break
            if k.startswith(city[0:-1]) and len(city) >= 3:  # 处理行政变更的地名，如县改区 或 县改市等
                data_new[city] = data[k]
                break
        # 处理不存在的地名
        if count == len(data):
            while city in cities:
                cities.remove(city)

    # print(len(data), len(data_new))

    # 写入覆盖坐标文件
    with open(_cities_file_path,mode='w', encoding='utf-8') as f:
        f.write(json.dumps(data_new, ensure_ascii=False))  # 将json转换为str

def show_fen_ci_qianmin():
    # ​ jieba是一个基于Python的分词库，完美支持中文分词，功能强大
    import jieba
    # ​ Matplotlib是一个Python的2D绘图库，能够生成高质量的图形，可以快速生成绘图、直方图、功率谱、柱状图、误差图、散点图等
    import matplotlib.pyplot as plt
    # ​ wordcloud是一个基于Python的词云生成类库，可以生成词云图
    # 可能安装失败 https://www.lfd.uci.edu/~gohlke/pythonlibs/#wordcloud
    # python -m pip install wordcloud-1.5.0-cp37-cp37m-win32.whl  
    from wordcloud import WordCloud, STOPWORDS

    # 获取所有个性签名
    signatures = []
    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            signature = row.split(',')[5]
            if signature != '':
                signatures.append(signature)

    # 设置分词
    split = jieba.cut(str(signatures), cut_all=False)  # False精准模式分词、True全模式分词
    words = ' '.join(split)  # 以空格进行拼接
    # print(words)

    # 设置屏蔽词，去除个性签名中的表情、特殊符号等
    stopwords = STOPWORDS.copy()
    stopwords.add('span')
    stopwords.add('class')
    stopwords.add('emoji')
    stopwords.add('emoji1f334')
    stopwords.add('emoji1f388')
    stopwords.add('emoji1f33a')
    stopwords.add('emoji1f33c')
    stopwords.add('emoji1f633')

    # 导入背景图
    bg_image = plt.imread(current_dir+'/20190104-wechat-bg.jpg')

    # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
    wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
                stopwords=stopwords, max_font_size=400, random_state=50)
    # 将分词后数据传入云图
    wc.generate_from_text(words)
    plt.imshow(wc)  # 绘制图像
    plt.axis('off')  # 不显示坐标轴
    # 保存结果到本地
    wc.to_file(current_dir+'/个性签名词云图.jpg')


def show_fen_ci_beizhu():
    # 导入jieba模块，用于中文分词
    import jieba
    # 导入matplotlib，用于生成2D图形
    import matplotlib.pyplot as plt
    # 导入wordcount，用于制作词云图
    from wordcloud import WordCloud, STOPWORDS

    # 获取备注名
    remarkNames = []
    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            remarkName = row.split(',')[1]
            if remarkName != '':
                remarkNames.append(remarkName)

    # 设置分词
    split = jieba.cut(str(remarkNames), cut_all=False)  # False精准模式分词、True全模式分词
    words = ' '.join(split)  # 以空格进行拼接

    # 导入背景图
    bg_image = plt.imread(current_dir+'/20190104-wechat-bg.jpg')

    # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
    wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
                max_font_size=400, random_state=50)
    # 将分词后数据传入云图
    wc.generate_from_text(words)
    plt.imshow(wc)  # 绘制图像
    plt.axis('off')  # 不显示坐标轴
    # 保存结果到本地
    wc.to_file(current_dir+'/备注名词云图.jpg')

def show_fenlei():
    # 导入jieba模块，用于中文分词
    import jieba
    # 导入Counter类，用于统计值出现的次数
    from collections import Counter
    from pyecharts import Bar

    # 获取备注名
    remarkNames = []
    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            remarkName = row.split(',')[1]
            if remarkName != '':
                remarkNames.append(remarkName)

    # 设置分词
    words = [x for x in jieba.cut(str(remarkNames), cut_all=False) if x not in ['-', ',', '(', ')', '（', '）', ' ', "'"]]  # 排除短横线、逗号、空格、单引号
    data_top10 = Counter(words).most_common(10)  # 返回出现次数最多的20条
    print(data_top10)

    bar = Bar('好友分类TOP10', '', title_pos='center', width=1200, height=600)
    attr, value = bar.cast(data_top10)
    bar.add('', attr, value, visual_range=[0, 200], is_visualmap=True, is_label_show=True)
    bar.render(current_dir+'/好友分类TOP10.html')


def show_teshu_friend():
    from pyecharts import Bar

    # 获取特殊好友
    star_list = []  # 星标朋友
    deny_see_list = []  # 不让他看我的朋友圈
    no_see_list = []  # 不看他的朋友圈

    with open(friends_data, mode='r', encoding='utf-8') as f:
        rows = f.readlines()
        for row in rows:
            # # 获取好友名称
            name = row.split(',')[1] if row.split(',')[1] != '' else row.split(',')[0]
            # 获取星标朋友
            star = row.split(',')[6]
            if star == '1':
                star_list.append(name)
            # 获取设置了朋友圈权限的朋友
            flag = row.split(',')[7].replace('\n', '')
            if flag in ['259', '33027', '65795']:
                deny_see_list.append(name)
            if flag in ['65539', '65795']:
                no_see_list.append(name)

    attr = ['星标朋友', '不让他看我的朋友圈', '不看他的朋友圈']
    value = [len(star_list), len(deny_see_list), len(no_see_list)]

    bar = Bar('特殊好友分析', '', title_pos='center')
    bar.add('', attr, value, is_visualmap=True, is_label_show=True)
    bar.render(current_dir+'/特殊好友分析.html')

# 获取数据
def get_touxiang_image():
    itchat.auto_login()
    friends = itchat.get_friends(update=True)

    #  在当前位置创建一个用于存储头像的目录headImages
    base_path = current_dir+'/headImages'
    if not os.path.exists(base_path):
        os.mkdir(base_path)

    # 获取所有好友头像
    for friend in friends:
        img_data = itchat.get_head_img(userName=friend['UserName'])  # 获取头像数据
        img_name = friend['RemarkName'] if friend['RemarkName'] != '' else friend['NickName']
        img_name=validateTitle(img_name)
        img_file = os.path.join(base_path, img_name + '.jpg')
        print(img_file)
        with open(img_file, 'wb') as file:
            file.write(img_data)


# 去除特殊字符，windows不能作为文件名
def validateTitle(title):
    import re
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    new_title = re.sub(rstr, "_", title)  # 替换为下划线
    return new_title



def analyse_touxiang_data():
    # 导入腾讯优图，用来实现人脸检测等功能  https://open.youtu.qq.com
    import TencentYoutuyun
    from pyecharts import Pie
    # 导入jieba模块，用于中文分词
    import jieba
    # 导入matplotlib，用于生成2D图形
    import matplotlib.pyplot as plt
    # 导入wordcount，用于制作词云图
    from wordcloud import WordCloud, STOPWORDS
    # 向腾讯优图平台申请的开发密钥，此处需要替换为自己的密钥
    appid = "----"
    secret_id = "----"
    secret_key = "----"
    userid = "----" # 你的qq号

    end_point = TencentYoutuyun.conf.API_YOUTU_END_POINT  # 优图开放平台
    youtu = TencentYoutuyun.YouTu(appid, secret_id, secret_key, userid, end_point)

    use_face_man = 0
    use_face_woman = 0
    not_use_face = 0

    base_path = current_dir+'/headImages'
    tag_tpyes = [] # 分词
    for file_name in os.listdir(base_path):
        result = youtu.DetectFace(os.path.join(base_path, file_name))  # 人脸检测与分析
        # print(result)  # 参考 https://open.youtu.qq.com/legency/#/develop/api-face-analysis-detect
        # 判断是否使用人像
        gender=""
        age=0
        beauty=0
        glasses=""
        if result['errorcode'] == 0:  # errorcode为0表示图片中存在人像
            gender = '男' if result['face'][0]['gender'] >= 50 else '女'
            if gender=="男":
                use_face_man+=1
            else:
                use_face_woman+= 1

            age = result['face'][0]['age']
            beauty = result['face'][0]['beauty']  # 魅力值
            glasses = '不戴眼镜 ' if result['face'][0]['glasses'] == 0 else '戴眼镜'
        else:
            not_use_face += 1

        tag_name=""
        result_type = youtu.imagetag(os.path.join(base_path, file_name))  # 头像分类
        if result_type['errorcode'] == 0 and len(result_type["tags"])>0:
            tag_name=max(result_type["tags"], key=lambda item: item['tag_confidence']) ["tag_name"].encode('ISO-8859-1').decode("utf8")
            tag_tpyes.append(tag_name)

        with open(current_dir+'/header.txt', mode='a', encoding='utf-8') as f:
            f.write('%s,%s,%d,%d,%s,%s\n' % (file_name[:-4], gender, age, beauty, glasses,tag_name))

    attr = ['使用人脸头像-男','使用人脸头像-女', '未使用人脸头像']
    value = [use_face_man,use_face_woman, not_use_face]
    pie = Pie('好友头像分析', '', title_pos='center')
    pie.add('', attr, value, radius=[30, 75], is_label_show=True,
            is_legend_show=True, legend_top='bottom')
    # pie.show_config()
    pie.render(current_dir+'/好友头像分析.html')

    # 设置分词
    split = jieba.cut(str(tag_tpyes), cut_all=False)  # False精准模式分词、True全模式分词
    words = ' '.join(split)  # 以空格进行拼接

    # 导入背景图
    bg_image = plt.imread(current_dir+'/20190104-wechat-bg.jpg')

    # 设置词云参数，参数分别表示：画布宽高、背景颜色、背景图形状、字体、屏蔽词、最大词的字体大小
    wc = WordCloud(width=1024, height=768, background_color='white', mask=bg_image, font_path='STKAITI.TTF',
                max_font_size=400, random_state=50)
    # 将分词后数据传入云图
    wc.generate_from_text(words)
    plt.imshow(wc)  # 绘制图像
    plt.axis('off')  # 不显示坐标轴
    # 保存结果到本地
    wc.to_file(current_dir+'/头像类别.jpg')

def reanalyse_touxiang_from_text():
    from pyecharts import Pie
    use_face_glass_man = 0
    use_face_unglass_man = 0
    use_face_glass_woman = 0
    use_face_unglass_woman = 0
    unuse_face=0
    with open(current_dir+'/header.txt', mode='r', encoding='utf-8') as f:
        rows=f.readlines()
        for row in rows:
            sex = row.split(',')[1]
            glass = row.split(',')[4]
            if sex=="男" and glass=="戴眼镜":
                use_face_glass_man+=1
            elif sex=="男" and glass=="不戴眼镜 ":
                use_face_unglass_man+=1
            elif sex=="女" and glass=="戴眼镜":
                use_face_glass_woman+=1
            elif sex=="女" and glass=="不戴眼镜 ":
                use_face_unglass_woman+=1
            else:
                unuse_face+=1

    attr = ['戴眼镜-男','不戴眼镜-男','戴眼镜-女','不戴眼镜-女', '未使用人脸头像']
    value = [use_face_glass_man,use_face_unglass_man, use_face_glass_woman,use_face_unglass_woman,unuse_face]
    pie = Pie('好友头像分析', '', title_pos='center')
    pie.add('', attr, value, radius=[30, 75], is_label_show=True,
            is_legend_show=True, legend_top='bottom')
    # pie.show_config()
    pie.render(current_dir+'/好友头像分析.html')

# 拼接头像
def join_image():
    import math
    from PIL import Image
    base_path = current_dir+'/headImages'
    files = os.listdir(base_path)
    each_size = int(math.sqrt(float(640 * 640) / len(files)))
    lines = int(640 / each_size)
    image = Image.new('RGB', (640, 640))
    x = 0
    y = 0
    for file_name in files:
        img = Image.open(os.path.join(base_path, file_name))
        img = img.resize((each_size, each_size), Image.ANTIALIAS)
        image.paste(img, (x * each_size, y * each_size))
        x += 1
        if x == lines:
            x = 0
            y += 1
    image.save(current_dir+'/all.jpg')
    #itchat.send_image('all.jpg', 'filehelper')

if __name__ == '__main__':
    # save_to_txt()
    # show_sex()
    # render()
    # show_fen_ci_qianmin()
    # show_fen_ci_beizhu()
    # show_fenlei()
    # show_teshu_friend()
    # get_touxiang_image()
    # analyse_touxiang_data()
    # join_image()
    # reanalyse_touxiang_from_text()