# _*_coding:UTF-8 _*_
# @Time : 2024/6/21 22:21
# @Author:lupeng
# @File : 数据可视化3
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
df = pd.read_csv('../1.csv')



# 提取'name'列
names = df['name']

# 定义词云参数并生成词云，增加最大词数和图的尺寸
wordcloud = WordCloud(
    font_path="msyh.ttc",  # 字体文件路径
    max_words=100,         # 增加最大显示词数
    width=1500,            # 增加图像宽度
    height=1200,           # 增加图像高度
    background_color="white",
    colormap='tab20'
).generate(' '.join(names))

# 显示词云图，增大图表尺寸
plt.figure(figsize=(15, 12))  # 增大显示窗口尺寸
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.savefig('类型词云图.png')
plt.show()