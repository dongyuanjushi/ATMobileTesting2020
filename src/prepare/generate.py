import os
import json

def generate(decoded_data_path,saved_txt_base_path):
    with open(decoded_data_path,"r",encoding="utf-8") as f:
        all_data=json.load(f)
        for item in all_data:
            saved_txt_path=os.path.join(saved_txt_base_path,item+".txt")
            with open(saved_txt_path,"w") as w:
                data=all_data[item]
                line = ""
                for widget in data.values():
                    bounds=widget["bounds"]
                    for b in bounds:
                        line+=str(b)+" "
                    line+=widget["class"]
                    line+="\n"
                w.writelines(line)


if __name__ == '__main__':
    decoded_data_path="../decoded_data/all_data.json"
    saved_txt_base_path="../train"
    generate(decoded_data_path,saved_txt_base_path)