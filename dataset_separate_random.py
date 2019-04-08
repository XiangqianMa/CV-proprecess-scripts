import os
import random

image_path = "/media/lab4/F/mxq/autopilot/VOC/JPEGImages"
train_txt_path = "/media/lab4/F/mxq/autopilot/VOC/ImageSets/Main/train.txt"
val_txt_path = "/media/lab4/F/mxq/autopilot/VOC/ImageSets/Main/val.txt"

# the number of images
count = 0
# the ratio of train images
train_ratio = 0.95

images = os.listdir(image_path)
for image in images:
    count = count + 1

# calculate the number of train images according to the train_ratio
train_image_num = int(count * train_ratio)
print("the number of train image:", train_image_num)
image_list = range(1, count + 1)
# select train_image_num images randomly
train_image_list = random.sample(image_list, train_image_num)
val_image_list = []

# put the rest images into val data
for name in image_list:
    if name in train_image_list:
        continue
    else:
        val_image_list.append(name)

with open(train_txt_path, 'w') as train_txt:
    for train_image_name in train_image_list:
        print("write train image name:", train_image_name)
        train_txt.writelines(str(train_image_name) + "\n")

with open(val_txt_path, 'w') as val_txt:
    for val_image_name in val_image_list:
        print("write val image name:", val_image_name)
        val_txt.writelines(str(val_image_name) + "\n")


print(len(val_image_list))
print(len(train_image_list))
