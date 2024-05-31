# coding: utf-8
import json
import eel
import sys
import platform
import os 
# import camera
import base64
import cv2
import requests
import hashlib
from modules import *
import background
background.n = 40
from modules.user_module.user import *
from modules.camera_module.camera import *
import logging
from datetime import date
import time
import subprocess

# overWrite Eel function to close all ports when program ends
def eel_shutdown():
    if len(eel._websockets) == 0:
        print("Video streaming Ends")
        for i in range(1,5):
            try:
                requests.get(f"http://127.0.0.1:800{i}/shutdown")
            except:
                pass    
        #subprocess.call("killport 8001 8002 8003 8004")
        sys.exit()
eel._detect_shutdown = eel_shutdown

today = date.today()
date_now = today.strftime("%d-%m-%Y")
'''
To save logs into a file
'''
# logging.basicConfig(filename='logs/'+str(date_now)+'.log',
#                      filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
#                      level=logging.INFO)

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',level=logging.INFO)
os.environ["cam_key"]="0"
os.environ["cams_list"]="0"
os.environ["stop_key"]="0"

@background.task
def work(i):
    # cmnd=f'py flask_camera{i}.py -p 800{i}'
    cmnd=f'py flask_camera{i}.py'

    subprocess.call(cmnd,shell=True)
    
@background.task
def work2(i):
    # cmnd=f'py flask_camera{i}.py -p 800{i}"'
    cmnd=f'py flask_camera{i}.py'

    subprocess.call(cmnd,shell=True)

@background.task
def work3(i):
    # cmnd=f'py flask_camera.py{i} -p 800{i}'
    cmnd=f'py flask_camera{i}.py'

    subprocess.call(cmnd,shell=True)

@background.task
def work4(i):
    # cmnd=f'py flask_camera.py{i} -p 800{i}'
    cmnd=f'py flask_camera{i}.py'

    subprocess.call(cmnd,shell=True)
    # vid = cv2.VideoCapture("rtsp://admin:Sentry_2020!@166.140.230.62:554/cam/realmonitor?channel=4&subtype=1")
    # while(True):
    #     ret, img = vid.read()
    #     ret, buffer = cv2.imencode('.jpg', img)
    #     img = buffer.tobytes()
    #     blob = base64.b64encode(img)
    #     blob = blob.decode("utf-8")
    #     eel.updateImageSrc3(blob)()

@background.task    
def start_cam(cam_path,i):
    
    url = f"http://127.0.0.1:800{i}/create_record"

    data={
        "cam_path":f"{cam_path}channel={i}&subtype=1"
    }
    res = requests.post(url, json = data)
    res=json.loads(res.text) 
    # requests.get(f"http://127.0.0.1:800{i}/", verify=False, timeout=1)

@background.callback
def work_callback(future):
    print("Worked check please",future.result())

def stop_cam(i):
    # url = f"http://127.0.0.1:800{i}/close"
    url = f"http://127.0.0.1:800{i}/restart"


    res = requests.get(url)
    return res
    # res=json.loads(res.text) 

lstFunc = [0,work, work2 ,work3, work4]  # create list of functions
for x in range(1,5):
    # Start 4 server in bg
    lstFunc[x](x)
def cam_start(cam_path,i):
    url = f"http://127.0.0.1:800{i}/create_record"
    if cam_path.find("http://")>=0:
        data={
        "cam_path":f"{cam_path}{i}/viqcam.mjpg"
        }
    else:
        data={
        "cam_path":f"{cam_path}channel={i}&subtype=1"
        }
    # print(data,"here is data-------")
    try:
        res = requests.post(url, json = data)
        res=json.loads(res.text)
    except:
        print(f"Server-{i} restared")
        lstFunc[i](i)
        cam_start(cam_path,i)     
# @eel.expose
# def video_feed(id):

#     print("Click to Start Cam Id = ",id)
#     # set this into function param
#     data={"id":id}
#     test=time.time()
#     obj=CameraClass()
#     cam_path=obj.get_camera_url(data)

#     for i in range(1,5):
#         # bg task
#         # start_cam(cam_path,i)
#         # simple function
#         cam_start(cam_path,i)

@eel.expose
def video_feed(cam_path):
    print(cam_path)
    video_stop()
    # time.sleep(5)
    r=test_fun()
    if r:
        for i in range(1,5):
            cam_start(cam_path,i)    

        return "Hello" 

def test_fun():
    for i in range(1,5):
        test_rout(i)
    return True    

# @eel.expose
def video_stop():
    print("Click to stop")
    for i in range(1,5):
        stop_cam(i)
        
    return False    
def test_rout(i):
    print("sent_request")
    url = f"http://127.0.0.1:800{i}/test"
    try:
        res = requests.get(url)
        # res.status_code
        res=json.loads(res.text)
        print("helllllllllo",type(res))
        if res==False:
            test_rout(i)
        if res:
            return True
    except:
        test_rout(i)

@eel.expose
def hello():
    eel.hello("Printing Hello from Python")()

def start_eel(arg):
    """Start Eel with either production or development configuration."""

    if arg == '--develop' or arg == '-d':
        """ 
        In this directory you eel file should exist by the name eel.js
        If the file doesn't exist will no longer able to use js expose funtions 
        """
        # directory = 'react_code2/src'
        directory = 'jobsiteui/src'

        app = None
        page = {'port': 3000}
    else:
        # directory = 'react_code2/build'
        directory = 'jobsiteui/build'

        app = 'chrome-app'
        page = 'index.html'
    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html'])
    eel.hello('Python World!')
    eel_kwargs = dict(
        host='localhost',
        port=8888,
        size=(1280, 800),
    )
    try:
        eel.start(page, **eel_kwargs)
        # eel.start(page,mode=app, **eel_kwargs)
    except EnvironmentError:
        # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
        if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
            eel.start(page, mode='edge', **eel_kwargs)
        else:
            raise

if __name__ == '__main__':  
    try:
        arg=sys.argv[1]
    except:
        arg=None    
    start_eel(arg)
    