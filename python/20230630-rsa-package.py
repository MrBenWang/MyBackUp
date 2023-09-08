#!/usr/bin/env python3
# coding: utf-8
import os
import shutil
import tkinter as tk
import tkinter.filedialog  # 注意次数要将文件对话框导入


signatured_items = [
    {"dll_name": "lenovo.mbg.service.lmsa.flash.dll", "target_bin_path": "plugins/8ab04aa975e34f1ca4f9dc3a81374e2c"},

    {"dll_name": "lenovo.mbg.service.lmsa.backuprestore.dll", "target_bin_path": "plugins/13f79fe4cfc98747c78794a943886bcd"},

    {"dll_name": "lenovo.mbg.service.lmsa.phonemanager.apps.dll", "target_bin_path": "plugins/02928af025384c75ae055aa2d4f256c8"},
    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.common.dll", "target_bin_path": "plugins/02928af025384c75ae055aa2d4f256c8"},
    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.dll", "target_bin_path": "plugins/02928af025384c75ae055aa2d4f256c8"},

    {"dll_name": "lenovo.mbg.service.lmsa.forum.dll", "target_bin_path": "plugins/a6099126929a4e74ac86f1c2405dcb32"},
    {"dll_name": "lenovo.mbg.service.lmsa.messenger.dll", "target_bin_path": "plugins/a6099126929a4e74ac86f1c2405dcb32"},
    {"dll_name": "lenovo.mbg.service.lmsa.support.dll", "target_bin_path": "plugins/a6099126929a4e74ac86f1c2405dcb32"},
    {"dll_name": "lenovo.mbg.service.lmsa.tips.dll", "target_bin_path": "plugins/a6099126929a4e74ac86f1c2405dcb32"},

    {"dll_name": "lenovo.mbg.service.lmsa.toolbox.dll", "target_bin_path": "plugins/dd537b5c6c074ae49cc8b0b2965ce54a"},

    {"dll_name": "lenovo.mbg.service.lmsa.hardwaretest.dll", "target_bin_path": "plugins/985c66acdde2483ed96844a6b5ea4337"},

    {"dll_name": "lenovo.mbg.service.common.log.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.common.utilities.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.common.webservices.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.devicemgt.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.download.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.hostcontroller.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.lang.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.pipes.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.resources.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.services.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.smartbase.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.smartdevice.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.socket.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.framework.updateversion.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.lmsa.common.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.mbg.service.lmsa.hostproxy.dll", "target_bin_path": ""},
    {"dll_name": "lenovo.themes.generic.dll", "target_bin_path": ""},

    # exe 文件
    {"dll_name": "LmsaWindowsService.exe", "target_bin_path": ""},
    {"dll_name": "Rescue and Smart Assistant.exe", "target_bin_path": ""},
    {"dll_name": "Uninstall.exe", "target_bin_path": ""},
    {"dll_name": "UninstallSurvey.exe", "target_bin_path": "Survey"},
    {"dll_name": "LmsaServiceUI.exe", "target_bin_path": "C:/ProgramData/LMSA/LmsaServiceUI"},
]


install_path = "C:/Program Files/Rescue and Smart Assistant/"
signature_path = "D:/RSA签名"
dll_bin_path = "D:/Projects/lmsa-client/Bin/"


def copy_to_bin():
    _uninstall_path = os.path.join(dll_bin_path, "Uninstall.exe")
    shutil.copyfile(os.path.join(signature_path, "Uninstall.exe"), _uninstall_path)

    for _item in signatured_items:
        _output_path = ""
        if _item["dll_name"].endswith(".exe"):
            _output_path = os.path.join(dll_bin_path, _item["dll_name"])
        else:
            _output_path = os.path.join(dll_bin_path, _item["target_bin_path"], _item["dll_name"])
        print("save to bin: "+_output_path)
        shutil.copyfile(os.path.join(signature_path, _item["dll_name"]), _output_path)


def copy_for_signature():
    _uninstall_path = os.path.join(install_path, "Uninstall.exe")
    shutil.copyfile(_uninstall_path, os.path.join(signature_path, "Uninstall.exe"))

    for _item in signatured_items:
        _output_path = ""
        if _item["dll_name"] != "LmsaServiceUI.exe":
            _output_path = os.path.join(install_path, _item["target_bin_path"], _item["dll_name"])
        else:
            _output_path = os.path.join(_item["target_bin_path"], _item["dll_name"])
        print("for signature: "+_output_path)
        shutil.copyfile(_output_path, os.path.join(signature_path, _item["dll_name"]))


