import cv2 as cv2
import mediapipe as mp
import math
import numpy
class HandDetector:

    def __init__(self):

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=False,
                                        max_num_hands=2,
                                        min_detection_confidence=0.5,
                                        min_tracking_confidence=0.5)
        self.mpDraw = mp.solutions.drawing_utils
        self.capture = cv2.VideoCapture(0)

    def findDirection(self):

        ret, img = self.capture.read()

        '''get results from the solution'''
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        # '''
        if self.results.multi_hand_landmarks:
            for single_hand in self.results.multi_hand_landmarks:
                self.mpDraw.draw_landmarks(img, single_hand, self.mpHands.HAND_CONNECTIONS)
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

                '''this condition test if the index finger is streched'''
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
def gen_frames0():
    detector = HandDetector()
    while 1:
        direction = detector.findDirection()
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