#!/usr/bin/env python3
#coding: utf-8

"""
create a new TXT file, the TXT's name is the same as the movie name.
"""

import os

def _get_filename(__path):
    f_list = os.listdir(__path)
    for i in f_list:
        #print(os.__path.splitext(i)[1])
        mytmp = i.decode('gbk')
        if os.path.splitext(mytmp)[1] != '.txt':
            __tmp_path = "%s/%stxt" % (__path, mytmp[:mytmp.rfind(".")+1])
            #open(__path + "/" + mytmp[:mytmp.rfind(".")+1]+"txt", "w").close()
            open(__tmp_path, "w").close()
            #print(__path+"/"+ mytmp[:mytmp.rfind(".")+1]+"txt")
            print(__tmp_path)

if __name__ == '__main__':
    _get_filename('G:/2-Relx/RMVB/movie')
