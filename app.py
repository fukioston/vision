from flask import Flask, render_template, Response, jsonify
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
    return render_template("index.html", rotation_angle=generate_rotation_angle, finger_director=get_direction)


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


@app.route('/api/mediapipedirection', methods=['GET'])
def get_direction():
    while 1:
        direction = detector.findDirection()  # 获得手的信息
        if direction:
            data = {'direction': direction}
            return jsonify(data)


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
