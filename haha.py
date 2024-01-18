# import cv2
# import mediapipe as mp
# from mediapipe.tasks import python
# from mediapipe.tasks.python import vision
#
# # 定义手势识别器相关的类
# import mediapipe as mp
#
# BaseOptions = mp.tasks.BaseOptions
# GestureRecognizer = mp.tasks.vision.GestureRecognizer
# GestureRecognizerOptions = mp.tasks.vision.GestureRecognizerOptions
# VisionRunningMode = mp.tasks.vision.RunningMode
#
# # Create a gesture recognizer instance with the video mode:
# options = GestureRecognizerOptions(
#     base_options=BaseOptions(model_asset_path='static/gesture_recognizer.task'),
#     running_mode=VisionRunningMode.VIDEO)
#
# # 创建手势识别器实例
# with GestureRecognizer.create_from_options(options) as recognizer:
#     # 初始化摄像头
#     cap = cv2.VideoCapture(0)
#     frame_count = 0  # 初始化帧计数器
#     while True:
#     # while cap.isOpened():
#         success, frame = cap.read()
#         imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # cv2图像初始化
#         mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
#         recognition_result = recognizer.recognize_for_video(mp_image, frame_count)
#         frame_count += 1
#         if recognition_result:
#             if recognition_result.gestures:
#                 t = recognition_result.gestures[0][0].category_name
#             else:
#                 t = "none"
#             print(t)
#         # print(t)
#         cv2.putText(frame, t, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
#         cv2.imshow("HandsImage", frame)  # CV2窗体
#         cv2.waitKey(1)  # 关闭窗体
#
#
#     # cap.release()
#     # cv2.destroyAllWindows()
data = [
    [0.100020188, 4.0, 999.7981653, 72.7074256],
    [0.125915414, 4.1, 794.1839426, 57.75472682],
    [0.158514915, 4.2, 630.8554631, 45.87713625],
    [0.199554426, 4.3, 501.1164216, 36.44224025],
    [0.251219067, 4.4, 398.0589575, 28.94768468],
    [0.316259684, 4.5, 316.1958515, 22.99442742],
    [0.398139316, 4.6, 251.1683625, 18.26549164],
    [0.501217585, 4.7, 199.5141492, 14.5090886],
    [0.630982817, 4.8, 158.482921, 11.52521138],
    [0.794344269, 4.9, 125.89, 9.154985603],
    [1, 5.0, 100, 7.272210345],
    [1.2589, 5.1, 79.43442688, 5.776638609],
    [1.58482921, 5.2, 63.09828174, 4.588639772],
    [1.995141492, 5.3, 50.12175847, 3.644959704]
]
x=data[13][3]/1.5
for i in data:
    print("{:.4f}".format(i[3]/x))