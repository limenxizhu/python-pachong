# _*_coding:UTF-8 _*_
# @Time : 2024/6/22 16:26
# @Author:lupeng
# @File : 数据可视化
import pandas as pd
import matplotlib.pyplot as plt


# 指定一个支持中文的字体，例如SimHei（宋体）
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('../1.csv')

# 绘制散点图
plt.scatter(df['runtime'], df['total_box_office'])
plt.xlabel('电影时长 (分钟)')
plt.ylabel('累加票房 (万元)')
plt.title('电影时长与累加票房的关系')
plt.grid(True)
plt.savefig('电影时长与累加票房的散点图.png')
plt.show()