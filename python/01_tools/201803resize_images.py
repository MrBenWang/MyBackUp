#!/usr/bin/env python3
#coding: utf-8

"""
resize the images, reduce the image size
e.g :   old/test.jpg (3M) --> new/test.jpg (512k)
"""

import os
from glob import glob
from PIL import Image

def _resize_images(__source_dir, __target_dir, __threshold):
    __filenames = glob('{}/*'.format(__source_dir))
    if not os.path.exists(__target_dir):
        os.makedirs(__target_dir)
    for filename in __filenames:
        filesize = os.path.getsize(filename)
        if filesize >= __threshold:
            print(filename)
            with Image.open(filename) as __im:
                width, height = __im.size
                new_width = 1024
                new_height = int(new_width * height * 1.0 / width)
                resized_im = __im.resize((new_width, new_height))
                output_filename = filename.replace(__source_dir, __target_dir)
                resized_im.save(output_filename)

if __name__ == '__main__':
    _resize_images("F:/银盘的备份/2016", "F:/test/2016", 1*1024*1024)
