#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PythonLearning -
Author: wtejing
Date: 2024/11/1
"""

print('------------------------')
import wordcloud
import re
import matplotlib.pyplot as plt
import jieba
from urllib.request import urlopen

startUrl = r'http://ccs.snnu.edu.cn/xygk/lsyg1.htm'
with urlopen(startUrl) as fp:
    content = fp.read().decode()

#提取并遍历每个事件链接
