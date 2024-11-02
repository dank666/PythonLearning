#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
PythonLearning -
Author: wtejing
Date: 2024/11/2
"""

print('------------------------')
print("42312205 王特警")
# # 编写程序，用户输入一段英文，然后输出这段英文中所有长度为3个字母的单词。
# import re
# text = input("请输入一段英文：")
# def words_three(text):
#     return re.findall(r'\b\w{3}\b', text)
# print(words_three(text))



# # 有一段英文文本，其中有单词连续重复了2次，编写程序检查重复的单词并只保留一个。例如文本内容为“This is is a desk.”，程序输出为“This is a desk.”
# import re
# def remove_repeated_words(text):
#     # 使用正则表达式匹配连续重复的单词
#     # r'\b(\w+)\s+\1\b' 匹配整个单词重复的模式
#     return re.sub(r'\b(\w+)\s+\1\s+\1\s+\1\b', r'\1', text)
#
# # 示例文本
# text = "This is is is is a desk."
# print("源文本：", text)
# output = remove_repeated_words(text)
# print("去重后的文本:", output)



# # 编写程序，用户从键盘输入小于1000的整数，对其进行因式分解。例如，10=2×5，60=2×2×3×5。
# def prime_factors(n):
#     factors = []
#     # 从质数2开始
#     divisor = 2
#     while n >= 2:
#         if n % divisor == 0:
#             factors.append(divisor)
#             n /= divisor
#         else:
#             divisor += 1
#     return factors
#
#
# num = int(input("请输入一个小于1000的整数："))
# if num <= 1 or num >= 1000:
#     print("请输入一个小于1000的整数：")
# else:
#     factors = prime_factors(num)
#     factors_str = "x".join(map(str, factors))
#     print(f"{num} = {factors_str}")



# # 编写程序，生成一个包含50个随机整数的列表，然后删除其中所有奇数。
# import random
# random_list = [random.randint(0, 100) for _ in range(50)]
# print("origin list: ", random_list)
#
# filtered_list = [num for num in random_list if num % 2 == 0]
# print("filtered list: ", filtered_list)
