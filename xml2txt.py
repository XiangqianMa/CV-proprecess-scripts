#coding=utf8
# 本文件的功能为从自动驾驶原始数据中提取二维bounding boxes信息，并按照一定的格式写入txt文件中。
import os
import xml.etree.ElementTree as ET

label_xml_path = "/media/mxq/MXQ_RZY/datasets/Pedstrain-Car/Annotation/day-pictures-less"
output_txt = "/media/mxq/MXQ_RZY/datasets/Pedstrain-Car/Annotation/txt/day_less.txt"


def extract_2d_bboxes(xml_name, xml_folder_path, output_txt_name):
    """
    :param xml_name:需要进行解析的标定文件的名称
    :param output_txt_name:提取出的坐标存放的txt文件
    :return: 无返回
    """
    xml_name_tmp = os.path.join(xml_folder_path, xml_name)

    tree = ET.parse(xml_name_tmp)
    root = tree.getroot()

    for obj in root.iter('object'):
        cls = obj.find('name').text
        print(cls)
        xmlbox = obj.find('bndbox')

        with open(output_txt_name, 'a') as output_file:
            output_file.writelines(xml_name.split('.')[0] + '.jpg' + ' ' + cls + ' ' + xmlbox.find('xmin').text + ' '
                                   + xmlbox.find('ymin').text + ' ' + xmlbox.find('xmax').text + ' '
                                   + xmlbox.find('ymax').text + '\n')


def write_output_file(xml_folder_path, output_txt_name):
    xml_names = os.listdir(xml_folder_path)
    for xml_name in xml_names:
        print("extract xml file:", xml_name)
        extract_2d_bboxes(xml_name, xml_folder_path, output_txt_name)
    print("Finished")


if __name__ == '__main__':
    xml_folders = os.listdir(label_xml_path)
    print(output_txt)
    for xml_folder in xml_folders:
        print(xml_folder + ": ")
        write_output_file(os.path.join(label_xml_path, xml_folder), output_txt)

