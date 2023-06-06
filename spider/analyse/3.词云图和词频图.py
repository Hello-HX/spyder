import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter

# 中文乱码的处理
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

df = pd.read_csv('双减政策_合并.csv', encoding='utf-8-sig')

# 1.词云图
# 统计词频
# 1.1 df 将所有的text_cut拼接成一个字符串

text = ''
for i in df['text_cut']:
    if type(i) == str:
        text += i

# 1.2 词云图
wc = WordCloud(
    background_color='white',
    width=1000,
    height=800,
    # 黑体
    font_path='simhei.ttf',
    # 设置最大词数
    max_words=100,
    # 设置字体最大值
    max_font_size=150,
    # 设置有多少种随机生成状态，即有多少种配色方案
    random_state=30
)
wc.generate_from_text(text)
plt.imshow(wc)
plt.axis('off')
plt.show()

# 2.词频图
# 2.1 统计词频
# 2.1.1 将所有的text_cut拼接成一个字符串
words = []
for i in df['text_cut']:
    if type(i) == str:
        words += i.split(' ')
# 2.1.2 统计词频

word_count = Counter(words)
# 2.1.3 排序
word_count = sorted(word_count.items(), key=lambda x: x[1], reverse=True)
# 2.1.4 取前10个
word_count = word_count[:10]
# 2.1.5 画图
plt.bar(range(len(word_count)), [i[1] for i in word_count], tick_label=[i[0] for i in word_count])
plt.show()
