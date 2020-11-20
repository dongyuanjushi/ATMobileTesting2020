from shutil import copyfile
import shutil
import os


def copy():
    for file in os.listdir(img_base_data_path):
        if file.endswith(".jpg"):
            source = os.path.join(img_base_data_path, file)
            target = os.path.join(copy_base_data_path, file)
            try:
                copyfile(source, target)
            except IOError as e:
                print("Unable to copy file. %s" % e)
                exit(1)


if __name__ == '__main__':
    img_base_data_path = "../../Data/data"
    copy_base_data_path = "../../Data/VOC2007/JPEGImages"
    copy()
