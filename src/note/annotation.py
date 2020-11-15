import cv2
import json
import os
base_img_path="../data"
decoded_base_path="../decoded_data"
annotated_base_img_path="../annotated_image"

def annotate_all(base_img_path):
    for file_name in os.listdir(base_img_path):
        if file_name.endswith(".jpg"):
            name=file_name[:len(file_name)-len(".jpg")]
            decoded_data_path=os.path.join(decoded_base_path,name+".json")
            with open(decoded_data_path,"r",encoding="utf-8") as f:
                decoded_data=json.load(f)
                absolute_img_path=os.path.join(base_img_path,file_name)
                annotate_img(absolute_img_path,name,decoded_data)
# with open("../data/1.json","r",encoding="utf-8") as f:
#     data=json.load(f)

def annotate_img(img_path,name,decoded_data):
    img=cv2.imread(img_path)
    img=cv2.resize(img,(1440,2560))
    for index in decoded_data:
        item = decoded_data[index]
        left_up = (item["bounds"][0], item["bounds"][1])
        right_down = (item["bounds"][2], item["bounds"][3])
        cv2.rectangle(img, left_up, right_down, (255, 0, 0), 4)
    annotated_img_path=os.path.join(annotated_base_img_path,name+".jpg")
    cv2.imwrite(annotated_img_path, img)




if __name__ == '__main__':
    annotate_all(base_img_path)
