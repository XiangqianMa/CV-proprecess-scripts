import os
import cv2

videos_path = "/media/mxq/MXQ_RZY/datasets/Pedstrain-Car/night-videos"
image_path = "/media/mxq/MXQ_RZY/datasets/Pedstrain-Car/night-pictures-less"

image_per_frames = 25

videos_files = os.listdir(videos_path)

for video_file in videos_files:
    video = cv2.VideoCapture(videos_path + '/' + video_file)

    if video.isOpened():
        print("Open video successfully.")
        image_number = 0
        frame_number = 0
        not_empty = True
        images_folder = image_path + '/' + video_file.split('.')[0]
        if os.path.exists(images_folder):
            print(images_folder, "exist.")
        else:
            os.mkdir(images_folder)
            print("Make ", images_folder)
        while not_empty:
            not_empty, frame = video.read()
            # cv2.imshow("video", frame)
            # cv2.waitKey(33)
            if frame_number % image_per_frames == 0:
                image_name = images_folder + '/' + video_file.split('.')[0] + '_' + str(image_number) + '.jpg'
                cv2.imwrite(image_name, frame)
                print("Writing image: ", image_name)
                image_number = image_number + 1
            frame_number = frame_number + 1
    else:
        print("Open video file failure, please check your video file: ", video_file)
        break

    print("Capture video", video_file, "successfully.")
    video.release()




