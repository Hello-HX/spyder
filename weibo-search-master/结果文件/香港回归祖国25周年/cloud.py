import re
import jieba
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from os import path


d = path.dirname(__file__)
stop = [line.strip() for line in open("part.txt", 'r', encoding='utf-8').readlines()]  # 停用词


def build_key_word(path):  # 通过词频产生特征
    d = {}
    with open(path, encoding="utf-8") as fp:
        for line in fp:
            for word in jieba.cut(line.strip()):
                p = re.compile(r'\w',re.ASCII)
                result = p.sub("", word)
                if not result or result == ' ':  # 空字符
                    continue
                if len(word) > 1:  # 避免大量无意义的词语进入统计范围
                    d[word] = d.get(word, 0) + 1
    kw_list = sorted(d, key=lambda x: d[x], reverse=True)
    size = int(len(kw_list) * 0.2)  # 取最前的30%
    mood = set(kw_list[:size])
    mood_without_stop = list(mood - set(stop))
    temp_list = {}
    for ii in mood_without_stop:
        temp_list[ii] = d[ii]
    return temp_list


wl_space_split = build_key_word("part.txt")
my_wordcloud = WordCloud(background_color='white',  # 设置背景颜色
                         font_path="simhei.ttf",  # 设置字体格式，如不设置显示不了中文
                         max_words=150,
                         max_font_size=150,  # 设置字体最大值
                         random_state=30,  # 设置有多少种随机生成状态，即有多少种配色方案
                         width=1000, height=800,# 设置生成图片的像素高度
                         ).generate_from_frequencies(wl_space_split)
#plt.figure(figsize=(100, 40))
plt.imshow(my_wordcloud)
plt.axis("off")
plt.show()
my_wordcloud.to_file(path.join(d, "out.png"))
