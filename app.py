import time

from flask import Flask, render_template, Response, jsonify, request
import random
import cv2 as cv2
import mediapipe as mp
import math
import numpy
from views.sight import *
app = Flask(__name__)


# 电脑自带摄像头
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/test2")
def test2():
    return render_template("test2.html", rotation_angle=generate_rotation_angle, finger_director=get_direction)


@app.route('/video_feed0')
def video_feed0():
    return Response(gen_frames0(), mimetype='multipart/x-mixed-replace; boundary=frame')


detector = detector_


@app.route('/api/angle', methods=['GET'])
def generate_rotation_angle():
    rand = random.randint(1, 4)

    data = {'rotation_angle': rand}
    return jsonify(data)

@app.route('/api/number', methods=['GET'])
def generate_number():
    options = [5, 6, 8, 9]

    # 从列表中随机选择一个元素
    rand = random.choice(options)
    data = {'rand': rand}
    return jsonify(data)


@app.route('/api/mediapipedirection', methods=['GET'])
def get_direction():
    while 1:
        direction = detector.findDirection()  # 获得手的信息
        if direction:
            data = {'direction': direction}
            return jsonify(data)
@app.route('/api/mediapipedirection2', methods=['GET'])
def get_direction22():
    x=get_direction2()
    if x:
        return x

error_count = 0
pre_size = -1
best_vision = -1

@app.route('/api/return', methods=['POST', 'GET'])
def estimate_vision():
    global pre_size
    global error_count
    global best_vision
    data_received = request.json

    current_size = data_received.get('distance')  # 注意此处使用正确的键名
    true_or_wrong = data_received.get('answer')  # 注意此处使用正确的键名
    print(current_size)
    print(true_or_wrong)  # 注意此处使用正确的键名


    if pre_size == -1:
        pre_size = current_size

    if error_count == 2:
        data = {'best_vision': best_vision, 'exit': 1}
    else:
        if current_size == pre_size:
            error_count += 1 if not true_or_wrong else 0
            data = {'best_vision': best_vision, 'exit': 0}
        else:
            pre_size = current_size
            pre_size_vision = (pre_size / 400) * 5.0
            best_vision = pre_size_vision if best_vision < pre_size_vision else best_vision
            data = {'best_vision': best_vision, 'exit': 0}

    return jsonify(data)  # 使用jsonify函数返回JSON格式的Response对象


@app.route('/api/mediapipedirection/size', methods=['GET'])
def get_size():
    eyes_detector = EyeDetector()
    while 1:
        E_size = detector.Distance()  # 获得字号大小
        if E_size is not None:
            data = {'E_size': E_size}
            return jsonify(data)


if __name__ == '__main__':
    app.run()
