import json
import math
import os
import re


def save_and_classify():
    all_path=os.path.join(save_based_path,"all_data.json")
    with open(all_path,"w") as w:
        json.dump(all_decoded_data,w)
    for item in all_decoded_data.values():
        if item["class"] not in classified.keys():
            classified.setdefault(item["class"], 1)
        else:
            classified[item["class"]] += 1
    classified_path = os.path.join(save_based_path, "classified.json")
    with open(classified_path, "w") as w:
        json.dump(classified, w)

def decode_all(base_path):
    for file_name in os.listdir(base_path):
        if file_name.endswith(".json"):
            absolute_file_name = os.path.join(base_path, file_name)
            decoded_data = {}
            with open(absolute_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)["activity"]["root"]
                decode(data["children"], decoded_data)
            all_decoded_data.update(decoded_data)


def check_duplicate(decoded_data, current_bounds):
    res = False
    for index in decoded_data:
        added_bounds = decoded_data[index]["bounds"]
        res = check_bounds(added_bounds, current_bounds)
        if res:
            break
    return res


def decode(data, decoded_data):
    for item in data:
        nobounds = False
        if item == None:
            continue
        elif "bounds" not in item.keys() or item.keys() == None:
            nobounds = True
        if not nobounds:
            is_duplicate = check_duplicate(decoded_data, item["bounds"])
            if "resource-id" not in item.keys():
                if not is_duplicate:
                    combined_class = combine_class(item["class"])
                    if combined_class == "False":
                        continue
                    elif combined_class is None:
                        combined_class = item["class"]
                    decoded_data.setdefault(item["ancestors"][0], {})
                    decoded_data[item["ancestors"][0]].setdefault("bounds", item["bounds"])
                    decoded_data[item["ancestors"][0]].setdefault("class", combined_class)
            else:
                if not is_duplicate:
                    combined_class = combine_class(item["class"])
                    if combined_class == "False":
                        continue
                    elif combined_class is None:
                        combined_class = item["class"]
                    decoded_data.setdefault(item["resource-id"], {})
                    decoded_data[item["resource-id"]].setdefault("bounds", item["bounds"])
                    decoded_data[item["resource-id"]].setdefault("class", combined_class)
        if "children" in item.keys():
            decode(item["children"], decoded_data)


def combine_class(current_class):
    res = None
    for item in match_patterns:
        res = re.match(item, current_class)
        if res is not None:
            res = match_patterns[item]
            break
    return res


def check_bounds(added_bounds, current_bounds):
    [l1, u1, r1, d1] = added_bounds
    [l2, u2, r2, d2] = current_bounds
    left_up_dis = get_distance(l1, u1, l2, u2)
    right_down_dis = get_distance(r1, d1, r2, d2)
    res = left_up_dis <= 150 and right_down_dis <= 150
    return res


def get_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


if __name__ == '__main__':
    all_decoded_data = {}
    classified = {}
    base_path = "../data"
    save_based_path = "../decoded_data"
    match_patterns = {
        r"^(.*)TextView$": "TextView",
        r"^((?!(Text|Image|Card|Item)).)*View$": "View",
        r"^((?!(Linear|Frame)).)*Layout$": "Layout",
        r"^(.*)LinearLayout$": "LinearLayout",
        r"^(.*)FrameLayout$": "FrameLayout",
        r"^(.*)(ImageView|imageview)$": "ImageView",
        r"^(.*)ItemView$": "ItemView",
        r"^(.*)CardView$": "CardView",
        r"^(.*)[B,b]{1}ar$": "Bar",
        r"^((?!(Image|Radio)).)*Button$": "Button",
        r"^(.*)ImageButton$": "ImageButton",
        r"^(.*)RadioButton$": "RadioButton",
        r"^(.*)Spinner$": "Spinner",
        r"^(.*)Switcher$": "Switcher",
        r"^(.*)Card$": "Card",
        r"^(.*)Indicator$": "Indicator",
        r"^(.*)Pager$": "Pager",
        r"^(.*)Picker$": "Picker",
        r"^(.*)EditText$": "EditText",
        r"^[a-z]{1,}": "False",
    }
    # strs=["ArabicTextView"]
    # count=0
    # for str in strs:
    #     for item in match_patterns:
    #         print(re.match(item,str))
    #     count+=1
    #     print(count)
    #     print("Finised:")
    decode_all(base_path)
    save_and_classify()