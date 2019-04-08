import xml.etree.ElementTree as ET
import os
from os import getcwd

sets = ['train', 'val']
# classes
classes = ["Car", "Pedestrian"]
# the path of JPEGImages
image_path = "/media/lab4/F/mxq/autopilot/VOC/JPEGImages"
# the path where you want to put your label files in
label_path = "/media/lab4/F/mxq/autopilot/VOC/labels"
# the path of original annotation
annotation_path = "/media/lab4/F/mxq/autopilot/VOC/Annotation"
# the path where you want to put your image path files in
image_path_path = "/media/lab4/F/mxq/autopilot/VOC/image_path"
# the path of train.txt and val.txt
dataset_separate_path = "/media/lab4/F/mxq/autopilot/VOC/ImageSets/Main"


def convert(size, box):
    dw = 1./(size[0])
    dh = 1./(size[1])
    x = (box[0] + box[1])/2.0 - 1
    y = (box[2] + box[3])/2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return x, y, w, h


def convert_annotation(image_id):
    in_file_name = os.path.join(annotation_path, image_id + '.xml')
    out_file_name = os.path.join(label_path, image_id + '.txt')
    in_file = open(in_file_name)
    out_file = open(out_file_name, 'w')

    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')


# the current working dirt
wd = getcwd()

for image_set in sets:
    if not os.path.exists(label_path):
        os.makedirs(label_path)

    image_set_txt = os.path.join(dataset_separate_path, image_set + '.txt')
    list_file_txt = os.path.join(image_path_path, image_set + '.txt')
    image_ids = open(image_set_txt).read().strip().split()
    list_file = open(list_file_txt, 'w')

    for image_id in image_ids:
        print("image:", image_id)
        image_path_0 = os.path.join(image_path, image_id + '.jpg')
        print(image_path_0)
        list_file.write(image_path_0 + '\n')
        # convert_annotation(image_id)
    list_file.close()

# os.system("cat 2007_train.txt 2007_val.txt 2012_train.txt 2012_val.txt > train.txt")
# os.system("cat 2007_train.txt 2007_val.txt 2007_test.txt 2012_train.txt 2012_val.txt > train.all.txt")

