import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 定义手势识别器相关的类
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the video mode:
options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='static/gesture_recognizer.task'),
    running_mode=VisionRunningMode.VIDEO)

# 创建手势识别器实例
with GestureRecognizer.create_from_options(options) as recognizer:
    # 初始化摄像头
    cap = cv2.VideoCapture(0)
    frame_count = 0  # 初始化帧计数器
    while True:
    # while cap.isOpened():
        success, frame = cap.read()
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # cv2图像初始化
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognition_result = recognizer.recognize_for_video(mp_image, frame_count)
        frame_count += 1
        if recognition_result:
            if recognition_result.gestures:
                t = recognition_result.gestures[0][0].category_name
            else:
                t = "none"
            print(t)
        # print(t)
        cv2.putText(frame, t, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.imshow("HandsImage", frame)  # CV2窗体
        cv2.waitKey(1)  # 关闭窗体


    # cap.release()
    # cv2.destroyAllWindows()
