#import使用的库文件
#人脸识别使用的库 face_recognition, cv2, numpy
#向云服务器上传照片文件（功能实现sftp）使用的库 paramiko, datetime
#和Arduino的通信（使用GPIO引脚的高低电平实现）使用的库 RPi.GPIO, time
#解决Arduino通信时关门sleep函数引起人脸识别关闭的bug，引入_thread

import face_recognition
import cv2
import numpy as np
import paramiko
import RPi.GPIO as GPIO
import time
from datetime import datetime
import _thread

#初始化GPIO引脚电平为低
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT, initial=GPIO.HIGH)

#定义GPIO变化函数，方便后续多线程处理
def DoorOpenwithGPIO( ):
    #发现已知人脸启动开门动作，10秒后恢复关门状态
    GPIO.output(3,GPIO.LOW)
    time.sleep(10)
    GPIO.output(3,GPIO.HIGH)

#初始化sftp连接，为上传图片做准备
trans = paramiko.Transport('49.235.10.60', 22)
trans.start_client()
trans.auth_password(username='hgf', password='12345hgf')
sftp = paramiko.SFTPClient.from_transport(trans)

#初始化已知人脸
#实例为奥巴马
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]
#宿舍成员真人照片
#hgf_image = face_recognition.load_image_file("hgf.jpg")
#hgf_face_encoding = face_recognition.face_encodings(hgf_image)[0]
#gyw_image = face_recognition.load_image_file("gyw.jpg")
#gyw_face_encoding = face_recognition.face_encodings(gyw_image)[0]
#hy_image = face_recognition.load_image_file("hy.jpg")
#hy_face_encoding = face_recognition.face_encodings(hy_image)[0]
#xqs_image = face_recognition.load_image_file("xqs.jpg")
#xqs_face_encoding = face_recognition.face_encodings(xqs_image)[0]

#已知人脸列表

known_face_encodings = [
    obama_face_encoding
    #hgf_face_encoding，
    #gyw_face_encoding，
    #hy_face_encoding，
    #xqs_face_encoding
]
known_face_names = [
    "Barack Obama"
    #“何公甫”,
    #“郭曜玮”，
    #“黄昱”，
    #“许秋实”
]

#读取摄像头数据
video_capture = cv2.VideoCapture(0)

#初始化变量
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

#人脸识别核心代码（英文注释来自项目face_recognition）
while True:
    # Grab a single frame of video
    ret, frame = video_capture.read()

    # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"


            #同时将陌生人的脸以"年月日_时分秒.jpg"输出，并上传到服务器
            outputfilename = datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
            cv2.imwrite(outputfilename, small_frame)
            outputfilepath = '/home/hgf/human/' + outputfilename
            sftp.put(outputfilename, outputfilepath)


            # # If a match was found in known_face_encodings, just use the first one.
            # if True in matches:
            #     first_match_index = matches.index(True)
            #     name = known_face_names[first_match_index]

            # Or instead, use the known face with the smallest distance to the new face
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                _thread.start_new_thread( DoorOpenwithGPIO, () )        

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




#还原GPIO数据
GPIO.cleanup()

#关闭sftp连接
trans.close()

# Release handle to the webcam
video_capture.release()
cv2.destroyAllWindows()