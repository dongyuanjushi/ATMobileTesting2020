import os
from shutil import copyfile


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
    ori_path = "../data"
    selected_path = "../data"
    select()
