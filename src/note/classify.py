import json
import os


def count():
    for file in os.listdir(base_decoded_path):
        absolute_path=os.path.join(base_decoded_path,file)
        with open(absolute_path,"r",encoding="utf-8") as f:
            data=json.load(f)
            all_data.setdefault(file,len(data))
def classify():
    for item in all_data.values():
        if item["class"] not in classes.keys():
            classes.setdefault(item["class"],1)
        else:
            classes[item["class"]]+=1

if __name__ == '__main__':
    classes = {}
    all_data = {}
    base_decoded_path = "../decoded_data"
    count()
    # classify()
    with open("count.json","w") as w:
        json.dump(all_data,w)