#!/usr/bin/env python3
# coding: utf-8
from xml.dom.minidom import parse
import xml.dom.minidom
import glob
import os
import time
import copy
import json


base_path = os.path.dirname(os.path.realpath(__file__))
is_debug = True  # 只执行一次，调试使用的


class EnglishString(object):
    def __init__(self, _key, _value):
        self.key = _key
        self.value = _value
        self.is_translated = False

    def set_template(self, old_string_tmp, ignore_tmp_list, new_string_tmp):
        '''
        设置替换的模板，用于replace
        '''
        self.ignore_list = []
        self.old_string = old_string_tmp.format(key=self.key, value=self.value)
        self.new_string = new_string_tmp.format(key=self.key, value=self.value)

        for __ignore in ignore_tmp_list:
            self.ignore_list.append(__ignore.format(key=self.key, value=self.value))
        return self

    def set_translated(self):
        self.is_translated = True

    def __str__(self):
        return f'{self.key}, {self.value}'


def pretreatment_cs_xaml():
    '''
    预处理项目文件 cs 和 xaml，把代码中的变量，直接替换成字符串
    '''
    xml_path = r"D:\Projects\lmsa-client\lmsa\common\lenovo.themes.generic\lang\en_us.xaml"
    DOMTree = xml.dom.minidom.parse(xml_path)
    _english_strings = DOMTree.getElementsByTagName("sys:String")
    _ret_key_value = []
    for _single in _english_strings:
        _ret_key_value.append(EnglishString(_single.getAttribute("x:Key"), _single.childNodes[0].data))

    _dir = r"D:\Projects\lmsa-client\lmsa"
    untranslated_file = os.path.join(base_path, time.strftime("%Y%m%d%H%M%S-", time.localtime()) + "not_translated_old.json")
    _files_xaml = [f for f in glob.glob(os.path.join(_dir, "**/*.xaml"), recursive=True)]
    _files_cs = [f for f in glob.glob(os.path.join(_dir, "**/*.cs"), recursive=True)]

    # 替换xaml
    _replace_xaml = []
    for _s in _ret_key_value:
        _replace_xaml.append(copy.copy(_s).set_template(
            old_string_tmp='{{DynamicResource {key}}}', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='{value}'))
        _replace_xaml.append(copy.copy(_s).set_template(
            old_string_tmp='{{StaticResource {key}}}', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='{value}'))
    for _file in _files_xaml:  # 替换xaml文件，例：LangText="hello" 换为 LangText="hello" LangKey="K0112"
        replace_change(_file, _replace_xaml)

    # 替换cs文件
    _replace_cs = []
    for _s in _ret_key_value:
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='(string)System.Windows.Application.Current.FindResource("{key}")', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='System.Windows.Application.Current.FindResource("{key}")', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.FindResource("{key}")?.ToString()', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.FindResource("{key}").ToString()', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.FindResource("{key}") as string', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.FindResource("{key}")', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='app.Resources("{key}").ToString()', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.Resources["{key}"]', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='Application.Current.Resources["{key}"].ToString()', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='"{value}"'))
    for _file in _files_cs:  # 替换cs文件，例：Application.Current.FindResource("hello") 换为 "K0112"
        replace_change(_file, _replace_cs)

    # 统计未替换的字符串
    _translated_string = {}
    for x in list(filter(lambda x: x.is_translated, _replace_xaml)):
        _translated_string[x.key] = x.value
    for x in list(filter(lambda x: x.is_translated, _replace_cs)):
        _translated_string[x.key] = x.value

    _untranslated_string = {}
    for x in _ret_key_value:
        if _translated_string.__contains__(x.key):
            continue
        _untranslated_string[x.key] = x.value
    with open(untranslated_file, 'w', encoding="utf-8") as __f:
        json.dump(_untranslated_string, __f)


def check_file_encode_utf(filename):
    '''
    检查文件是否时utf-8，不是则转化为utf-8
    '''
    from chardet import detect
    with open(filename, 'rb') as f:
        rawdata = f.read()
        _encoding_type = detect(rawdata)['encoding'].upper()

    if _encoding_type == "UTF-8" or _encoding_type == "UTF-8-SIG":
        return

    try:
        with open(filename, 'r', encoding=_encoding_type) as f, open(filename+"new", 'w', encoding='utf-8') as target_f:
            text = f.read()  # for small files, for big use chunks
            target_f.write(text)

        os.remove(filename)  # remove old encoding file
        os.rename(filename+"new", filename)  # rename new encoding
        print(filename, "\t", _encoding_type)
    except Exception as error:
        print(f'exception: {filename} \t {_encoding_type} \t {error}')


