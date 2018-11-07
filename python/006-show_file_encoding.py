import chardet
import os

dir_my = r"C:\Wzl\mrbenwang.github.io-hugo\themes\jane\layouts\_default"

"""
显示 该文件加下面，所有的文件 编码格式。
是根据文本的内容来判断的，有可能是，ascii 或 utf-8。不过 ascii 占用存储空间更少。

例如：chardet.detect 始终显示是 ascii ，无论 vscode 中，怎么改变为utf-8。
"""


def GetFileList(_dir):
    if os.path.isfile(_dir):
        f = open(_dir, 'rb')
        data = f.read()
        _tmp_encoding = chardet.detect(data)["encoding"]
        # if _tmp_encoding == "utf-8" or _tmp_encoding == "ascii":  # 排除常规编码格式
        #     pass
        # else:
        #     print(str(chardet.detect(data)) + "\t" + _dir[find_nth(_dir, "\\", 4):])
        print(str(chardet.detect(data)) + "\t" + _dir[find_nth(_dir, "\\", 4):])
    elif os.path.isdir(_dir):
        for s in os.listdir(_dir):
            if s == ".git":  # 忽略 .git目录
                continue
            loop_new_dir = os.path.join(_dir, s)
            GetFileList(loop_new_dir)


def find_nth(string, substring, n):
    """
    递归查找，第几个 字符串
    """
    if (n == 1):
        return string.find(substring)
    else:
        return string.find(substring, find_nth(string, substring, n - 1) + 1)


if __name__ == '__main__':
    #print(dir_my[find_nth(dir_my, "\\", 4):])
    GetFileList(dir_my)
