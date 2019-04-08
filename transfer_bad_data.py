import imghdr
import os
import struct
import cv2

###################################################
# 功能：查找数据集中存储格式错误的图片，并将其转换为统一的格式
###################################################

# 数据集存放路径
image_path = "/media/mxq/数据/DataSets/Tianchi/IJCAI_2019_AAAC_train"
# 数据集路径下是否有子文件夹，有则设置该参数为True，否则为False
sub_dir_exit = True
# 目标格式
dir_format = "jpg"
type_dict = {
 
    'FFD8FF':'jpg','89504E47':'png','47494638':'gif','49492A00':'tif',
    '424D':'bmp','41433130':'dwg','38425053':'psd','7B5C727466':'rtf','3C3F786D6C':'xml',
    '68746D6C3E':'html','44656C69766572792D646174653A':'eml','CFAD12FEC5FD746F':'dbx','2142444E':'pst',
    'D0CF11E0':'doc/xls','5374616E64617264204A':'mdb','FF575043':'wpd','252150532D41646F6265':'ps/eps',
    '255044462D312E':'pdf','AC9EBD8F':'qdf','E3828596':'pwl','504B0304':'zip',
    '52617221':'rar','57415645':'wav','41564920':'avi','2E7261FD':'ram',
    '2E524D46':'rm','000001BA':'mpg','000001B3':'mpg','6D6F6F76':'mov','3026B2758E66CF11':'asf','4D546864':'mid'
}
 
#转成16进制字符串
def bytes2hex(bytes):
    num = len(bytes)
    hexstr = u""
    for i in range(num):
        t = u"%x" % bytes[i]
        if len(t) % 2:
            hexstr += u"0"
        hexstr += t
    return hexstr.upper()
 
#获得类型
def get_filetype(filename):
    file = open(filename,'rb')
    ftype = 'unknown'
 
    for k,v in type_dict.items():
        # 16进制每一位占4位
        num_bytes = int(len(k)/2)
        file.seek(0)
        # 一个byte占8位(一个字节)，故两个十六进制所占的位数相当于一个char，
        # 所以从文件中读取char时，对应的二进制位数需要减半
        hbytes = struct.unpack('B'*num_bytes, file.read(num_bytes))
        code = bytes2hex(hbytes)
        if code == k:
            ftype =  v
            break
 
    file.close()
    return ftype


def modify_image_formate(image_name, origin_format, format='.jpg'):
    '''修改图片为正确的存储格式

    origin_format:图片的正确格式
    image_name: 待修改的图片的存储路径
    format:　目标格式
    
    '''
    if origin_format == 'png' or origin_format == 'bmp':
        image = cv2.imread(image_name)
        dir_image_name = image_name.split('.')[0] + format

        os.remove(dir_image_name)
        cv2.imwrite(dir_image_name, image)
    elif origin_format == 'gif':
        gif = cv2.VideoCapture(image_name)
        success, frame = gif.read()
        while(success):
            dir_image_name = image_name.split('.')[0] + format

            os.remove(dir_image_name)
            cv2.imwrite(dir_image_name, frame)
            success, frame = gif.read()
        
        gif.release()


if __name__ == "__main__":

    if sub_dir_exit:
        sub_dirs = os.listdir(image_path)
    else:
        sub_dirs = image_path

    for sub_dir in sub_dirs:
        print("------------{}----------".format(sub_dir))
        if sub_dir_exit:
            image_names = os.listdir(os.path.join(image_path, sub_dir))
        else:
            image_names = sub_dir

        for image_name in image_names:
            if sub_dir_exit:
                image_full_name = os.path.join(image_path, sub_dir, image_name)
            else:
                image_full_name = os.path.join(sub_dir, image_name)
            
            image_type = get_filetype(image_full_name)

            # 图片存储格式正确时，跳过当前图片，否则修改图片存储格式
            if image_type is dir_format:
                continue
            else:
                print("Modifing {}, it's right format is: {}.".format(image_full_name, image_type))
                modify_image_formate(image_full_name, origin_format=image_type, format='.jpg')
        