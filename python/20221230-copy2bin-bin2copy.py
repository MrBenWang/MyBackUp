#!/usr/bin/env python3
# coding: utf-8
import os
import time
import shutil


current_dir = r"C:\Users\zhenglong.wang\Desktop\测试\RSA签名"
items = [
    {"dll_name": "lenovo.mbg.service.lmsa.flash.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.flash.common.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c", "only": True},
    {"dll_name": "lenovo.mbg.service.common.log.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c"},
    {"dll_name": "lenovo.mbg.service.framework.devicemgt.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c"},
    {"dll_name": "lenovo.mbg.service.framework.smartbase.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c"},
    {"dll_name": "lenovo.mbg.service.framework.smartdevice.dll", "target_bin_path": "plugins\8ab04aa975e34f1ca4f9dc3a81374e2c"},

    {"dll_name": "lenovo.mbg.service.lmsa.forum.dll", "target_bin_path": "plugins\310f47ad70d54880b33225d864e6fe68", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.hostproxy.dll", "target_bin_path": "plugins\310f47ad70d54880b33225d864e6fe68"},
    {"dll_name": "lenovo.mbg.service.common.log.dll", "target_bin_path": "plugins\310f47ad70d54880b33225d864e6fe68"},
    {"dll_name": "lenovo.mbg.service.common.utilities.dll", "target_bin_path": "plugins\310f47ad70d54880b33225d864e6fe68"},
    {"dll_name": "lenovo.mbg.service.framework.lang.dll", "target_bin_path": "plugins\310f47ad70d54880b33225d864e6fe68"},

    {"dll_name": "lenovo.mbg.service.lmsa.tips.dll", "target_bin_path": "plugins\992e746537954a7d9ae613d5ec9bc7a6", "only": True},
    {"dll_name": "lenovo.mbg.service.framework.devicemgt.dll", "target_bin_path": "plugins\992e746537954a7d9ae613d5ec9bc7a6"},

    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.phonemanager.apps.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.common.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8", "only": True},
    {"dll_name": "lenovo.mbg.service.framework.devicemgt.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8"},
    {"dll_name": "lenovo.mbg.service.framework.msgConstant.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8"},
    {"dll_name": "lenovo.mbg.service.lmsa.common.dll", "target_bin_path": "plugins\02928af025384c75ae055aa2d4f256c8"},

    {"dll_name": "lenovo.mbg.service.lmsa.messenger.dll", "target_bin_path": "plugins\a6099126929a4e74ac86f1c2405dcb32", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.support.dll", "target_bin_path": "plugins\a6099126929a4e74ac86f1c2405dcb32", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.tips.dll", "target_bin_path": "plugins\a6099126929a4e74ac86f1c2405dcb32"},
    {"dll_name": "lenovo.mbg.service.lmsa.forum.dll", "target_bin_path": "plugins\a6099126929a4e74ac86f1c2405dcb32"},

    {"dll_name": "lenovo.mbg.service.lmsa.toolbox.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a", "only": True},
    {"dll_name": "lenovo.mbg.service.lmsa.phonemanager.apps.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.common.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.lmsa.phoneManager.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.common.webservices.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.framework.devicemgt.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.framework.msgConstant.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.lmsa.common.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"},
    {"dll_name": "lenovo.mbg.service.lmsa.flash.common.dll", "target_bin_path": "plugins\dd537b5c6c074ae49cc8b0b2965ce54a"}
]


def copy_to_bin(dll_name, plugin_path):
    dll_current_path = current_dir + "/" + dll_name
    dll_bin_path = "D:/Projects/lmsa-client/Bin/" + plugin_path + dll_name
    shutil.copyfile(dll_current_path, dll_bin_path)


if __name__ == "__main__":
    # do_translate_vscode("Reselect", "it")
    # print(translator.translate('Reselect', src="en", dest='it'))
    copy_to_bin()
