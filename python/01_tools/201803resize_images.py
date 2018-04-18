#!/usr/bin/python3
# -*- coding:utf8 -*-

import codecs
import os
from glob import glob
from PIL import Image

# resize the images, reduce the image size
# e.g :   old/test.jpg (3M) --> new/test.jpg (512k)
def resize_images(source_dir, target_dir, threshold):
    filenames = glob('{}/*'.format(source_dir))
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for filename in filenames:
        filesize = os.path.getsize(filename)
        if filesize >= threshold:
            print(filename)
            with Image.open(filename) as im:
                width, height = im.size
                new_width = 1024
                new_height = int(new_width * height * 1.0 / width)
                resized_im = im.resize((new_width, new_height))
                output_filename = filename.replace(source_dir, target_dir)
                resized_im.save(output_filename)

if __name__ == '__main__':
    resize_images("F:/银盘的备份/2016","F:/test/2016",1*1024*1024)
