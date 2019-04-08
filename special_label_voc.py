import os
import xml.etree.ElementTree as ET
import xml.dom.minidom
import shutil
import cv2

# 提取的类别的名称
cls_name = ["car", "person"]
# 原始xml文件的存放路径
label_xml_path = "/home/mxq/Project/VOCdevkit/VOC2012/Annotations"
# 要产生的xml文件的存放路径
label_xml_path_ = "/home/mxq/Project/VOC2012_Special/Annotations"
# 原始图片样本存放的路径
images_path = "/home/mxq/Project/VOCdevkit/VOC2012/JPEGImages"
# 拷贝的目的路径
images_path_ = "/home/mxq/Project/VOC2012_Special/JPEGImages"


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
        difficult = obj.find('difficult').text
        xmlbox = obj.find('bndbox')

        bbox = {'name': cls,
                'difficult': difficult,
                'xmin': int(float(xmlbox.find('xmin').text)),
                'ymin': int(float(xmlbox.find('ymin').text)),
                'xmax': int(float(xmlbox.find('xmax').text)),
                'ymax': int(float(xmlbox.find('ymax').text))}

        bboxes.append(bbox)

    return bboxes


def extract_size(xml_name, xml_folder_path):
    """
    从xml_name文件中提取出图片大小
    :param xml_name: xml文件名
    :param xml_folder_path: xml文件的存放路径
    :return: 图片大小
    """
    xml_name_tmp = os.path.join(xml_folder_path, xml_name)

    tree = ET.parse(xml_name_tmp)
    root = tree.getroot()

    size = root.find('size')
    width = size.find('width').text
    height = size.find('height').text
    depth = size.find('depth').text

    return width, height, depth


def generate_xml(xml_name, bboxes, size, cls_name, label_xml_path):
    """
    生成只包含cls_name中类别的xml文件
    :param xml_name:待生成的xml文件的名称
    :param bboxes:bboxes信息
    :param size:图片大小
    :param cls_name:类别列表
    :param label_xml_path:生成的xml文件的存放路径
    :return:无返回值
    """
    # 解析得到图像大小数据
    width = size[0]
    height = size[1]
    depth = size[2]
    # 要写入的xml文件的名称
    xml_name_ = os.path.join(label_xml_path, xml_name)

    impl = xml.dom.minidom.getDOMImplementation()
    # 设置根节点
    dom = impl.createDocument(None, 'annotation', None)
    root = dom.documentElement

    # 向根节点下添加size字节点
    size_node = dom.createElement('size')
    root.appendChild(size_node)

    # 向size节点下添加width子节点
    width_node = dom.createElement('width')
    width_val = dom.createTextNode(width)
    width_node.appendChild(width_val)
    size_node.appendChild(width_node)

    # 向size节点下添height子节点
    height_node = dom.createElement('height')
    height_val = dom.createTextNode(height)
    height_node.appendChild(height_val)
    size_node.appendChild(height_node)

    # 向size节点下添加depth子节点
    depth_node = dom.createElement('depth')
    depth_val = dom.createTextNode(depth)
    depth_node.appendChild(depth_val)
    size_node.appendChild(depth_node)

    for bbox in bboxes:
        if bbox['name'] in cls_name:
            if bbox['name'] == 'car':
                name = 'Car'
            else:
                name = 'Pedestrian'
            # 向根节点下添加object子节点
            object_node = dom.createElement('object')
            root.appendChild(object_node)

            # 向object节点添加name子节点
            name_node = dom.createElement('name')
            name_val = dom.createTextNode(name)
            name_node.appendChild(name_val)
            object_node.appendChild(name_node)

            # 向object节点添加difficult子节点
            difficult_node = dom.createElement('difficult')
            difficult_val = dom.createTextNode(bbox['difficult'])
            difficult_node.appendChild(difficult_val)
            object_node.appendChild(difficult_node)

            # 向object节点添加bndbox子节点
            bndbox_node = dom.createElement('bndbox')
            object_node.appendChild(bndbox_node)

            # 向bndbox节点扩展xmin子节点
            xmin_node = dom.createElement('xmin')
            xmin_val = dom.createTextNode(str(bbox['xmin']))
            xmin_node.appendChild(xmin_val)
            bndbox_node.appendChild(xmin_node)

            # 向bndbox节点扩展ymin子节点
            ymin_node = dom.createElement('ymin')
            ymin_val = dom.createTextNode(str(bbox['ymin']))
            ymin_node.appendChild(ymin_val)
            bndbox_node.appendChild(ymin_node)

            # 向bndbox节点扩展xmax子节点
            xmax_node = dom.createElement('xmax')
            xmax_val = dom.createTextNode(str(bbox['xmax']))
            xmax_node.appendChild(xmax_val)
            bndbox_node.appendChild(xmax_node)

            # 向bndbox节点扩展ymax子节点
            ymax_node = dom.createElement('ymax')
            ymax_val = dom.createTextNode(str(bbox['ymax']))
            ymax_node.appendChild(ymax_val)
            bndbox_node.appendChild(ymax_node)

    with open(xml_name_, 'w') as file:
        dom.writexml(file, addindent=" ")


if __name__ == '__main__':

    xml_files = os.listdir(label_xml_path)
    for xml_file in xml_files:
        print(xml_file)
        size = extract_size(xml_file, label_xml_path)
        bboxes = extract_bboxes(xml_file, label_xml_path)

        flag = False
        for bbox in bboxes:
            if bbox['name'] in cls_name:
                flag = True
        if flag:
            generate_xml(xml_file, bboxes, size, cls_name, label_xml_path_)
            old_image_name = os.path.join(images_path, xml_file.split('.')[0] + ".jpg")
            new_image_name = os.path.join(images_path_, xml_file.split('.')[0] + ".jpg")
            # 将样本图片拷贝至指定路径
            shutil.copy(old_image_name, new_image_name)
