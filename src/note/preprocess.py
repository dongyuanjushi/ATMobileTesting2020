import json
import math
import os

base_path = "../data"
save_based_path = "../decoded_data"


def decode_all(base_path):
    for file_name in os.listdir(base_path):
        if file_name.endswith(".json"):
            absolute_file_name = os.path.join(base_path, file_name)
            decoded_data = {}
            with open(absolute_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)["activity"]["root"]
                decoded_data.setdefault(data["ancestors"][0], {})
                decoded_data[data["ancestors"][0]].setdefault("bounds", data["bounds"])
                decoded_data[data["ancestors"][0]].setdefault("class", data["class"])
                decode(data["children"], decoded_data)
                f.close()
            save_path = os.path.join(save_based_path, file_name)
            with open(save_path, "w") as w:
                json.dump(decoded_data, w)


def decode(data, decoded_data):
    for item in data:
        nobounds=False
        if item == None:
            continue
        elif "bounds" not in item.keys() or item.keys()==None:
            nobounds=True
        if not nobounds:
            is_duplicate = check_duplicate(decoded_data, item["bounds"])
            if "resource-id" not in item.keys():
                if not is_duplicate:
                    decoded_data.setdefault(item["ancestors"][0], {})
                    decoded_data[item["ancestors"][0]].setdefault("bounds", item["bounds"])
                    len = item["class"].rfind(".")
                    class_type = item["class"][len + 1:]
                    decoded_data[item["ancestors"][0]].setdefault("class", class_type)
            else:
                if not is_duplicate:
                    decoded_data.setdefault(item["resource-id"], {})
                    decoded_data[item["resource-id"]].setdefault("bounds", item["bounds"])
                    len = item["class"].rfind(".")
                    class_type = item["class"][len + 1:]
                    decoded_data[item["resource-id"]].setdefault("class", class_type)
        if "children" in item.keys():
            decode(item["children"], decoded_data)


def check_duplicate(decoded_data, current_bounds):
    res = False
    for index in decoded_data:
        added_bounds = decoded_data[index]["bounds"]
        res = check_bounds(added_bounds, current_bounds)
        if res:
            break
    return res


def check_bounds(added_bounds, current_bounds):
    [l1, u1, r1, d1] = added_bounds
    [l2, u2, r2, d2] = current_bounds
    left_up_dis = get_distance(l1, u1, l2, u2)
    right_down_dis = get_distance(r1, d1, r2, d2)
    return left_up_dis <= 10 and right_down_dis <= 10


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    decode_all(base_path)
