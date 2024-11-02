#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PythonLearning -
Author: wtejing
Date: 2024/11/2
"""

print('------------------------')
print("42312205 王特警")
import re
import jieba
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from urllib.request import urlopen

startUrl = r'http://ccs.snnu.edu.cn/xygk/lsyg1.htm'
with urlopen(startUrl) as fp:
    content = fp.read().decode('utf-8')  # 从指定的 URL 下载内容，并将其转换为字符串形式

# 定义一个函数来清除HTML标签
def clean_html(html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', html)
    return cleantext

# 提取并遍历每个事件链接
pattern = re.compile(r'<p.*?><strong><span.*?>(.*?)</span></strong>\s*<span.*?>(.*?)</span>\s*</p>', re.DOTALL | re.IGNORECASE)
result = re.findall(pattern, content)

# 检查结果是否为空
if not result:
    print("No matches found.")
else:
    file_test = open('test_example.txt', 'w', encoding='utf-8')

    result_str = ""
    for item in result:
        time = clean_html(item[0]).strip()  # 清理时间字段中的HTML标签
        description = clean_html(item[1]).strip()  # 清理描述字段中的HTML标签
        print(time, description)
        result_str += f'{time} {description}\n'
        file_test.write(f'时间： {time}\r\n')
        file_test.write(f'事件： {description}\r\n')
    file_test.close()

    words = jieba.lcut(result_str)
    words_str = ' '.join(words)
    stat_dict = {}
    for element in words:
        stat_dict[element] = stat_dict.get(element, 0) + 1
    print(stat_dict)

    # 创建wordcloud对象
    wc = WordCloud(
        font_path=r'C:\windows\fonts\simfang.ttf', width=500, height=400,
        background_color='white', font_step=3,
        random_state=False, prefer_horizontal=0.9
    )
    # 创建并显示词云
    craw_stat = wc.generate(words_str)
    craw_stat.to_image().save('craw_stat.png')
    plt.imshow(craw_stat)
    plt.axis('off')
    plt.show()