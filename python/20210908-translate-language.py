#!/usr/bin/env python3
# coding: utf-8
from openpyxl import load_workbook
from googletrans import Translator
import os
import time

source_excel = "translate_language.xlsx"
base_path = os.path.dirname(os.path.realpath(__file__))
language_code = []
translator = Translator(service_urls=[
    'translate.google.cn'
])


def do_translate(text_english, target_lang):
    str_tran = translator.translate(text_english, src='en', dest=target_lang.strip()).text
    print(str_tran)
    return str_tran


def read_excel():
    _file_path = os.path.join(base_path, source_excel)
    _wb = load_workbook(_file_path)
    _sheet = _wb.worksheets[0]  # 第一个工作表
    text_english = ""
    for index_r, row in enumerate(_sheet.iter_rows()):
        if index_r == 1:  # 第二行的内容为语言编码
            for cell in row:
                language_code.append(cell.value)

        if index_r > 1:  # 从第三行开始读取
            for index_c, cell in enumerate(row):
                if index_c == 1:  # 第二列为待翻译的英文
                    text_english = cell.value
                if index_c > 1:  # 需要翻译的对于语言
                    target_lang = language_code[index_c]
                    text_replace = text_english.replace("&#x0a;", "\n").replace("&quot;", "\"")
                    cell.value = do_translate(text_replace, target_lang)
    _wb.save(filename=os.path.join(base_path, time.strftime("%m%d%H%M%S-", time.localtime()) + source_excel))


if __name__ == "__main__":
    #print(translator.translate('안녕하세요.', src="ko", dest='zh-cn'))
    read_excel()
