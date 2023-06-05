import datetime
import os
import re
import time
import requests
import pandas as pd
from pyquery import PyQuery as pq

session = requests.Session()
session.trust_env = False

headers = {
    "authority": "s.weibo.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "max-age=0",
    "sec-ch-ua": "\"Chromium\";v=\"110\", \"Not A(Brand\";v=\"24\", \"Google Chrome\";v=\"110\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
}

cookies = open("cookie.txt", "r").read()
cookies = cookies.split(";")
cookies = [cookie.split("=") for cookie in cookies]
cookies = {cookie[0]: cookie[1] for cookie in cookies}
session.cookies.update(cookies)
session.headers.update(headers)


def get_total_page(keyword, data_range):
    """获取总页数"""
    url = "https://s.weibo.com/weibo"
    params = {
        "q": keyword,
        "typeall": "1",
        "suball": "1",
        "timescope": data_range,
        "Refer": "g",
        "page": str(1)
    }
    response = session.get(url, params=params)
    doc = pq(response.text)
    li_lis = doc("div.m-page ul.s-scroll li").items()
    li_lis = [li for li in li_lis]
    if li_lis:
        last_li = li_lis[-1]
        total_page = last_li("a").text().replace("第", "").replace("页", "")
        return int(total_page)
    if "抱歉，未找到“" in response.text:
        print("时间范围为{}，未找到“{}”相关微博,".format(data_range, keyword, ))
        return 0


def fetch_weibo_list_by_keyword_date_range(keyword, data_range, page):
    """通过关键词和时间范围获取微博列表"""
    url = "https://s.weibo.com/weibo"
    params = {
        "q": keyword,
        "typeall": "1",
        "suball": "1",
        "timescope": data_range,
        "Refer": "g",
        "page": str(page)
    }
    print("正在爬取第{}页,关键词为{},时间范围为{}".format(page, keyword, data_range))
    response = session.get(url, params=params)

    doc = pq(response.text)
    feed_list_items = doc("div.card-wrap").items()
    weibos = []
    for feed in feed_list_items:
        mid = feed.attr("mid")
        uid_reg = re.compile(r"\/\/weibo.com\/(.*?)\?refer_flag=.*?")
        a = feed("a.name")
        screen_name = a.attr("nick-name")
        href = a.attr("href")
        if href is None:
            continue
        uid = uid_reg.findall(href)[0]
        short_p_text = feed("p[@node-type='feed_list_content']").text()
        p_text = feed("p[@node-type='feed_list_content_full']").text() or short_p_text
        # 转评论赞量 card-act
        card_act = feed("div.card-act")
        ul_lis = card_act("ul li").items()
        ul_lis = [li.text() for li in ul_lis]
        reposts_count = str(ul_lis[0] if ul_lis[0].isdigit() else 0)
        comments_count = str(ul_lis[1] if ul_lis[1].isdigit() else 0)
        attitudes_count = str(ul_lis[2] if ul_lis[2].isdigit() else 0)
        dic = {"mid": mid, "uid": uid, "p_text": p_text, "screen_name": screen_name, "reposts_count": reposts_count,
               "comments_count": comments_count, "attitudes_count": attitudes_count}
        weibos.append(dic)

    return weibos


def get_weibos(save_csv_path, keyword, date_ranges):
    # 记录已经爬取的mid
    crawled_mids = []
    if os.path.exists(save_csv_path):
        crawled_mids = pd.read_csv(save_csv_path)["mid"].tolist()
        # 转字符串
        crawled_mids = [str(mid) for mid in crawled_mids]
    for index, date_range in enumerate(date_ranges):
        total_page = get_total_page(keyword, "custom:" + date_range)
        print(keyword, date_range, "总页数为{}".format(total_page))
        if total_page is None:
            continue
        for page in range(1, total_page + 1):
            weibos = fetch_weibo_list_by_keyword_date_range(keyword, "custom:" + date_range, page)
            res = []
            for weibo in weibos:
                mid = weibo["mid"]
                screen_name = weibo["screen_name"]
                if str(mid) in crawled_mids:  # 已经爬取过的mid不再爬取
                    continue
                dic = {"screen_name": screen_name,
                       "date_range": date_range, "total_page": total_page, "current_page": page,
                       "keyword": keyword}
                dic.update(weibo)  # 合并字典
                res.append(dic)
                crawled_mids.append(str(mid))
            yield res


def get_date_range_list(start_date, end_date, days=1):
    """获取时间范围列表 比如 [2020-01-01:2020-01-02,2020-01-02:2020-01-03....]"""
    now_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    num = 0
    date_ranges = []
    while now_date <= end_date:
        num += 1
        last_date = now_date
        now_date = now_date + datetime.timedelta(days=days)  # 日期加days天
        print(str(last_date) + ":" + str(now_date))
        date_ranges.append(str(last_date) + ":" + str(now_date))

    return date_ranges


if __name__ == '__main__':
    keyword = "郑州暴雨"
    save_csv_path = keyword + ".csv"  # 保存的文件名
    start_date = "2022-06-28"  # 开始日期
    end_date = "2022-06-29"  # 结束日期
    days = 1  # 时间间隔
    date_ranges = get_date_range_list(start_date, end_date,days)  # 日期范围
    count = 0
    if os.path.exists(save_csv_path):
        df = pd.read_csv(save_csv_path, encoding="utf_8_sig")
        # 计算有 多少条
        count = df.shape[0]
        print("已经爬取了{}条".format(count))
    get_weibos_generator = get_weibos(save_csv_path, keyword, date_ranges)
    for weibos in get_weibos_generator:
        df = pd.DataFrame(weibos)
        df.to_csv(save_csv_path, mode='a', index=False, header=not os.path.exists(save_csv_path), encoding="utf_8_sig")
        count += len(weibos)
        if count % 10 == 0:
            print("已经爬取了{}条".format(count))

