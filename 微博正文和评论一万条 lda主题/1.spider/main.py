import os

from get_weibos import get_weibos, get_date_range_list
from get_comments import get_comments
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def run():
    keyword = "双减政策"
    save_csv_path1 = keyword + ".csv"  # 微博文章保存的文件名
    save_csv_path2 = keyword + "_comment.csv"  # 微博评论保存的文件名
    start_date = "2021-07-24"  # 开始日期
    end_date = "2023-05-29"  # 结束日期
    days = 1  # 时间间隔
    date_ranges = get_date_range_list(start_date, end_date, days)  # 日期范围
    count = 0
    # 最大爬取15000条
    max_count = 15000
    if os.path.exists(save_csv_path1):
        df = pd.read_csv(save_csv_path1, encoding="utf_8_sig")
        # 计算有 多少条
        count = df.shape[0]
    if os.path.exists(save_csv_path2):
        df1 = pd.read_csv(save_csv_path2, encoding="utf_8_sig")
        mids = df1["mid"].tolist()
        count += df1.shape[0]
    else:
        mids = []
    print("已经爬取了{}条".format(count))
    get_weibos_generator = get_weibos(save_csv_path1, keyword, date_ranges)
    for weibos in get_weibos_generator:
        df = pd.DataFrame(weibos)
        df.to_csv(save_csv_path1, mode='a', index=False, header=not os.path.exists(save_csv_path1),
                  encoding="utf_8_sig")
        count += len(weibos)
        if count % 10 == 0:
            print("已经爬取了{}条".format(count))
        with ThreadPoolExecutor(max_workers=5) as executor:
            weibos_mids = [weibo["mid"] for weibo in weibos if
                           int(weibo["comments_count"]) > 0 and weibo["mid"] not in mids]
            results = executor.map(get_comments, weibos_mids)
        # 转df
        comments = []
        for result in results:
            comments.extend(result)
        count += len(comments)
        df_comment = pd.DataFrame(comments)
        df_comment.to_csv(save_csv_path2, mode='a', index=False, header=not os.path.exists(save_csv_path2),
                          encoding="utf_8_sig")
        if count >= max_count:
            break


if __name__ == '__main__':
    run()
