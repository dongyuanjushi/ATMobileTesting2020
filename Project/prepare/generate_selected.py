import os
from shutil import copyfile

# 将标注情况较差的数据从数据集中剔除
def select():
    print(ori_path + "/selected.txt")
    file = open(ori_path + "/selected.txt","r")
    while 1:
        line = file.readline()[:-1]
        if not line:
            break
        data_path = str(line).zfill(6) + ".jpg"
        source = os.path.join(ori_path, data_path)
        target = os.path.join(selected_path, data_path)
        try:
            copyfile(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)
        data_path = str(line).zfill(6) + ".json"
        source = os.path.join(ori_path, data_path)
        target = os.path.join(selected_path, data_path)
        try:
            copyfile(source, target)
        except IOError as e:
            print("Unable to copy file. %s" % e)
            exit(1)


if __name__ == '__main__':
    ori_path = "../../Data/data"
    selected_path = "../../Data/data"
    select()
