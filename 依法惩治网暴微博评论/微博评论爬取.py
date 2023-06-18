import random
import re
import time
import csv
from lxml import etree
from urllib.parse import quote

import requests

zero_count = 0
comment_number = 0

headers_com = {
    'Cookie': 'SINAGLOBAL=6436334064314.1.1646568095851; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWF9-RqdikGrxNnlsg0cFsU5JpX5KMhUgL.FoqNSKzRe0zXSo-2dJLoI7f.qPSJqPSJ9J8JMc9y; ULV=1686926687065:38:2:2:234015187507.20163.1686926687061:1686581257227; WBPSESS=iMG6SagG-GcJSPT1i8x5Q11ydOw-8PXwCUeW7GcmwkNdMKzVu-5aDh5SS2Z_GRl5egcFtK3j8HiHLNIEhCSrDLFRyKxhmArBSpP102M2PEOkvczsEeuKEL_fej6KW-Mn3wd2WtzvBFOtTcwnYKU6zg==; XSRF-TOKEN=6WmxVebK2oI3UwFXVGtF6RtB; ALF=1689590468; SSOLoginState=1686998470; SCF=Asc0VprXpN51zMLyEcgVza-2xlaP4FXkWCgxHkGPDAbZb32Re-RUX5oU0DO4Ew-f8J_WQdwWVXTwpgEI2bjVKQY.; SUB=_2A25Jif2XDeRhGeBJ7lAZ8yzIzTmIHXVq_2hfrDV8PUNbmtANLUb4kW9NRldGL14kZQn29D9d21wvBht13tE_N8SZ',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
}


def getArticleId(id_str):
    """
    :param id_str: 需要解密的id字符串
    :return:
    """
    url_id = "https://weibo.com/ajax/statuses/show?id={}".format(id_str)
    resp_id = requests.get(url_id, headers=headers)
    if resp_id is None:
        return  0
    article_id = resp_id.json()["id"]
    return article_id


def get_one_page(params):
    """
    :param params: get请求需要的参数，数据类型为字典
    :return: max_id：请求所需的另一个参数
    """
    url = "https://weibo.com/ajax/statuses/buildComments"
    resp = requests.get(url, headers=headers, params=params)

    data_list = resp.json()["data"]
    global zero_count
    if len(data_list) == 0:
        zero_count += 1
    else:
        zero_count = 0

    global comment_number
    comment_number += len(data_list)
    print("已经爬到的评论数：", comment_number)
    for data in data_list:
        data_dict = {
            "screen_name": data["user"]["screen_name"],
            "profile_image_url": data["user"]["profile_image_url"],
            "location": data["user"]["location"],
            "created_time": data["created_at"].replace("+0800", ""),
            "text": data["text_raw"],
        }
        print(
            f'昵称：{data_dict["screen_name"]}\n头像：{data_dict["profile_image_url"]}\n地址：{data_dict["location"]}\n发布时间：{data_dict["created_time"]}\n评论内容：{data_dict["text"]}')
        print("=" * 90)
        saveData(data_dict)
    max_id = resp.json()["max_id"]
    if max_id:
        return max_id
    else:
        return


def get_all_data(params):
    """
    :param params: get请求需要的参数，数据类型为字典
    :return:
    """
    max_id = get_one_page(params)
    params["max_id"] = max_id
    params["count"] = 20
    while max_id:
        if zero_count == 20:
            break
        params["max_id"] = max_id
        time.sleep(.5)
        max_id = get_one_page(params)


def saveData(data_dict):
    """
    :param data_dict: 要保存的数据，形式为dict类型
    :return:
    """
    writer.writerow(data_dict)


if __name__ == '__main__':
    uid = '2656274875'
    baseUrl = 'https://s.weibo.com/weibo?q={}&Refer=index'
    topic = '#建议出台反网络暴力法你支持吗#'  # 爬取的话题
    fileName = topic.replace('#', '')

    # 向csv文件写入表头
    header = ["screen_name", "profile_image_url", "location", "created_time", "text"]
    f = open(f"微博话题/{fileName}.csv", "w", encoding="utf-8", newline="")
    writer = csv.DictWriter(f, header)
    writer.writeheader()

    url = baseUrl.format(quote(topic))

    page = 0
    pageCount = 1

    while True:
        page = page + 1
        tempUrl = url + '&page=' + str(page)
        print('-' * 36, tempUrl, '-' * 36)
        response = requests.get(tempUrl, headers=headers_com)
        html = etree.HTML(response.text, parser=etree.HTMLParser(encoding='utf-8'))
        count = len(html.xpath('//div[@class="card-wrap"]')) - 2
        for i in range(1, count + 1):
            # 微博url
            weibo_url = html.xpath(
                '//div[@class="card-wrap"][' + str(
                    i) + ']/div[@class="card"]/div[1]/div[2]/div[@class="from"]/a/@href')

            if len(weibo_url) == 0:
                continue

            url_str = '.*?com\/\d+\/(.*)\?refer_flag=\d+_'
            res = re.findall(url_str, weibo_url[0])
            weibo_url = res[0]

            headers = {
                "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36",
                "x-requested-with": "XMLHttpRequest",
                "referer": "https://weibo.com/2656274875/{}".format(weibo_url),
                "cookie": 'SINAGLOBAL=6436334064314.1.1646568095851; UOR=,,login.sina.com.cn; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWF9-RqdikGrxNnlsg0cFsU5JpX5KMhUgL.FoqNSKzRe0zXSo-2dJLoI7f.qPSJqPSJ9J8JMc9y; ULV=1686926687065:38:2:2:234015187507.20163.1686926687061:1686581257227; WBPSESS=iMG6SagG-GcJSPT1i8x5Q11ydOw-8PXwCUeW7GcmwkNdMKzVu-5aDh5SS2Z_GRl5egcFtK3j8HiHLNIEhCSrDLFRyKxhmArBSpP102M2PEOkvczsEeuKEL_fej6KW-Mn3wd2WtzvBFOtTcwnYKU6zg==; XSRF-TOKEN=6WmxVebK2oI3UwFXVGtF6RtB; ALF=1689590468; SSOLoginState=1686998470; SCF=Asc0VprXpN51zMLyEcgVza-2xlaP4FXkWCgxHkGPDAbZb32Re-RUX5oU0DO4Ew-f8J_WQdwWVXTwpgEI2bjVKQY.; SUB=_2A25Jif2XDeRhGeBJ7lAZ8yzIzTmIHXVq_2hfrDV8PUNbmtANLUb4kW9NRldGL14kZQn29D9d21wvBht13tE_N8SZ',
                "x-xsrf-token": "-YYOKoKzkyMDGhDmhVSCLqpD"
            }

            id = getArticleId(weibo_url)  # 获取参数需要的真正id

            # get请求的参数
            params = {
                "is_reload": 1,
                "id": id,
                "is_show_bulletin": 2,
                "is_mix": 0,
                "count": 10,
                "uid": int(uid)
            }

            get_all_data(params)

        try:
            if pageCount == 1:
                pageA = html.xpath('//*[@id="pl_feedlist_index"]/div[5]/div/a')[0].text
                pageCount = pageCount + 1
            elif pageCount == 50:
                print('没有下一页了')
                break
            else:
                pageA = html.xpath('//*[@id="pl_feedlist_index"]/div[5]/div/a[2]')[0].text
                pageCount = pageCount + 1
        except:
            print('没有下一页了')
            break

    f.close()
    print("数据爬取完毕。")
