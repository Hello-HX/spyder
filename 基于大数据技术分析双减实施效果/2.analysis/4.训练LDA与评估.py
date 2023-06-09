import webbrowser
from multiprocessing import freeze_support
import gensim
from gensim import corpora
from gensim.models import CoherenceModel
from pprint import pprint
import pandas as pd

df = pd.read_csv("双减政策_合并.csv", encoding="utf-8-sig")
# 去掉空值
df.dropna(inplace=True)

documents = df["text_cut"].tolist()
# 预处理你的文本数据
texts = [[text for text in doc.split()] for doc in documents]

# 创建字典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

num_topics = 10
# 选择迭代次数为15
passes = 15


def train_main():
    # 训练
    model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
    # 保存模型
    model.save('model.lda')
    # 保存字典
    dictionary.save('dictionary.dict')

    # 打印主题
    pprint(model.print_topics(num_topics=num_topics, num_words=10))

    # 保存主题
    topics = model.print_topics(num_topics=num_topics, num_words=10)
    with open("topics.txt", "w", encoding="utf-8-sig") as f:
        for topic in topics:
            f.write(str(topic) + "\n")

    # 评估
    # 计算一致性得分
    coherence_model_lda = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)

    # 计算困惑度
    perplexity = model.log_perplexity(corpus)
    print('\nPerplexity: ', perplexity)

    topic_table = pd.DataFrame(columns=['Word Rank'])
    for i in range(model.num_topics):
        topic = model.show_topic(i, 10)
        words = [word for word, prob in topic]
        probs = [prob for word, prob in topic]
        topic_table['Topic {} Word'.format(i)] = words
        topic_table['Topic {} Probability'.format(i)] = probs

    # 生成html 展示主题
    html_table = topic_table.to_html()
    with open('topic_table.html', 'w') as f:
        f.write(html_table)

    # 自动打开 HTML 文件
    webbrowser.open('topic_table.html')


# 一致性得分:  0.5453528368432143
#
# 困惑度:  -8.96735138803919

if __name__ == '__main__':
    freeze_support()
    train_main()
