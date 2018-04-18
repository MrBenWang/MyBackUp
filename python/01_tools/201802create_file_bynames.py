#!/usr/bin/python3
# -*- coding:utf8 -*-
# create a new TXT file, the TXT's name is the same as the movie name.

import codecs
import os

path = 'G:/2-Relx/RMVB/movie'
def getFileName(path):
    f_list = os.listdir(path)
    for i in f_list:
        #print(os.path.splitext(i)[1])
        mytmp = i.decode('gbk')
        if os.path.splitext(mytmp)[1] != '.txt':
            open(path+"/"+mytmp[:mytmp.rfind(".")+1]+"txt","w").close()
            print(path+"/"+ mytmp[:mytmp.rfind(".")+1]+"txt")

if __name__ == '__main__':
    getFileName(path)
