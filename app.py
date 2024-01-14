from flask import Flask, render_template, Response
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


@app.route('/video_feed0')
def video_feed0():
    return Response(gen_frames0(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run()