def open_file_dialog(_default_path, _type):
    # 从本地选择一个文件，并返回文件的目录
    _dir_new_path = tkinter.filedialog.askdirectory(initialdir=_default_path)
    if _dir_new_path == '':
        return

    if _type == "install":
        install_path = _dir_new_path
        lb_install.config(text=_dir_new_path)
    elif _type == "bin":
        dll_bin_path = _dir_new_path
        lb_bin.config(text=_dir_new_path)
    elif _type == "sign":
        signature_path = _dir_new_path
        lb_sign.config(text=_dir_new_path)
    else:
        raise


def replace_version_compile():
    raise


_my_version = "1.0.0"
_my_new_version = "1.0.0"
if __name__ == "__main__":
    logfile = open("D:/Projects/lmsa-client/lmsa-package-multi-lang.nsi", "r", -1, "utf-8")
    lines = logfile.readlines()
    for line in lines:
        if ("!define PRODUCT_VERSION" in line):
            print(line)
            _my_version = line.split("\"")[1]
    # 版本号+1
    # _my_new_version = _my_version.split(".")[0, -1]+int(_my_version.split(".")[-1])+1

root_window = tk.Tk()  # 创建主窗口
root_window.title("RSA 签名打包")  # 设置窗口标题

# 窗口居中，获取屏幕尺寸以计算布局参数，使窗口居屏幕中央
width = 500
height = 400
screenwidth = root_window.winfo_screenwidth()
screenheight = root_window.winfo_screenheight()
size_geo = "%dx%d+%d+%d" % (width, height, (screenwidth-width)/2, (screenheight-height)/2)
root_window.geometry(size_geo)
root_window.minsize(width, height)

# 编译
frame_compile = tk.LabelFrame(root_window, text="编  译", height=150, width=400, labelanchor="n", background='#5CACEE')
frame_compile.place(relwidth=1, relheight=0.3)

tk.Label(frame_compile, text="当前版本版本号：").grid(row=0, column=0, padx=10, pady=2,  sticky="e")
tk.Label(frame_compile, text=_my_version, relief="sunken").grid(row=0, column=1, padx=10, pady=2, sticky="w")

tk.Label(frame_compile, text="待替换的版本号：").grid(row=1, column=0, padx=10, pady=2,  sticky="e")
input_version = tk.Entry(frame_compile, width=8)
input_version.grid(row=1, column=1, padx=10, pady=2, sticky="w")
input_version.insert(0, _my_new_version)

tk.Button(frame_compile, text="替换版本号，并且执行编译", command=replace_version_compile).grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="w")

# 打包
frame_package = tk.LabelFrame(root_window, text="打  包", height=150, width=400, labelanchor="n", background='#66CDAA')
frame_package.place(relx=0, rely=0.3, relwidth=1, relheight=0.7)

tk.Button(frame_package, text="安装的路径：", command=lambda: open_file_dialog(install_path, "install")).grid(row=0, column=0, padx=10, pady=2, sticky="e")
lb_install = tk.Label(frame_package, text=install_path, relief="sunken")
lb_install.grid(row=0, column=1, sticky="w")

tk.Button(frame_package, text="Bin的路径：", command=lambda: open_file_dialog(dll_bin_path, "bin")).grid(row=1, column=0, padx=10, pady=2, sticky="e")
lb_bin = tk.Label(frame_package, text=dll_bin_path, relief="sunken")
lb_bin.grid(row=1, column=1, sticky="w")

tk.Button(frame_package, text="RSA签名 tmp:", command=lambda: open_file_dialog(signature_path, "sign")).grid(row=2, column=0, padx=10, pady=2, sticky="e")
lb_sign = tk.Label(frame_package, text=signature_path, relief="sunken")
lb_sign.grid(row=2, column=1, sticky="w")

tk.Button(frame_package, text="从安装目录Copy出来 准备签名", command=copy_for_signature).grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)
tk.Button(frame_package, text="Copy到Bin 准备打包", command=copy_to_bin).grid(row=3, column=1, sticky="e", padx=10, pady=5)

root_window.mainloop()  # 主窗口进入消息事件循环
