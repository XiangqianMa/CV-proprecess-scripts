#coding=utf8
# 本文件的功能为从自动驾驶原始数据中提取二维bounding boxes信息，并按照一定的格式写入txt文件中。
import os

label_txt_path = "/media/lab3/D78F4730A17C1FD2/mxq/datasets/autopilot/training/label_2"
output_txt = "/media/lab3/D78F4730A17C1FD2/mxq/project/data_process/2d_bboxes.txt"


def extract_2d_bboxes(txt_name, output_txt_name):
    """
    :param txt_name:需要进行解析的标定文件的名称
    :param output_txt_name:提取出的坐标存放的txt文件
    :return: 无返回
    """
    txt_name_tmp = os.path.join(label_txt_path, txt_name)
    with open(txt_name_tmp) as file:
        for line in file:
            class_name = line.split(' ')[0]
            # 给出的是左上,右下坐标
            left = line.split(' ')[4]
            top = line.split(' ')[5]
            right = line.split(' ')[6]
            bottom = line.split(' ')[7]
            if class_name == "Pedestrian" or class_name == "Car":
                with open(output_txt_name, 'a') as output_file:
                    output_file.writelines(txt_name.split('.')[0] + '.png' + ' ' + class_name + ' ' + left + ' ' + top + ' ' +
                                           right + ' ' + bottom + '\n')


def write_output_file(label_path, output_txt_name):
    txt_names = os.listdir(label_path)
    for txt_name in txt_names:
        print("extract txt file:", txt_name)
        extract_2d_bboxes(txt_name, output_txt_name)
    print("Finished")


if __name__ == '__main__':
    write_output_file(label_txt_path, output_txt)

