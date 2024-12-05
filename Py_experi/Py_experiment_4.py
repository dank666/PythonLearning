from faker import Faker
from openpyxl import Workbook
from random import randint
import numpy as np
import pandas as pd

def create_stuInfo_excel(stu_num):
    faker = Faker(locale='zh_CN')
    workbook = Workbook()
    worksheet = workbook.create_sheet(title='students', index=0)
    columns = ['学号', '姓名', '电话', '性别']
    worksheet.append(columns)
    for i in range(stu_num):
        line = []
        line.append(f'{1000 + i : 04}')
        line.append(faker.name())
        line.append(faker.phone_number())
        line.append(faker.simple_profile()['sex'])
        worksheet.append(line)
    filename1 = 'student_info.xlsx'
    workbook.save(filename1)

def create_stuScore_csv(stu_num):
    columns2 = ['学号', '成绩']
    score_list = []
    score_list.append(columns2)  # 在列表的开头添加列名
    for i in range(stu_num):
        line = []
        line.append(f'{1000 + i:04}')
        line.append(str(randint(0, 100)))
        score_list.append(line)

    filename2 = 'student_score.csv'
    with open(filename2, 'w', encoding='utf-8') as fcsv:  # 使用with语句打开文件
        for line in score_list:
            fcsv.write(','.join(line) + '\n')  # 写入每一行

def stu_stat(student_info_excel, student_score_csv):
    df_excel = pd.read_excel(student_info_excel)
    df_csv = pd.read_csv(student_score_csv, encoding='utf-8')
    df_csv.columns = df_csv.columns.str.strip()  # 去掉列名的空格

    print("Excel 列名：", df_excel.columns)  # 打印 Excel 列名
    print("CSV 列名：", df_csv.columns)  # 打印 CSV 列名
    print("CSV 数据：", df_csv.head())  # 打印 CSV 的前几行数据

    df = pd.merge(df_excel, df_csv, on='学号')

    male_ratio = sum(df['性别'] == 'M') / len(df['性别'])
    print('男生占比：{:.2%}'.format(male_ratio), '女生占比：{:.2%}'.format(1 - male_ratio))
    max_score_stu = df[df['成绩'] == max(df['成绩'])][['学号', '姓名']]
    min_score_stu = df[df['成绩'] == min(df['成绩'])][['学号', '姓名']]
    print('最高分：{:.2%}'.format(max(df['成绩'])))
    print(max_score_stu)
    print('最低分：{:.2%}'.format(min(df['成绩'])))
    print(min_score_stu)
    print('平均分：{:}'.format(int(np.average(df['成绩']))))
    interval = [0, 60, 70, 80, 90, 100]
    print(pd.cut(df['成绩'], interval, right=False).value_counts(sort=False))

stu_num = 30
create_stuInfo_excel(stu_num)
create_stuScore_csv(stu_num)
stu_stat('student_info.xlsx', 'student_score.csv')