def read_translate_xml():
    '''
    从xml中，读取已经翻译的key和value
    '''
    xml_path = os.path.join(base_path, "20220105-en-US.xml")
    DOMTree = xml.dom.minidom.parse(xml_path)
    _english_strings = DOMTree.getElementsByTagName("sys:String")
    _ret_key_value = []
    for _single in _english_strings:
        __value = _single.childNodes[0].data.replace("\n", "\\n").replace(r'"', r'\"')
        _ret_key_value.append(EnglishString(_single.getAttribute("x:Key"), __value))
    return _ret_key_value


def replace_english_to_key():
    _translate_map = read_translate_xml()

    _dir = r"D:\Projects\lmsa-client\lmsa"
    _files_cs = [f for f in glob.glob(os.path.join(_dir, "**/*.cs"), recursive=True)]
    _files_xaml = [f for f in glob.glob(os.path.join(_dir, "**/*.xaml"), recursive=True)]
    untranslated_file = os.path.join(base_path, time.strftime("%Y%m%d%H%M%S-", time.localtime()) + "not_translated.json")

    # # 替换xaml
    # _replace_xaml = []
    # for _s in _translate_map:
    #     _replace_xaml.append(copy.copy(_s).set_template(
    #         old_string_tmp='LangText="{value}"', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='LangText="{value}" LangKey="{key}"'))
    #     _replace_xaml.append(copy.copy(_s).set_template(
    #         old_string_tmp='Content="{value}"', ignore_tmp_list=['LangKey="{key}"'], new_string_tmp='Content="{value}" LangKey="{key}"'))
    # for _file in _files_xaml:  # 替换xaml文件，例：LangText="hello" 换为 LangText="hello" LangKey="K0112"
    #     replace_change(_file, _replace_xaml)

    # 替换cs文件
    _replace_cs = []
    for _s in _translate_map:
        _replace_cs.append(copy.copy(_s).set_template(
            old_string_tmp='"{value}"', ignore_tmp_list=['Register("{value}"', '"{key}"/*"{value}"*/'], new_string_tmp='"{key}"/*"{value}"*/'))
    _files_cs = []
    _files_cs.append(r'D:\Projects\lmsa-client\lmsa\plugins\phoneManager\ViewModels\ConnectingViewModel.cs')
    for _file in _files_cs:  # 替换cs文件，例："hello" 换为 "K0112"/*"hello"*/
        replace_change(_file, _replace_cs)
    return
    # 统计未替换的字符串
    _translated_string = {}  # 已翻译的字符串
    for x in list(filter(lambda x: x.is_translated, _replace_xaml)):
        _translated_string[x.key] = x.value
    for x in list(filter(lambda x: x.is_translated, _replace_cs)):
        _translated_string[x.key] = x.value
    _new_translate_map = {}
    for x in _translate_map:
        _new_translate_map[x.key] = x.value

    _untranslated_string = {}
    for x in _new_translate_map.keys():
        if _translated_string.__contains__(x):
            continue
        _untranslated_string[x] = _new_translate_map[x]
    with open(untranslated_file, 'w', encoding="utf-8") as __f:
        json.dump(_untranslated_string, __f)


def replace_change(filename: str, _english_key_value: list):
    '''
    执行替换文件翻译，
    如果文件中，同时存在 new_key 和 old_string, 则认为已经替换，不再执行。并且记录在未替换文件中
    如果文件中，仅仅存在 old_string 则执行替换
    '''
    _content = ""
    is_translated = False
    with open(filename, 'r', encoding='utf-8') as __f:
        _content = __f.read()
        for __s in _english_key_value:
            if __s.old_string not in _content:
                continue  # old_string 不存在不替换
            else:
                _is_ignore = False
                for __ignore in __s.ignore_list:
                    if __ignore in _content:
                        _is_ignore = True
                        break
                if _is_ignore:
                    continue  # 同时存在 ignore_list 不替换
                else:
                    is_translated = True
                    __s.set_translated()
                    _content = _content.replace(__s.old_string, __s.new_string)

    if is_translated:
        with open(filename, 'w', encoding='utf-8') as __f:
            __f.write(_content)


