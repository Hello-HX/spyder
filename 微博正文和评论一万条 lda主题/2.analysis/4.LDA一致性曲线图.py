from multiprocessing import freeze_support

import gensim
from gensim import corpora
from gensim.models import CoherenceModel
from pprint import pprint
import pandas as pd
import webbrowser
import matplotlib.pyplot as plt

df = pd.read_csv("双减政策_合并.csv", encoding="utf-8-sig")
# 去掉空值
df.dropna(inplace=True)

documents = df["text_cut"].tolist()
# 预处理你的文本数据
texts = [[text for text in doc.split()] for doc in documents]

# 创建字典和语料库
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]


# 定义函数以计算一致性得分
def compute_coherence_values(dictionary, corpus, texts, limit, start=2, step=3, passes=15):
    coherence_values = []
    model_list = []
    for num_topics in range(start, limit, step):
        model = gensim.models.ldamodel.LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary, passes=passes)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=texts, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())

    return model_list, coherence_values


def train_main():
    # 使用上述函数计算一致性得分
    start = 2
    limit = 30
    step = 1
    model_list, coherence_values = compute_coherence_values(dictionary=dictionary, corpus=corpus, texts=texts,
                                                            start=start,
                                                            limit=limit, step=step)
    # 绘制一致性得分图
    x = range(start, limit, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    # 保存
    plt.savefig('coherence_values.png')

    # 打印不同主题数的一致性得分
    for m, cv in zip(range(start, limit, step), coherence_values):
        print("Num Topics =", m, " has Coherence Value of", round(cv, 4))

    # 选择一致性得分最高的模型
    optimal_model = model_list[coherence_values.index(max(coherence_values))]

    # 打印最优模型的主题
    pprint(optimal_model.print_topics())
    # 打印主题数
    print("The best number of topics is:", optimal_model.num_topics)


if __name__ == '__main__':
    freeze_support()
    train_main()
