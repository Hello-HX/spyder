import re

import pandas as pd

import jieba
from snownlp import SnowNLP
from wordcloud import WordCloud
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']

from collections import Counter
path = '../爆发期/'
filename = path + '爆发期.csv'
posname = path + '积极评论词云.png'
negname = path + '消极评论词云.png'
imagename = path + '词频图.png'
ansname = path + '情感词频图.png'
data = pd.read_csv(filename)

comments = data['text']

comments = comments.drop_duplicates()
print(comments.head())

# 加载停用词表
stopwords_file = 'stopwords.txt'
with open(stopwords_file, "r", encoding='utf-8') as words:
    stopwords = [i.strip() for i in words]
stopwords.extend(['好感兴趣', '已开通超话社区', '转发微博', '图片评论', '已开通了超话社区'])


def clean(text):
    text = re.sub(r"(回复)?(//)?\s*@\S*?\s*(:| |$)", " ", text)  # 去除正文中的@和回复/转发中的用户名
    text = re.sub(r"\[\S+\]", "", text)  # 去除表情符号
    URL_REGEX = re.compile(
        r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))',
        re.IGNORECASE)
    text = re.sub(URL_REGEX, "", text)  # 去除网址

    # 去除符号
    for ch in "。，：；{|}（）()+-*&……%￥#@！~·`、【】[];:?？《》<>,.":
        text = text.replace(ch, '')

    # 去除停用词
    for word in stopwords:
        text = text.replace(word, '')

    text = re.sub(r"\s+", " ", text)  # 合并正文中过多的空格
    text = text.replace(" ", "")  # 去除无意义的词语
    return text.strip()


clean_comments = []
for comment in comments:
    comment = clean(comment)
    clean_comments.append(comment)

# 对评论进行分词,去除一些停用词
segmented_comments = []
for comment in clean_comments:
    if len(comment) == 0:
        continue
    seg_list = "".join(jieba.cut(comment))
    segmented_comments.append(seg_list)

print(segmented_comments)


# 进行情感倾向分析
def analyze_sentiment(text):
    s = SnowNLP(text)
    return s.sentiments


# 分析每条评论的情感倾向得分
sentiment_scores = [analyze_sentiment(comment) for comment in segmented_comments]

# 根据情感倾向分数将评论分类为积极和消极
positive_comments = [comment for comment, score in zip(segmented_comments, sentiment_scores) if score >= 0.5]
negative_comments = [comment for comment, score in zip(segmented_comments, sentiment_scores) if score < 0.5]

# 绘制积极和消极两类词云图
def generate_wordcloud_pos(text):
    wordcloud = WordCloud(min_font_size=20, max_font_size=100, font_path="simhei.ttf", background_color='white',
                          width=800, height=800, max_words=100).generate(text)
    plt.figure(figsize=(10, 10),dpi=100)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(posname)
    plt.show()

def generate_wordcloud_neg(text):
    wordcloud = WordCloud( min_font_size=20,max_font_size=100,font_path="simhei.ttf", background_color='white',
                           width=800,height=800,max_words=100).generate(text)
    plt.figure(figsize=(10, 10),dpi=200)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.savefig(negname)
    plt.show()


# 绘制积极评论词云图
positive_text = ' '.join(positive_comments)
generate_wordcloud_pos(positive_text)

# 绘制消极评论词云图
negative_text = ' '.join(negative_comments)
generate_wordcloud_neg(negative_text)


def plot_word_frequency(text):
    word_list = jieba.lcut(text)
    word_counter = Counter(word_list)
    word_freq = word_counter.most_common(21)[1:21]  # 取出现频率最高的前20个词语及其频次
    words, freqs = zip(*word_freq)

    plt.figure(figsize=(10, 6))
    plt.bar(words, freqs)
    plt.xticks(rotation=45)
    plt.xlabel('词语')
    plt.ylabel('频次')
    plt.title('评论词语频次图')
    plt.savefig(imagename)
    plt.show()


import matplotlib.pyplot as plt
from collections import Counter
import jieba
import snownlp


def plot_word_sentiment(text):
    word_list = jieba.lcut(text)
    word_sentiments = []  # 存储每个词语的情感值
    for word in word_list:
        sentiment = snownlp.SnowNLP(word).sentiments
        word_sentiments.append(sentiment)

    # 将情感值分为积极、消极、中性三类
    positive_words = [word_list[i] for i in range(len(word_list)) if word_sentiments[i] > 0.66]
    neutral_words = [word_list[i] for i in range(len(word_list)) if 0.33 <= word_sentiments[i] <= 0.66]
    negative_words = [word_list[i] for i in range(len(word_list)) if word_sentiments[i] < 0.33]

    # 统计每类词语的频次
    positive_freqs = Counter(positive_words)
    neutral_freqs = Counter(neutral_words)
    negative_freqs = Counter(negative_words)

    # 取出现频率最高的前20个词语及其频次
    positive_word_freq = positive_freqs.most_common(8)[1:9]
    neutral_word_freq = neutral_freqs.most_common(8)[1:9]
    negative_word_freq = negative_freqs.most_common(8)[1:9]

    # 提取词语和频次
    positive_words, positive_freqs = zip(*positive_word_freq)
    neutral_words, neutral_freqs = zip(*neutral_word_freq)
    negative_words, negative_freqs = zip(*negative_word_freq)

    # 绘制柱形图
    plt.figure(figsize=(16, 8))
    plt.bar(positive_words, positive_freqs, color='pink', label='positive')
    plt.bar(neutral_words, neutral_freqs, color='lightgrey', label='neutral')
    plt.bar(negative_words, negative_freqs, color='indianred', label='negative')
    plt.xticks(rotation=45)
    plt.xlabel('词语')
    plt.ylabel('频次')
    plt.title('评论词语情感分析')
    plt.legend(loc='upper right')
    plt.annotate('positive words', xy=(0.85, 0.92), xycoords='axes fraction', color='pink', fontsize=12)
    plt.annotate('neutral words', xy=(0.85, 0.88), xycoords='axes fraction', color='lightgrey', fontsize=12)
    plt.annotate('negative words', xy=(0.85, 0.84), xycoords='axes fraction', color='indianred', fontsize=12)
    plt.savefig(ansname)
    plt.show()


# 绘制总的词频图
total_text = ' '.join(clean_comments)
plot_word_frequency(total_text)
plot_word_sentiment(total_text)
