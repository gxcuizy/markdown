#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PIL import Image
import os
import glob
from PIL import ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
# 当前目录
in_dir = os.getcwd()
# 转换后图片目录
out_dir = in_dir + ' mini'
# 缩放比例
percent = 0.4
percent = float(percent)
if not os.path.exists(out_dir):
    os.mkdir(out_dir)


# 图片批处理
def main():
    for files in glob.glob(in_dir + '/*.jpg'):
        filepath, filename = os.path.split(files)
        im = Image.open(files)
        im = im.resize((1080, 810))
        im.save(os.path.join(out_dir, filename))


if __name__ == '__main__':
    main()
print('you succeed.')
