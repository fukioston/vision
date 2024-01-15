import cv2 as cv2
import mediapipe as mp
import math
from cvzone.FaceMeshModule import FaceMeshDetector
import random
import numpy


class HandDetector:

    def __init__(self):
        self.my_eyes = mp.solutions.face_mesh
        self.eyes = self.my_eyes.FaceMesh(static_image_mode=True,
                                          max_num_faces=1,
                                          refine_landmarks=True,
                                          min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)
        self.mpHands = mp.solutions.hands  # 初始化手部追踪模块
        self.hands = self.mpHands.Hands(static_image_mode=False,  # 初始化手部追踪对象
                                        max_num_hands=2,
                                        min_detection_confidence=0.5,
                                        min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils  # 绘制手部关键点
        self.capture = cv2.VideoCapture(0)  # 创建一个视频捕获对象

    def findDirection(self):

        ret, img = self.capture.read()  # 从视频中捕获一帧，ret表示帧是否捕获成功，img表示捕获得到的帧数据

        '''get results from the solution'''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 将捕获的帧img的颜色空间从BGR转换为RGB
        self.results = self.hands.process(imgRGB)  # 对处理后的帧进行手部追踪

        # '''
        if self.results.multi_hand_landmarks:  # 检测到手
            for single_hand in self.results.multi_hand_landmarks:  # 遍历每一个手
                self.mpDraw.draw_landmarks(img, single_hand, self.mpHands.HAND_CONNECTIONS)  # 绘制手部关节点间的连线
        # '''

        dirc = None

        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:


                lm_mcp = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_MCP]
                lm_pip = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_PIP]
                lm_tip = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP]

                dist_pip2mcp = math.hypot(lm_pip.x - lm_mcp.x,
                                          lm_pip.y - lm_mcp.y,
                                          lm_pip.z - lm_mcp.z)
                dist_tip2mcp = math.hypot(lm_tip.x - lm_mcp.x,
                                          lm_tip.y - lm_mcp.y,
                                          lm_tip.z - lm_mcp.z)

                '''this condition test if the index finger is stretched'''
                if dist_tip2mcp > 1.8 * dist_pip2mcp:

                    '''the cosine of the angle between the vector from MCP to TIP and the positive direction of X/Y'''
                    cos_x = (lm_tip.x - lm_mcp.x) / dist_tip2mcp
                    cos_y = (lm_tip.y - lm_mcp.y) / dist_tip2mcp

                    '''| 1 - right | 2 - down | 3 - left | 4 - up |'''
                    if cos_x < -0.8:
                        dirc = 1
                    elif cos_y > 0.9:
                        dirc = 2
                    elif cos_x > 0.8:
                        dirc = 3
                    elif cos_y < -0.9:
                        dirc = 4

        return dirc
    def Distance(self):
        face_mesh = self.my_eyes.FaceMesh()

        # 读取帧
        ret, frame = self.capture.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        detector = FaceMeshDetector(maxFaces=1)  # 最多检测一张脸

        img, faces = detector.findFaceMesh(frame, draw=False)  # 不绘制关键点

        # 进行面部追踪
        self.results = face_mesh.process(rgb_frame)

        if self.results.multi_face_landmarks:

            if faces:
                face = faces[0]  # faces是三维列表，我们只需要第一张脸的所有关键点
                # 获取瞳孔的坐标
                left_eye = tuple(face[145])  # 左眼关键点坐标
                right_eye = tuple(face[374])  # 右眼坐标

                # 在图像上绘制瞳孔
                cv2.circle(frame, left_eye, 5, (0, 255, 255), cv2.FILLED)
                cv2.circle(frame, right_eye, 5, (0, 255, 255), cv2.FILLED)

                w, _ = detector.findDistance(right_eye, left_eye)
                W = 6.3  # 人脸两眼之间的平均距离是6.3cm
                foucs = 650  # 摄像头焦距
                dist = int((foucs * W) / w)  # 计算距离

                if dist < 60:  # 返回字号大小
                    E_size = 40
                elif dist > 1000:
                    E_size = 800
                else:
                    E_size = int(dist - dist % 20)
        return E_size

class EyeDetector:
    def __init__(self):
        self.my_eyes = mp.solutions.face_mesh
        self.eyes = self.my_eyes.FaceMesh(static_image_mode=True,
                                          max_num_faces=1,
                                          refine_landmarks=True,
                                          min_detection_confidence=0.5,
                                          min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def Distance(self):
        face_mesh = self.my_eyes.FaceMesh()

        # 读取帧
        ret, frame = self.cap.read()
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        detector = FaceMeshDetector(maxFaces=1)  # 最多检测一张脸

        img, faces = detector.findFaceMesh(frame, draw=False)  # 不绘制关键点

        # 进行面部追踪
        self.results = face_mesh.process(rgb_frame)

        if self.results.multi_face_landmarks:

            if faces:
                face = faces[0]  # faces是三维列表，我们只需要第一张脸的所有关键点
                # 获取瞳孔的坐标
                left_eye = tuple(face[145])  # 左眼关键点坐标
                right_eye = tuple(face[374])  # 右眼坐标

                # 在图像上绘制瞳孔
                cv2.circle(frame, left_eye, 5, (0, 255, 255), cv2.FILLED)
                cv2.circle(frame, right_eye, 5, (0, 255, 255), cv2.FILLED)

                w, _ = detector.findDistance(right_eye, left_eye)
                W = 6.3  # 人脸两眼之间的平均距离是6.3cm
                foucs = 650  # 摄像头焦距
                dist = int((foucs * W) / w)  # 计算距离

                if dist < 60:  # 返回字号大小
                    E_size = 40
                elif dist > 1000:
                    E_size = 800
                else:
                    E_size = int(dist - dist % 20)
        return E_size


detector_ = HandDetector()
def gen_frames0(detector=detector_):
    while 1:
        direction = detector.findDirection()  # 获得手的信息
        if direction is not None:
            print("Detected direction:", direction)
        # 显示图像（可选）
        ret, frame = detector.capture.read()
        ret1, buffer = cv2.imencode('.jpg', frame)
        # 将缓存里的流数据转成字节流
        frame = buffer.tobytes()
        # 指定字节流类型image/jpeg
        # yield (b'--frame\r\n'
        #        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



