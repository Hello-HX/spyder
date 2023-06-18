import csv
import os

import pandas as pd

path = "微博话题"
files = os.listdir(path)

# 向csv文件写入表头
header = ["screen_name", "profile_image_url", "location", "created_time", "text"]
f = open(f"微博评论.csv", "w", encoding="utf-8", newline="")
writer = csv.DictWriter(f, header)
writer.writeheader()
f.close()

comment = pd.read_csv("微博评论.csv")

for file in files:
    data = pd.read_csv(os.path.join(path, file))
    comment = pd.concat([comment, data])
    print(comment.shape)

comment.to_csv("微博评论.csv", index_label=False)
