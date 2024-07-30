# _*_coding:UTF-8 _*_
# @Time : 2024/6/21 21:19
# @Author:lupeng
# @File : 猫眼整理
import pandas as pd
df = pd.read_csv('猫眼.csv')
print(df['time'].head())

df['date'] = pd.to_datetime(df['time'], errors='coerce').dt.date
# 验证 date_only 列的数据类型
print(df['date'].dtype)  # 这可能显示为 object，但内容实际上是 datetime.date
# 如果需要，显式地将 date_only 列转换为 datetime.date 类型（通常不是必要的）
# 但这可以确保我们知道列中的确切数据类型
df['date'] = [pd.to_datetime(x, errors='coerce').date() if pd.notnull(pd.to_datetime(x, errors='coerce')) else None
for x in df['time']]
# 或者使用 apply 函数（但通常列表推导式更快）
df['date'] = df['time'].apply(lambda x: pd.to_datetime(x, errors='coerce').date() if pd.notnull(pd.to_datetime(x, errors='coerce')) else None)
df['date'] = df['date'].dt.strftime('%Y-%m-%d') if pd.api.types.is_datetime64_any_dtype(df['date']) else df['date']
# 现在再次检查数据类型（应该仍然是 object，但内容是 datetime.date）
df = df.drop(columns=['time'])



df.drop_duplicates(inplace=True)
# 删除现有的'index'列
df = df.drop(columns=['index'])
# 重置索引
df = df.reset_index(drop=True)
# 添加新的序号列并命名为'index'，并将其置于第一列
df.insert(0, 'index', range(1, len(df) + 1))
# 保存到新文件
df.to_csv('1.csv', index=False, encoding='utf_8_sig')

