import cv2 as cv2
import mediapipe as mp
import math
import random
import numpy


class HandDetector:

    def __init__(self):

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

        '''We cannot tell apart the hands on the screen, so we iterate it for every hand detected'''
        if self.results.multi_hand_landmarks:
            for myHand in self.results.multi_hand_landmarks:

                '''landmark of MCP, PIP, and TIP of the index finger'''
                lm_mcp = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_MCP]
                lm_pip = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_PIP]
                lm_tip = myHand.landmark[self.mpHands.HandLandmark.INDEX_FINGER_TIP]

                '''the distance from PIP and TIP to MCP'''
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
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')



