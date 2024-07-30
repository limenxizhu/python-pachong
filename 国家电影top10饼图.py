# _*_coding:UTF-8 _*_
# @Time : 2024/6/22 16:58
# @Author:lupeng
# @File : 数据可视化
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../1.csv')


df['country'] = df['country'].str.split(',')
# 展开country列以便每个国家都有单独的行
df = df.explode('country').reset_index(drop=True)
# 将含有非数值的数据转换为NaN
for column in ['first_week_box_office', 'total_box_office']:
    df[column] = pd.to_numeric(df[column], errors='coerce')
# 删除含有NaN的行
df.dropna(subset=['first_week_box_office', 'total_box_office'], inplace=True)
# 对于合作电影，平分票房
df['total_box_office'] /= df['country'].apply(lambda x: len(x))
# 计算每个国家的总票房
df['country'] = df['country'].str.strip().str.lower()
# 再次进行groupby和sum操作
total_box_office_by_country = df.groupby('country')['total_box_office'].sum().reset_index()
# 确保排序
total_box_office_by_country.sort_values(by='total_box_office', ascending=False, inplace=True)
# 选择排名前十的国家
# 选择排名前十的国家及其总票房
top_countries = total_box_office_by_country.head(10)
# 创建饼图
plt.figure(figsize=(8, 8))
plt.pie(top_countries['total_box_office'],
        labels=top_countries['country'],
        autopct='%1.1f%%',  # 显示百分比
        startangle=140)     # 开始角度
plt.title('各国电影总票房占比（Top 10）')
plt.axis('equal')          # 确保饼图是圆形
plt.tight_layout()
plt.savefig('国家票房占比top10.png', dpi=300)
plt.show()