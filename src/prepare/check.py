import cv2
import os


def check(base_path):
    for file in os.listdir(base_path):
        if file.endswith(".jpg"):
            img_path = os.path.join(base_path, file)
            img = cv2.imread(img_path)
            img = cv2.resize(img, (1080, 1920))
            cv2.imwrite(img_path, img)


if __name__ == '__main__':
    base_path = "../test_data"
    check(base_path)
