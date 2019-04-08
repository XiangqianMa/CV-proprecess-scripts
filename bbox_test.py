import cv2
import numpy as np

image_path = "/home/mxq/Desktop/resize_person.jpg"

x = 0.51
y = 0.50
w = 0.95
h = 0.95

img = cv2.imread(image_path)
height = np.shape(img)[0]
weight = np.shape(img)[1]

print(weight, height)

print(x*weight, y*height, w*weight, h*height)

left = int(x * weight - w * (weight/2))
right = int(x * weight + w * (weight/2))
top = int(y * height - h * (height/2))
bottom = int(y * height + h * (height/2))

cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
cv2.imshow("img1", img)
cv2.waitKey(0)
