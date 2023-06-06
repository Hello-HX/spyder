import os
from get_weibos import get_weibos, get_date_range_list
from get_comments import get_comments
from concurrent.futures import ThreadPoolExecutor
import pandas as pd


def run_web(keyword="双减政策"):
    print("正在爬取网页数据：保存为json文件和csv文件")
    save_csv_path1 = keyword + ".csv"  # 保存的文件名
    save_json_path = keyword + ".json"  # 保存json
    start_date = "2022-06-28"  # 开始日期
    end_date = "2022-06-29"  # 结束日期
    days = 1  # 时间间隔
    date_ranges = get_date_range_list(start_date, end_date, days)  # 日期范围
    count = 0
    max_count = 15000
    if os.path.exists(save_csv_path1):
        df = pd.read_csv(save_csv_path1, encoding="utf_8_sig")
        # 计算有 多少条
        count = df.shape[0]
        print("已经爬取了{}条".format(count))

    get_weibos_generator = get_weibos(save_csv_path1, keyword, date_ranges)

    for weibos in get_weibos_generator:
        df = pd.DataFrame(weibos)
        df.to_csv(save_csv_path1, mode='a', index=False, header=not os.path.exists(save_csv_path1),
                  encoding="utf_8_sig")
        count += len(weibos)
        if count % 10 == 0:
            print("已经爬取了{}条".format(count))

    if os.path.exists(save_csv_path1):
        df = pd.read_csv(save_csv_path1, encoding="utf_8_sig")
        # 计算有 多少条
        count = df.shape[0]
        print("已经爬取了{}条".format(count))

    get_weibos(save_csv_path1, keyword, date_ranges)

    # 所有页数的数据都保存到同一个JSON文件中
    df = pd.read_csv(save_csv_path1, encoding="utf_8_sig")
    df.to_json(save_json_path, orient="records", force_ascii=False)

    # 读取JSON文件为DataFrame
    df = pd.read_json(save_json_path)
    # 获取mid属性的值
    mids = df["mid"].tolist()


def web_comment(keyword="双减政策"):
    save_csv_path1 = keyword + ".csv"  # 保存的文件名
    save_csv_path2 = keyword + "_comment.csv"  # 微博评论保存的文件名
    save_json_path = keyword + ".json"  # 保存json
    count = 0
    max_count = 1500
    # 读取csv文件为DataFrame
    df = pd.read_csv(save_csv_path1)
    # 获取mid属性的值
    mids = df["mid"].tolist()
    for id in mids:
        result = get_comments(id)
        get_comments(str(id))
        comments = []
        comments.extend(result)
        count += len(comments)
        df_comment = pd.DataFrame(comments)
        df_comment.to_csv(save_csv_path2, mode='a', index=False, header=not os.path.exists(save_csv_path2),encoding="utf_8_sig")
        if count >= max_count:
            break


if __name__ == '__main__':
    #keyword = str(input("输入关键字"))
    keyword = "双减政策"
    run_web(keyword)
    web_comment(keyword)

