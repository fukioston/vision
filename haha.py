import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

# 定义手势识别器相关的类
import mediapipe as mp

BaseOptions = mp.tasks.BaseOptions
GestureRecognizer = mp.tasks.vision.GestureRecognizer
GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
GestureRecognizerResult = mp.tasks.vision.GestureRecognizerResult
VisionRunningMode = mp.tasks.vision.RunningMode

# Create a gesture recognizer instance with the live stream mode:
def print_result(result: GestureRecognizerResult, output_image: mp.Image, timestamp_ms: int):
    if result.gestures:
        t = result.gestures[0][0].category_name
    else:
        t = None

    print("t:", t)
    # print('gesture recognition result: {}'.format(result.gestures))

options = GestureRecognizerOptions(
    base_options=BaseOptions(model_asset_path='gesture_recognizer.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

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
        recognition_result=recognizer.recognize_async(mp_image , frame_count)
        frame_count += 1
        cv2.imshow("HandsImage", frame)  # CV2窗体
        cv2.waitKey(1)  # 关闭窗体
        # if recognition_result.gestures:
        #     top_gesture = recognition_result.gestures[0][0]
        #     hand_landmarks = recognition_result.hand_landmarks
        #     print(top_gesture)


    # cap.release()
    # cv2.destroyAllWindows()
