import cv2
import numpy as np

image_path = "/home/mxq/Desktop/142.jpg"
image_txt = "/home/mxq/Desktop/image.txt"
img = cv2.imread(image_path)
cv2.imshow("img", img)
# cv2.waitKey(0)
img_width = np.shape(img)[0]
print(img_width)
img_height = np.shape(img)[1]
print(img_height)
img_channel = np.shape(img)[2]
print(img_channel)
img_ = np.reshape(img, [img_width*img_height*3])
# print(img_)
# print(img)
with open(image_txt, "w") as txt:
    for i in range(img_channel):
        for n in range(img_width):
            for j in range(img_height):
                txt.write(str(img[n, j, i]) + "\n")
                print(img[n, j, i])





