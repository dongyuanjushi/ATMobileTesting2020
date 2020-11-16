import json
import os




if __name__ == '__main__':
    classes = {}
    all_data = {}
    base_decoded_path = "../decoded_data"
    count()
    classify()
    with open("count.json","w") as w:
        json.dump(all_data,w)
    for item in classes:
        print(item)
        print(classes[item])
    print(len(classes))