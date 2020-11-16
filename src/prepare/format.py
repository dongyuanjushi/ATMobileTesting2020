import os


def rename(img_path):
    image_idx = 1
    json_idx=1
    for item in os.listdir(img_path):
        old_file = os.path.join(img_path, item)
        if item.endswith(".jpg"):
            new_file = os.path.join(img_path, (str(image_idx).zfill(6) + '.jpg'))
            image_idx+=1
            os.rename(old_file, new_file)
        elif item.endswith(".json"):
            new_file = os.path.join(img_path, (str(json_idx).zfill(6) + '.json'))
            json_idx+=1
            os.rename(old_file, new_file)


if __name__ == '__main__':
    origin_img_path = "../data"
    rename(origin_img_path)
