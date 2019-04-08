#coding=utf8

import os
import xml.etree.ElementTree as ET
import cv2

label_xml_path = "/home/mxq/Project/VOC2012_Special/Annotations"
images_path = "/home/mxq/Project/VOC2012_Special/JPEGImages"
images_plot_path = "/media/lab4/F/mxq/datasets/Pedstrain-Car/JPEGImages_bboxes"


def extract_bboxes(xml_name, xml_folder_path):
    """
    :param xml_name:需要进行解析的标定文件的名称
    :param xml_folder_path
    :return: the bboxes
    """
    xml_name_tmp = os.path.join(xml_folder_path, xml_name)

    tree = ET.parse(xml_name_tmp)
    root = tree.getroot()

    bboxes = []
    for obj in root.iter('object'):
        cls = obj.find('name').text
        xmlbox = obj.find('bndbox')

        bbox = {'xmin':int(xmlbox.find('xmin').text),
                'ymin':int(xmlbox.find('ymin').text),
                'xmax':int(xmlbox.find('xmax').text),
                'ymax':int(xmlbox.find('ymax').text)}

        bboxes.append(bbox)

    return bboxes


def draw_bboxes(img, img_name, bboxes):
    for i in range(len(bboxes)):
        xmin = bboxes[i]['xmin']
        ymin = bboxes[i]['ymin']
        xmax = bboxes[i]['xmax']
        ymax = bboxes[i]['ymax']

        cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)

    img_name = os.path.join(images_plot_path, img_name + '.jpg')
    # cv2.imwrite(img_name, img)
    cv2.imshow("img_bboxes", img)
    cv2.waitKey(0)


if __name__ == '__main__':
    labels = os.listdir(label_xml_path)

    print(labels)
    for label in labels:
        bboxes = extract_bboxes(label, label_xml_path)

        image_name = os.path.join(images_path, label.split('.')[0] + '.jpg')
        print(image_name)

        img = cv2.imread(image_name)
        # cv2.imshow("image", img)
        # cv2.waitKey(10)

        draw_bboxes(img, label.split('.')[0] + '.jpg', bboxes)






