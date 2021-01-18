import os
from re import search

tar = "D:/Movies/"

for dirname, dirpath, filename in os.walk(tar):
    # print("dirname: ", dirname)
    # print("filename: ", filename)
    # for file in dirname:
    if search(r"Thor", dirname):
        print(f"{dirname}")
        break
    print("dirpath: ", dirpath)