import keyring
import subprocess
import datetime
import colorama
import requests
import json

import os
import sys
import shutil
import sqlite3
import win32crypt
colorama.init()  # support ANSI sequences on Windows

"""
三个月更改一次密码的，希望通过脚本能一键更新，所有软件的密码
"""

lastModifyDate = "2018-11-10"   # 修改日期，必须大于今天
current_index = 1  # 当前第几个,

items = []
new_pwds = []
new_win_pwd = "test123456"


def init():
    global new_pwds
    new_pwds = ["imzi-8357", "imzi-8457", "imzi-8557", "imzi-8657"]

    """
    控制面板/所有控制面板项/凭据管理器 -> Windows 凭据 -> 普通凭据
    {"group","remake", "system", "username", "new_pwd"}
    {"密码类型","备注名", "Internet地址或网络地址", "用户名", "新密码(为空不修改)"}
    密码类型：
    w_login     windows登陆密码
    w_nomal_pwd 控制面板/所有控制面板项/凭据管理器 -> Windows 凭据 -> 普通凭据
    i_web_pwd   修改网站密码
    """
    global items
    items = [
        ["w_login", "Windows登陆", "windows", "username", new_win_pwd],
        ["w_nomal_pwd", "VPN", "Microsoft_OC1:uri=username@test.com:specific:LAD:1",
            "username@test.com", new_pwds[current_index]],
        ["w_nomal_pwd", "git_lenovo", "git:http://gitlab.test.com", "username", new_pwds[current_index]],
        ["w_nomal_pwd", "git_lenovo_at", "git:http://username@gitlab.test.com", "username", new_pwds[current_index]],
        ["w_nomal_pwd", "Remote 78", "TerMSRV/10.50.40.78", "CNT01\\administrator", ""],
        ["w_nomal_pwd", "Remote 80", "TerMSRV/10.50.40.80", "CNT01\\administrator", ""],
        ["i_web_pwd", "web_lenovo", "https://myos.com/accaweb/api/loginutils/login", "username", new_pwds[current_index]]
    ]


def show_pwd():
    """
    展示 windows 普通凭据
    """
    print("\t\033[4;32;40m**windows普通凭据 新密码**\033[0m")
    print("-----------------------")
    for _i in items:
        if _i[0] == "w_nomal_pwd":
            keyring.get_password(_i[2], _i[3])
            print(_i[1] + ":\t" + keyring.get_password(_i[2], _i[3]))


def _ser_windows_login_pwd():
    """
    修改windows 登陆密码
    """
    for _i in items:
        if _i[0] == "w_login" and _i[4]:
            _cmd = "net users {0} {1} /domain".format(_i[3], _i[4])
            subprocess.call(_cmd, shell=True)
            return


def _set_windows_nomal_pwd():
    """
    修改windows 普通凭据
    """
    for _i in items:
        if _i[0] == "w_nomal_pwd" and _i[4]:
            keyring.set_password(_i[2], _i[3], _i[4])
    print("\t\033[4;32;40m**新密码**\033[0m")
    print("-----------------------")
    show_pwd()


def _set_web_pwd():
    """
    修改  web 的密码，不同网站的修改密码方式不同
    """
    return  # 暂无
    web_info_index = None
    web_info_item = None
    for index, item in enumerate(items):
        if item[0] == "i_web_pwd":
            web_info_index = index
            web_info_item = item
            break

    if not web_info_item:
        return

    # 用旧密码登陆
    myrequest = requests.Session()
    post_data = {
        "os_username": web_info_item[3],
        "os_password": items[web_info_index - 1][4],  # 旧密码
        "login": "登录"
    }
    myrequest.post("https://myos.com/accaweb/api/loginutils/login", data=post_data)

    # 使用新密码修改
    post_data = {
        "os_username": web_info_item[3],
        "os_password": web_info_item[4],
        "os_password_old": items[web_info_index - 1][4],  # 旧密码
        "login": "登录"
    }
    response = myrequest.post(web_info_item[2], data=post_data)
    json_data = json.loads(response.text)
    if not json_data:
        print("地址访问出现问题:" + web_info_item[2])
    elif json_data["code"] == "0":
        print("web 密码修改成功!")
    else:
        print("Web 密码修改失败,原因:" + response.text)


def _set_windows_mail_pwd():
    """
    设置 windows mail，或者 outlook 为新密码
    暂不知道如何实现
    """
    pass


def _ser_chrome_pwd():
    r"""
    C:\Users\用户名\AppData\Local\Google\Chrome\User Data\Default
    更新 chrome 的密码，尝试修改sqlite数据，并且替换后
    会多处一条，修改后的数据。推测，可能有md5校验，防止暴力修改密码
    """

    outFile_path = os.path.join(os.getcwd(), "ChromePass.txt")
    if os.path.exists(outFile_path):
        os.remove(outFile_path)

    db_file_path = os.path.join(os.environ["LOCALAPPDATA"],
                                r"Google\Chrome\User Data\Default\Login Data")
    tmp_file = os.path.join(os.getcwd(), "tmp_tmp_tmp")
    if os.path.exists(tmp_file):
        os.remove(tmp_file)
    shutil.copyfile(db_file_path, tmp_file)    # In case file locked
    conn = sqlite3.connect(tmp_file)
    for item in items:
        if item[0] == "i_web_pwd":
            new_pwd = win32crypt.CryptProtectData(item[0].encode('utf-16-le'), None, None, None, None, 0)  # 新密码加密
            conn.execute(
                "update logins set password_value=? where origin_url=? and username_value=? ", (new_pwd, item[2], item[3]))
            conn.commit()
    conn.close()
    shutil.copyfile(tmp_file, db_file_path)  # 需要关闭，所有Chrome 相关进程


def set_new_pwd():
    _ser_windows_login_pwd()
    _set_windows_nomal_pwd()
    _set_web_pwd()
    _set_windows_mail_pwd()


if __name__ == "__main__":
    init()
    print("\t**旧密码**")
    print("-----------------------")
    _today = datetime.datetime.today()
    _last = datetime.datetime.strptime(lastModifyDate, "%Y-%m-%d")

    if _today >= _last:
        print("\033[1;31;47m 请检查是否没有修改 新密码!\033[0m")
    else:
        show_pwd()
    print("-----------------------")
    print("继续修改密码，请输入\033[4;32;40m y \033[0m，放弃修改输入\033[4;31;40m n \033[0m: ")
    input_name = input()
    if input_name == "y" or input_name == "Y":
        print("开始修改密码！")
