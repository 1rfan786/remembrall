import urllib
import requests
import os

def upload(filename):
    encoded = urllib.quote(open(filename, "rb").read().encode("base64"))
    params = {
        "api_key": "MlNqKOB0gvIJ9dBz",
        "api_secret": "CWf5gIEQqoo59fRy",
        "jobs": "object_add",
        "base64": encoded,
        "name_space" : "hackathon_testing",
        "user_id": "test",
    }
    resp = requests.request("POST","https://rekognition.com/func/api/index.php", data=params)
    print resp.status_code
    print resp.content
    return resp

def from_cwd(relative_path):
    return os.path.join(os.getcwd(), relative_path.lstrip('\/'))

def analyze(filename):
    encoded = urllib.quote(open(filename, "rb").read().encode("base64"))
    params = {
        "api_key": "MlNqKOB0gvIJ9dBz",
        "api_secret": "CWf5gIEQqoo59fRy",
        "jobs": "scene_understanding_3",
        "base64": encoded,
    }
    resp = requests.request("POST","https://rekognition.com/func/api/index.php", data=params)
    print resp.status_code
    print resp.content
    return resp

analyze("static/pikachu.jpg")