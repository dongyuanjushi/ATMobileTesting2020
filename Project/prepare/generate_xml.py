import os
import json
from lxml import etree


class GEN_Annotations:
    def __init__(self, filename):
        self.root = etree.Element("annotation")
        child1 = etree.SubElement(self.root, "folder")
        child1.text = "VOC2007"
        child2 = etree.SubElement(self.root, "filename")
        child2.text = filename

    def set_size(self, width, height, channel):
        size = etree.SubElement(self.root, "size")
        widthn = etree.SubElement(size, "width")
        widthn.text = str(width)
        heightn = etree.SubElement(size, "height")
        heightn.text = str(height)
        channeln = etree.SubElement(size, "depth")
        channeln.text = str(channel)

    def savefile(self, filename):
        tree = etree.ElementTree(self.root)
        tree.write(filename, pretty_print=True, xml_declaration=False, encoding='utf-8')

    def add_pic_attr(self, label, xmin, ymin, xmax, ymax):
        object = etree.SubElement(self.root, "object")
        namen = etree.SubElement(object, "name")
        posen = etree.SubElement(object, "pose")
        posen.text = "Unspecified"
        truncated = etree.SubElement(object, "truncated")
        truncated.text = str(0)
        difficult = etree.SubElement(object, "difficult")
        difficult.text = str(0)
        namen.text = label
        bndbox = etree.SubElement(object, "bndbox")
        xminn = etree.SubElement(bndbox, "xmin")
        xminn.text = str(xmin)
        yminn = etree.SubElement(bndbox, "ymin")
        yminn.text = str(ymin)
        xmaxn = etree.SubElement(bndbox, "xmax")
        xmaxn.text = str(xmax)
        ymaxn = etree.SubElement(bndbox, "ymax")
        ymaxn.text = str(ymax)


if __name__ == '__main__':
    decoded_data_path = "../../Data/all_data.json"
    saved_xml_base_path = "../../Data/VOC2007/Annotations"
    with open(decoded_data_path, "r", encoding="utf-8") as f:
        all_data = json.load(f)
        for item in all_data:
            saved_xml_path = os.path.join(saved_xml_base_path, item + ".xml")
            filename = item + ".jpg"
            anno = GEN_Annotations(filename)
            anno.set_size(1080, 1920, 3)
            data = all_data[item]
            for widget in data.values():
                label = widget["class"]
                [xmin, ymin, xmax, ymax] = widget["bounds"]
                anno.add_pic_attr(label, xmin, ymin, xmax, ymax)
            anno.savefile(saved_xml_path)
