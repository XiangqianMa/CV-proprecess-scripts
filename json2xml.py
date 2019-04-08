import json
import os
import cv2
import numpy as np
import shutil
import special_label_voc as slv

cls_name = ["Car", "Pedestrian"]
# json文件存放路径
json_path = "/home/mxq/Project/tiny-yolo/bdd100k/labels"
# xml文件存放路径
xml_path = "/home/mxq/Project/tiny-yolo/bbd100k_xml"
# 图片路径
images_path = ""
# 包含特定目标的图片的存放路径
images_path_ = ""


def json_to_xml(json_file):
    with open(json_file, 'r') as file:
        json_decode = json.load(file)
        # 每一个entity包含一张图片的标定信息
        for entity in json_decode:
            # 图片名称
            image_name = entity['name']
            # 图片下的所有标定
            labels = entity["labels"]
            bboxes = []
            flag = False
            for label in labels:
                if label["category"] == "car":
                    flag = True
                    label_ = "Car"
                    bbox = {"name": label_,
                            'difficult': str(0),
                            'xmin': label["box2d"]["x1"],
                            'ymin': label["box2d"]["y1"],
                            'xmax': label["box2d"]["x2"],
                            'ymax': label["box2d"]["y2"]
                            }
                    bboxes.append(bbox)
                elif label["category"] == "person":
                    flag = True
                    label_ = "Pedestrian"
                    bbox = {"name": label_,
                            'difficult': str(0),
                            'xmin': label["box2d"]["x1"],
                            'ymin': label["box2d"]["y1"],
                            'xmax': label["box2d"]["x2"],
                            'ymax': label["box2d"]["y2"]
                            }
                    bboxes.append(bbox)
                else:
                    continue
            if flag:
                image_name_ = os.path.join(images_path, image_name)
                image = cv2.imread(image_name_)
                size = np.shape(image)
                size = [str(size[0]), str(size[1]), str(size[2])]
                xml_name = image_name.split('.')[0] + '.xml'
                slv.generate_xml(xml_name, bboxes, size, cls_name, xml_path)

                old_image_name = image_name_
                new_image_name = os.path.join(images_path_, image_name)
                # 将样本图片拷贝至指定路径
                shutil.copy(old_image_name, new_image_name)


json_file_name = os.path.join(json_path, "bdd100k_labels_images_val.json")
json_to_xml(json_file_name)




