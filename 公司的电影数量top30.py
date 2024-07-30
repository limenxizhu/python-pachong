# _*_coding:UTF-8 _*_
# @Time : 2024/6/22 16:58
# @Author:lupeng
# @File : 数据可视化
import pandas as pd
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../1.csv')

# 对公司列进行词频统计
company_counts = df['company'].value_counts()

# 取前30的公司
top_30_companies = company_counts.head(30)

plt.figure(figsize=(10, 6))
bar_plot = plt.bar(top_30_companies.index, top_30_companies.values)
for bar in bar_plot:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='bottom', ha='center')
# 绘制柱状图

plt.title('公司的电影数量top30')
plt.xlabel('公司')
plt.ylabel('数量')
plt.xticks(rotation=45)  # 旋转标签防止重叠
plt.tight_layout()
plt.savefig('公司的电影数量top30.png')# 自动调整子图参数,使之填充整个图像区域
plt.show()