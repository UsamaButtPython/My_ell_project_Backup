from time import time
from urllib import response
from flask import Flask, Response,redirect, request, jsonify,make_response
import cv2
import argparse
from flask_restful import Resource, Api,reqparse
from flask_cors import CORS
import os, signal 

import os
import sys
import time
import subprocess
from flask import Flask, request, jsonify
from multiprocessing import Process, Queue

some_queue = None

app = Flask(__name__)

print("I'm runing")
# parser = argparse.ArgumentParser(description='Process some integers.')
# parser.add_argument('-p','--port',dest='port',type=str,help='Port',
#                         required=True)
# args = parser.parse_args()
cv_obj=None
cam_path=None
stop_key=0
start=0
dis_img=0
Server_restart=0
#CORS(app)
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers'
    )
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PUT,POST,DELETE,OPTIONS')
    return response




@app.route('/restart')
def restart():
    try:
        some_queue.put("something")
        print("Restarted successfully")
        return "Quit"
    except:
        print("Failed in restart")
        return "Failed"
@app.route('/test')
def test():
    global Server_restart
    if Server_restart==1:
        return (jsonify(True),
                    200)
    return (jsonify(False),
                    200)                

def start_flaskapp(queue):
    global some_queue
    some_queue = queue
    global Server_restart
    Server_restart=1
    app.run(host='0.0.0.0', port=8002)



class VideoCamera(object):
    def __init__(self,cam_num):
        # cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')
        self.video = cv2.VideoCapture(cam_num)
        
    def __del__(self):
        self.video.release()

    
    def gen_frames(self,stop=None):
        print("self.video",self.video)
        global stop_key,start,dis_img
          
        while True:
            success, frame = self.video.read()  # read the camera frame
            if not success:
                dis_img=1
                
                break
            elif success and stop_key==1:
                print("camera_stoped")
                start=0
                stop_key=0
                # this will empty the frame
                img = cv2.imread('.\img\disconnected.jpg')
                # # frame = img[1].tobytes()
                frame = img.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                break
            else:
                start=1
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        stop_key=0
        self.__del__()
        yield str(dis_img)
       

       
# cap=cv2.VideoCapture("rtsp://admin:Sentry_2020!@166.140.230.62:554/cam/realmonitor?channel=1&subtype=1")
@app.route('/create_record', methods=['POST'])
def create_record():
    parser = reqparse.RequestParser()
    parser.add_argument('cam_path', type=str, required=True,
                        help='cam_path cannot Be Empty')
    try:
        args = parser.parse_args()
    except Exception as e:
        return (jsonify(e),400)
    global cam_path,cv_obj
    print("i'm obj",cv_obj)
    try:

        cv_obj.__del__()
        print("Deleted Bro")
    except:
        pass   
    cam_path = args['cam_path']
    
    # return redirect("/stream", code=200)
    """Video streaming route. Put this in the src attribute of an img tag."""
    return (jsonify(True),
                200)


@app.route('/get_record', methods=['POST'])
def get_record():
    global cam_path
    cam_path = args['cam_path']
    
    """Video streaming route. Put this in the src attribute of an img tag."""
    return (jsonify(cam_path),200)

def snf():
    img = cv2.imread('.\img\disconnected.jpg')
    # frame=cv2.imencode(".jpg",img)[1].tobytes()
    img = cv2.imencode('.jpg', img)
    frame = img[1].tobytes()
    yield (b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
@app.route('/stream_not_found', methods=['GET'])
def stream_not_found():
    return Response(snf(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/', methods=['GET', "OPTIONS"])
# @no_cache
def stream():
    global stop_key,cam_path,cv_obj,dis_img
    global Server_restart
    Server_restart=0
    print("I'm CamPath",cam_path)
    try:
        cv_obj.__del__()
    except:
        pass    
    cv_obj=VideoCamera(cam_path)
    next_data=next(cv_obj.gen_frames())
    if next_data=="1":
        response=redirect("/",code=404)
    else:
        print('stream found')    
        """Video streaming route. Put this in the src attribute of an img tag."""
        # return Response(cv_obj.gen_frames(),
        #                 mimetype='multipart/x-mixed-replace; boundary=frame')
        response=Response(cv_obj.gen_frames(),
                        mimetype='multipart/x-mixed-replace; boundary=frame')    
    return response
def check_stop():
    if start==1:
        if stop_key==0:
            return True
        else:
            import time
            # time.sleep(0.00001)
            time.sleep(0.001)

            check_stop()
    else:
        return True        

@app.route('/close', methods=["GET"])
def end_video_feed():
    global stop_key,start
    print(args.port,"start===",start)
    if start==1:
        stop_key=1
        # if cv_obj:
        #     cv_obj.gen_frames(stop=1)
        
        check_stop()

        """Video streaming route. Put this in the src attribute of an img tag."""
    return "conection close"

@app.route('/shutdown', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })  



if __name__ == '__main__':
    q = Queue()
    p = Process(target=start_flaskapp, args=[
        q,
    ])
    p.start()
    while True:  #wathing queue, if there is no call than sleep, otherwise break
        if q.empty():
            time.sleep(1)
        else:
            break
    p.terminate()  #terminate flaskapp and then restart the app on subprocess
    args = [sys.executable] + [sys.argv[0]]
    subprocess.call(args)
