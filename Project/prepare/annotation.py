import cv2
import json
import os


def annotate_all(base_img_path):
    with open(os.path.join(decoded_base_path, "all_data.json"), "r", encoding="utf-8") as f:
        all_data = json.load(f)
        for file_name in os.listdir(base_img_path):
            # if file_name == "000475.jpg":
            if file_name.endswith(".jpg"):
                name = file_name[:len(file_name) - len(".jpg")]
                decoded_data = all_data[name]
                img_path = os.path.join(base_img_path, file_name)
                annotate_img(img_path, name, decoded_data)


def annotate_img(img_path, name, decoded_data):
    img = cv2.imread(img_path)
    for index in decoded_data:
        item = decoded_data[index]
        left_up = (item["bounds"][0], item["bounds"][1])
        right_down = (item["bounds"][2], item["bounds"][3])
        cv2.rectangle(img, left_up, right_down, (255, 0, 0), 4)
        text = item["class"]
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(img, text, (left_up[0] - 1, left_up[1] - 1), font, 1.2, (205, 0, 205), 2)
    annotated_img_path = os.path.join(annotated_base_img_path, name + ".jpg")
    cv2.imwrite(annotated_img_path, img)


if __name__ == '__main__':
    base_img_path = "../../Data/data"
    decoded_base_path = "../../Data/decoded_data"
    annotated_base_img_path = "../../Data/annotated_image"
    annotate_all(base_img_path)
