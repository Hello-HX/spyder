import re

import pandas as pd

# 读取数据
df = pd.read_csv('双减政策_合并.csv', encoding='utf-8-sig')

# 分词
import jieba

# 停用词
with open('中文停用词表1.txt', encoding='utf-8') as f:
    stopwords = f.read().splitlines()
# 分词
# 去掉非中文字符 去掉@网名

df['text_cut'] = df['text'].apply(lambda x: ''.join(re.findall('[\u4e00-\u9fa5]', x)))
# 去掉收起 这两个字
df['text_cut'] = df['text_cut'].apply(lambda x: x.replace('收起', ''))
# 去掉停用词
df['text_cut'] = df['text_cut'].apply(lambda x: [i for i in jieba.cut(x) if i not in stopwords])
# 去掉单字
df['text_cut'] = df['text_cut'].apply(lambda x: [i for i in x if len(i) > 1])
df['text_cut'] = df['text_cut'].apply(lambda x: ' '.join(x))

# 保存
df.to_csv('双减政策_合并.csv', index=False, encoding='utf-8-sig')
