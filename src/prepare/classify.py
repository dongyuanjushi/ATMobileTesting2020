import json


def classify():
    with open(all_data_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
        for item in all_data.values():
            for widget in item.values():
                if widget["class"] not in classified.keys():
                    classified.setdefault(widget["class"], 1)
                else:
                    classified[widget["class"]] += 1
    with open("classified.txt", "w") as w:
        lines = ""
        for item in classified:
            lines += (item + ":" + str(classified[item]) + "\n")
        w.writelines(lines)


if __name__ == '__main__':
    all_data_path = "../decoded_data/all_data.json"
    classified = {}
    classify()
