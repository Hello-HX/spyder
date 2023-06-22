from xml.dom.minidom import parse
from snownlp import SnowNLP
import csv
import xml.etree.ElementTree as ET
import codecs


def analyze_sentiment(text):
    '''
    分析文本的情感倾向，返回情感分析结果（0表示消极，1表示正向）
    '''
    s = SnowNLP(text)
    if s.sentiments > 0.5:
        return 1
    else:
        return 0


def csv_to_xml(csv_file_path, xml_file_path):
    with codecs.open(csv_file_path, 'r', 'utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        root = ET.Element('data')

        for row in csv_reader:
            element = ET.SubElement(root, 'sentence')
            weibo_text = row['微博正文']
            sentiment = analyze_sentiment(weibo_text)
            if sentiment == 1:
                element.set('polarity', 'POS')
            else:
                element.set('polarity', 'NEG')
            element.text = weibo_text

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)


def read_data():
    '''
    读取xml数据 并返回每个有观点的句子的内容及其情感倾向
    '''
    csv_to_xml('香港回归祖国25周年.csv', '香港回归祖国25周年.xml')
    dom = parse('香港回归祖国25周年.xml')
    sentences = dom.getElementsByTagName("sentence")  # 获取所有‘sentence’的节点
    datas = []
    polaritys = []
    for i in range(len(sentences)):
        # 循坏读取列表中的内容 如果句子是观点句 则读取其内容 并读取其情感倾向
        datas.append(sentences[i].firstChild.data)
        # print(sentences[i].firstChild.data)
        polaritys.append(sentences[i].getAttribute('polarity'))
    return datas, polaritys


def sen_main():
    datas, polaritys = read_data()

    pridict_polaritys = []
    true = 0
    for polarity in polaritys:
        if polarity == 'POS':
            true += 1
    # 计算每个句子情感倾向分析的正确性

    print("正向率为 ==> {}".format(true / len(polaritys)))


if __name__ == "__main__":
    sen_main()