# 字符串是软件的内容，不能翻译，需要排除的文件
'''
特殊字符串 "www.lenovo.com/privacy/"
code, type, 属性名, 字符串作为判断条件if switch, 权限判断
在定义的字符串的时候不翻译，到变量转了好几遍以后，使用的时候才翻译。
还有很多垃圾代码，或者不再使用的功能，无法确定
'''
except_file_list = [
    r"lmsa\common\lenovo.mbg.service.common.utilities\Configurations.cs",
    r"lmsa\common\lenovo.mbg.service.common.utilities\DriversHelper.cs",
    r"lmsa/framework/devicemgt/DeviceListener/ReadPropertiesInFastboot.cs",
    r"lmsa/framework/devicemgt/DeviceListener/DeviceManager.cs",
    r"lmsa/framework/devicemgt/DeviceOperator/AdbOperator.cs",
    r"???lmsa/framework/messageconstant/lenovo.mbg.service.framework.message.constant/MessageConstant.cs",
    r"lmsa/framework/resources/DownloadResourcesCompatible.cs",
    r"lmsa/framework/services/Download/DownloadInfo.cs",
    r"lmsa/framework/smartdevice/Steps/FastbootDeviceMatchCheck.cs",
    r"lmsa/framework/smartdevice/Steps/FindComPorts.cs",
    r"lmsa/framework/smartdevice/Steps/ReadPropertiesInFastboot.cs",
    r"lmsa/framework/socket/FileTransfer/SocketServiceHeadersDefine.cs",
    r"???lmsa/lmsa/Lenovo Moto Smart Assistant/Business/Notice/FeedbackNotice.cs",
    r"???lmsa/lmsa/Lenovo Moto Smart Assistant/Converters/NewVersionNameConverter.cs",
    r"lmsa/lmsa/Lenovo Moto Smart Assistant/Login/View/LoggingInView.xaml.cs",
    r"lmsa/lmsa/Lenovo Moto Smart Assistant/ResourcesCleanUp/Storage/ResourcesLog.cs",
    r"lmsa/lmsa/Lenovo Moto Smart Assistant/ViewModels/NewVersionViewModel.cs",
    r"lmsa/plugins/flash/UserControlsViewModelV2/ManualFastbootReadStepViewModel.cs",
    r"lmsa/plugins/flash/common/FlashFailedGuide.cs",
    r"lmsa/plugins/flash/common/ReadFastbootProperties.cs",
    r"???lmsa/plugins/flash/vibeflash/Controls/DeviceStageUserControls/DeviceUpdated.xaml.cs",
    r"???lmsa/plugins/flash/vibeflash/Controls/DeviceStageUserControls/DeviceUpdatedBK.xaml.cs",
    r"lmsa/plugins/support/Business/IBaseWarrantyConverter.cs",
    r"lmsa/plugins/support/Business/SearchService.cs",
    r"lmsa/plugins/support/ViewModel/IBaseSearchResultViewModel.cs",
    r"lmsa/plugins/support/ViewModel/SupportSearchResultViewModel.cs",
    r"lmsa/plugins/toolBox/GifMaker/Gif/PlotCore/PlotSetModel.cs",
    r"lmsa/plugins/toolBox/GifMaker/Model/PlotModel.cs",
    r"lmsa/plugins/toolBox/GifMaker/Model/ProgressModel.cs",
    r"lmsa/plugins/toolBox/ScreenCapture/ViewModel/VideoDetailListItemViewModel.cs",
    r"lmsa/plugins/phoneManager/Business/BackupRestore/Storage/Test.cs",
    r"lmsa/plugins/phoneManager/Business/DeviceSmsManagement.cs"
]

if __name__ == "__main__":
    # pretreatment_cs_xaml()
    # 正则表达式替换 LangText(="{Binding.*?}")     LangText$1 LangKey$1
    # 正则表达式替换 LangText(="{TemplateBinding.*?}")     LangText$1 LangKey$1
    # 正则表达式替换 Application.Current.Resources\[".*\w\d{4}"\]       Application.Current.FindResource\(".*\w\d{4}"\)
    replace_english_to_key()
