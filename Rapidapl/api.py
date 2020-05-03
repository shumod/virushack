from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
app = Flask(__name__)
api = Api(app)
cameras = [
    {
        "id": 0,
        "camera_ip": "1.11.1.1",
        "camera_port": "9999"
    },
    {
        "id": 1,
        "camera_ip": "1.11.1.2",
        "camera_port": "9998"
    },
    {
        "id": 2,
        "camera_ip": "1.11.1.3",
        "camera_port": "99997"
    },
    {
        "id": 3,
       "camera_ip": "1.11.1.4",
        "camera_port": "9999"
    },
    {
        "id": 4,
        "camera_ip": "1.11.1.5",
        "camera_port": "9999"
    },
    {
        "id": 5,
        "camera_ip": "1.11.1.6",
        "camera_port": "9999"
    },
    {
        "id": 6,
        "camera_ip": "1.11.1.7",
        "camera_port": "9999"
    },
    {
        "id": 7,
        "camera_ip": "1.11.1.8",
        "camera_port": "9999"
    },
    {
        "id": 8,
        "camera_ip": "1.11.1.9",
        "camera_port": "9999"
    },
    {
        "id": 9,
        "camera_ip": "1.11.1.10",
        "camera_port": "9999"
    }
]
class Camera(Resource):
    def get(self, id):
            for camera in cameras:
                if(camera["id"] == id):
                    return camera, 200
            return "Camera not found", 404
api.add_resource(Camera,  "/cameras/<int:id>")
app.run(debug=True)