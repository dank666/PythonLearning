import cv2
from moviepy.video.io.VideoFileClip import VideoFileClip
import pygame
import numpy as np

# 使用已经训练好的人脸检测模型（Haar Cascade）
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

video_path  = '/home/wtejing/Linux/mmexport1711172008306.mp4'

# 用 moviepy 加载视频文件
clip = VideoFileClip(video_path)

# 获取音频
audio = clip.audio  # 属性访问

# 初始化 pygame
pygame.mixer.init()

# 将音频加载到 pygame 中并播放
audio_path = '/home/wtejing/Linux/emp_audio.wav'  # 临时保存音频的路径
audio.write_audiofile(audio_path, codec='pcm_s16le')  # 将音频导出为 .wav 文件，使用 pcm_s16le 编解码器

pygame.mixer.music.load(audio_path)
pygame.mixer.music.play()

# 打开视频
cap = cv2.VideoCapture(video_path)

while True:
    # 捕获视频域
    ret, frame = cap.read()

    # 视频结束
    if not ret:
        print("End of video.")
        break

    # 将图像转换为灰度图，以提高检测效率
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 使用Haar Cascade进行人脸检测
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # 在检测到人脸的地方绘制矩形框
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # OpenCV使用BGR（蓝、绿、红）颜色空间，(255, 0, 0)表示纯蓝色，2表示矩形框的线宽
    
    # 显示结果
    cv2.imshow('Face Detection', frame)

    # 按键退出
    if cv2.waitKey(1) & 0xFF == ord('q'): # 每一毫秒检查一次键盘的输入，按q退出程序
        break

# 释放摄像头，并关闭窗口
cap.release()
cv2.destroyAllWindows()
