"""
Routes and views for the flask application.
"""

from flask import render_template
from VirusHackCv import app
import cv2
import base64
from flask import Flask


@app.route('/')
@app.route('/video_feed')
def cam():
    # пример
    # scr='http://login:pass@IP/vidieo.cgi'
    # или с камеры компа сразу
    src = 0
    capture = cv2.VideoCapture(scr)
    frame = capture.read()[1]
    cnt = cv2.imencode('.png',frame)[1]
    b64 = base64.b64encode(cnt).decode()
    b64_src = 'data:image/png;base64,'
    img_src = b64_src +  b64
    return render_template("outputs.html",user_image=  img_src )
