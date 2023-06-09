import pandas as pd

df1 = pd.read_csv('双减政策.csv', encoding='utf-8')
df1 = df1[['mid', 'p_text']]
# 重命名
df1.rename(columns={'p_text': 'text'}, inplace=True)
df2 = pd.read_csv('双减政策_comment.csv', encoding='utf-8')
df2 = df2[['mid', 'text']]

df = pd.concat([df1, df2], axis=0)
df.to_csv('双减政策_合并.csv', index=False, encoding='utf-8-sig')

