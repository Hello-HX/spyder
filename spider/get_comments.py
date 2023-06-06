from pyquery import PyQuery as pq
import requests

# 隧道域名:端口号
tunnel = "k321.kdltps.com:15818"

# 白名单方式（需提前设置白名单）
proxies = {
    "http": "http://%(proxy)s/" % {"proxy": tunnel},
    "https": "http://%(proxy)s/" % {"proxy": tunnel}
}


headers = {
    "authority": "weibo.com",
    "accept": "application/json, text/plain, */*",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "client-version": "v2.40.21",
    "pragma": "no-cache",
    "sec-ch-ua": "^\\^Google",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "^\\^Windows^^",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "server-version": "v2023.03.31.2",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}
url = "https://weibo.com/ajax/statuses/buildComments"


def get_total_number(weibo_id):
    params = {
        "flow": "0",
        "is_reload": "1",
        "id": weibo_id,
        "is_show_bulletin": "2",
        "is_mix": "0",
        "max_id": "",
        "count": "20",
        "fetch_level": "0"
    }
    while True:
        try:
            #response = requests.get(url, headers=headers, params=params, timeout=2,proxies=proxies)
            response = requests.get(url, headers=headers, params=params, timeout=2)
            if response.json()["ok"] == 1 and response.json()["max_id"] == 0 and response.json()["data"] == []:
                total_number = 0
                data = []
                max_id = 0
                break
            total_number = response.json()["total_number"]
            data = response.json()["data"]
            max_id = response.json()["max_id"]
            break
        except Exception as e:
            # {"ok":1,"data":[],"rootComment":[],"max_id":0,"trendsText":"已加载全部评论"}
            print(weibo_id,e)
            print("Retrying...")
    return total_number, data, max_id


def get_comments(weibo_id):
    comments = []
    total_number, data, max_id = get_total_number(weibo_id)
    for comment in data:
        pq_comment = pq(comment["text"])
        comment["text"] = pq_comment.text()
        comments.append(comment["text"])

    # 如果评论数大于20，那么就需要翻页 且最多25页
    page = total_number // 20
    if page > 25:
        page = 25
    for _ in range(page):
        try_times = 0
        try_max_times = 3
        while True:
            try:
                params = {
                    "flow": "0",
                    "is_reload": "1",
                    "id": weibo_id,
                    "is_mix": "0",
                    "max_id": max_id,
                    "count": "20",
                    "is_show_bulletin": "2",
                    "fetch_level": "0"
                }
                #response = requests.get(url, headers=headers, params=params, timeout=2,proxies=proxies)
                response = requests.get(url, headers=headers, params=params, timeout=2)
                data = response.json()
                max_id = response.json()["max_id"]
                for comment in data["data"]:
                    pq_comment = pq(comment["text"])
                    comment["text"] = pq_comment.text()
                    comments.append(comment["text"])
                break
            except Exception as e:
                print(url)
                print(e)
                print("Retrying...")
                try_times += 1
                if try_times == try_max_times:
                    break

    comments = [comment for comment in comments if comment != ""]
    comments = list(set(comments))
    comments = [{"text": comment, "mid": weibo_id} for comment in comments]
    try:
        print(comments)
    except:
        pass
    return comments


if __name__ == '__main__':
    get_comments("4662792832159536")
