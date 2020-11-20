import json
import math
import os
import re


def save_and_classify():
    all_path = os.path.join(save_based_path, "all_data.json")
    with open(all_path, "w") as w:
        json.dump(all_decoded_data, w)
    all_txt_path = os.path.join(save_based_path, "all_data.txt")
    txt = open(all_txt_path, "w")
    line = ""
    for file in all_decoded_data:
        line += ("Name:" + file + ".jpg\n")
        data = all_decoded_data[file]
        line += ("Bbox数量:" + str(len(data)) + "\n\n")
    txt.write(line)
    txt.close()


def decode_all(base_path):
    for file_name in os.listdir(base_path):
        # if file_name == "000475.json":
        if file_name.endswith(".json"):
            absolute_file_name = os.path.join(base_path, file_name)
            decoded_data = {}
            with open(absolute_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)["activity"]["root"]
                decode(data["children"], decoded_data)
            all_decoded_data.setdefault(file_name[:len(file_name) - len(".json")], decoded_data)


def check_duplicate(decoded_data, item):
    res = False
    removed_id = []
    for index in decoded_data:
        added_bounds = decoded_data[index]["bounds"]
        close = check_dis(added_bounds, item["bounds"])
        if close:
            return close
        inside = check_inside(added_bounds, item["bounds"])
        if inside:
            return inside
        outside = check_inside(item["bounds"], added_bounds)
        if outside:
            if item["class"] != "False" :
                #and priority[item["class"]] >= priority[decoded_data[index]["class"]]
                removed_id.append(index)
            else:
                return res
    for i in removed_id:
        decoded_data.pop(i)
    return res


def check_inside(add_bounds, current_bounds):
    inside = True
    for i in range(4):
        if current_bounds[i] - add_bounds[i] <= 0 or current_bounds[i] - add_bounds[i] >= 500:
            inside = False
            break
    return inside


def decode(data, decoded_data):
    for item in data:
        nobounds = False
        if item is None:
            continue
        elif "bounds" not in item.keys() or item.keys() is None:
            nobounds = True
        if not nobounds:
            resize(item["bounds"])
            combine_class(item)
            is_duplicate = check_duplicate(decoded_data, item)
            if "resource-id" not in item.keys():
                if not is_duplicate:
                    if item["class"] != "False":
                        decoded_data.setdefault(item["ancestors"][0], {})
                        decoded_data[item["ancestors"][0]].setdefault("bounds", item["bounds"])
                        decoded_data[item["ancestors"][0]].setdefault("class", item["class"])
            else:
                if not is_duplicate:
                    if item["class"] != "False":
                        decoded_data.setdefault(item["resource-id"], {})
                        decoded_data[item["resource-id"]].setdefault("bounds", item["bounds"])
                        decoded_data[item["resource-id"]].setdefault("class", item["class"])
        if "children" in item.keys():
            decode(item["children"], decoded_data)


def combine_class(current):
    res = None
    for item in match_patterns:
        res = re.match(item, current["class"])
        if res is not None:
            res = match_patterns[item]
            break
    current["class"] = res


def resize(bounding_box):
    height, width = 1920, 1080
    ori_height, ori_width = 2560, 1440
    for i in range(len(bounding_box)):
        if i % 2 == 0:
            bounding_box[i] = round(bounding_box[i] / ori_width * width)
            bounding_box[i] = bounding_box[i] - 5 if bounding_box[i] == 1080 else bounding_box[i]
        else:
            bounding_box[i] = round(bounding_box[i] / ori_height * height)
            bounding_box[i] = bounding_box[i] - 5 if bounding_box[i] == 1920 else bounding_box[i]
        bounding_box[i] = 5 if bounding_box[i] <= 0 else bounding_box[i]


def check_dis(added_bounds, current_bounds):
    [l1, u1, r1, d1] = added_bounds
    [l2, u2, r2, d2] = current_bounds
    if abs(l2 - r2) <= 15 or abs(d2 - u2) <= 10:
        return True
    if r2 - l2 < 0 or d2 - u2 < 0:
        return True
    left_up_dis = get_distance(l1, u1, l2, u2)
    right_down_dis = get_distance(r1, d1, r2, d2)
    closed_dis = left_up_dis <= 20 or right_down_dis <= 20
    if closed_dis:
        return True
    return False


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    all_decoded_data = {}
    classified = {}
    base_path = "../../Data/data"
    save_based_path = "../../Data/decoded_data"
    # priority = {
    #     "TextView": 1,
    #     "ImageView": 2,
    #     "Button": 3,
    #     "SpecialButton": 4,
    #     "Bar": 5,
    #     "Container": 6,
    # }
    match_patterns = {
        r"^(.*)TextView$": "TextView",
        r"^((?!(Text|Image|Card|Item)).)*View$": "View",
        r"^((?!(Linear|Frame)).)*Layout$": "View",
        r"^(.*)LinearLayout$": "False",
        r"^(.*)FrameLayout$": "False",
        r"^(.*)(ImageView|imageview)$": "ImageView",
        r"^(.*)ItemView$": "ItemView",
        r"^(.*)CardView$": "CardView",
        r"^(.*)[B,b]{1}ar$": "Bar",
        r"^((?!(Image|Radio)).)*Button$": "Button",
        r"^(.*)ImageButton$": "ImageButton",
        r"^(.*)RadioButton$": "RadioButton",
        r"^(.*)Spinner$": "Spinner",
        r"^(.*)Switcher$": "Switcher",
        r"^(.*)Indicator$": "Indicator",
        r"^(.*)Pager$": "Pager",
        r"^(.*)Picker$": "Picker",
        r"^(.*)EditText$": "EditText",
        r"^[a-z]{1,}": "False",
        r"X\.[0-9]*": "False",
        "DragandDrop.PagedDragDropGrid": "False",
        "DragandDrop.DragDropGrid": "False"
    }
    decode_all(base_path)
    save_and_classify()
