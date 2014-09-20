import urllib
import requests

def upload(filename):
    with open("path/to/file.png", "rb") as f:
        data = f.read()
        image_data = {
            "api_key": "MlNqKOB0gvIJ9dBz",
            "api_secret": "CWf5gIEQqoo59fRy",
            "jobs": "object_add",
            "base64": encoded
        }
        resp = requests.post('https://rekognition.com/func/api/', params=image_data)
        return resp