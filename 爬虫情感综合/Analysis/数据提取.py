import os
import csv
import pandas as pd

file_paths = ["../初始数据/校方回应食堂饭菜中吃出老鼠头.csv", "../初始数据/市监局回应反复对比确认是鸭脖.csv",
              "../初始数据/高校鼠头事件涉事窗口几乎没人去吃饭.csv",
              "../初始数据/鸭脖或鼠头需要更可信的解释.csv", "../初始数据/江西省教育厅介入鸭脖事件.csv",
              "../初始数据/鼠头鸭脖食堂意见反馈群曝光.csv",
              "../初始数据/鼠头鸭脖学校门口大量学生取外卖.csv", "../初始数据/联合调查组认定饭菜中异物是鼠头.csv",
              "../初始数据/江西全省技工院校开展食品安全专项整治.csv"]
file_paths = ["../初始数据/高校鼠头事件涉事窗口几乎没人去吃饭.csv"]
filename = "../发生期/发生期.csv"

# 向csv文件写入表头
header = ["screen_name", "profile_image_url", "location", "created_time", "text"]
with open(filename, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, header)
    writer.writeheader()

comment = pd.read_csv(filename)

for file_path in file_paths:
    data = pd.read_csv(file_path)
    comment = pd.concat([comment, data])
    print(comment.shape)

comment.to_csv(filename, index_label=False)
