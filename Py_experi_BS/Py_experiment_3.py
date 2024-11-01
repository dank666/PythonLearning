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
    content = fp.read().decode()  # 从指定的 URL 下载内容，并将其转换为字符串形式

# 提取并遍历每个事件链接
pattern = re.compile(u'p.*?<span style="background.*?>(.*?)</span>.*?' + '<span style="background.*?">:(>*?)</span>(.*?)</span></p>', re.I)
# u 表示这是一个 Unicode 字符串。在 Python 3 中，字符串默认就是 Unicode，所以 u 前缀是可选的。
# .*? 是非贪婪匹配，匹配任意数量的任意字符（除了换行符），尽可能少地匹配
# <span style="background.*?"> 匹配 <span> 标签，其中 style 属性包含 background，并且 .*? 是非贪婪匹配，尽可能少地匹配。
# (.*?) 是一个捕获组，匹配任意数量的任意字符（除了换行符），尽可能少地匹配。这个捕获组用于提取第一个 <span> 标签内的内容。
# re.I 是 re.IGNORECASE 的缩写，表示忽略大小写。
result = re.findall(pattern, content)
# re.findall 是 Python 的 re 模块中的一个函数，用于在字符串中查找所有与给定正则表达式模式匹配的子串，并返回一个列表。
file_test = open('test_example', 'w', encoding='utf-8')

result_str = ""
for item in result:
    print(item[0], item[1], item[2])
    result_str += ''.join(item)
    file_test.write('时间： ' + item[0] + '\r\n')
    file_test.write('事件： ' + item[1] + item[2] + '\r\n')
file_test.close()

words = jieba.lcut(result_str)
words_str = ' '.join(words)
stat_dict = {}
for element in words:
    stat_dict[element] = stat_dict.get(element, 0) + 1
print(stat_dict)

# 创建wordcloud对象
wc = wordcloud.WordCloud(
    r'C:\windows\fonts\simfang.ttf', width=500, height=400,
    background_color='white', font_step=3,
    random_state=False, prefer_horizontal=0.9)
