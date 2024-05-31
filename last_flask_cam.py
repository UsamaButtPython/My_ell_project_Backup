from time import time
from urllib import response
from flask import abort
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
from multiprocessing import Process, Queue,Manager
from werkzeug.serving import run_simple
some_queue = None
video_queue=None
app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

print("I'm runing")
parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('-p','--port',dest='port',type=str,help='Port',
                        required=True)
args = parser.parse_args()
cv_obj=None
cam_path=None
# stop_key=0
# start=0
# dis_img=0
p1_status_glob=None
video_queue=None
main_loop=None
found_cam=False
p=None
force_stop=0
stoped=0

@app.route('/restart')
def restart():
    try:
        
        some_queue.put("something")
        print("Restarted successfully")
        return "Quit"
    except:
        print("Failed in restart")
        return "Failed"

class VideoCamera(object):
    def __init__(self,cam_num):
        global p1_status_glob,video_queue
        # cv2.VideoCapture('rtsp://username:password@192.168.1.64/1')
        try:
            self.video = cv2.VideoCapture(cam_num)
            print("i'm test",self.video.isOpened())
            if not self.video.isOpened():
                self.video =None 
                print('Error') 
                p1_status_glob.put(False)
                video_queue.put('None')
        except:
            self.video =None  
        
    def __del__(self):
        try:
            self.video.release()
        except:
            pass

    
    def gen_frames(self,q,stop=None):
        print("self.video",self.video)
        while True:
            # print("i'm video module")
            success, frame = self.video.read()  # read the camera frame
            p1_status_glob.put(success)
            if force_stop==1:
                abort(404)
            if not success:
                break
            else:
                start=1
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                q.put(frame)
        self.video.__del__()
       

       
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



@app.route('/shutdown', methods=['GET'])
def stopServer():
    os.kill(os.getpid(), signal.SIGINT)
    return jsonify({ "success": True, "message": "Server is shutting down..." })  

def playstream(q,p1_status,cam_path):
    global video_queue,p1_status_glob,video_queue
    
    p1_status_glob=p1_status
    video_queue=q
    # ncv_obj=VideoCamera('rtsp://admin:Sentry_2022!321@165.140.230.62:554/cam/realmonitor?channel=1&subtype=1')
    print(cam_path)
    ncv_obj=VideoCamera(cam_path)
    
    print('camera play',ncv_obj.video)
    if ncv_obj.video is not None:
        ncv_obj.gen_frames(video_queue)
    # p.terminate()     
    return ncv_obj.video 
# def get_frames():

# class testMain(object):        
#     def StreamMultiprocessing(self):
#         global p,cam_path
#         print('cam_path',cam_path)
#         # if you hit / from another browser it will not create process
#         if p is None:
#             q = Queue()
#             p1_status=Queue()
#             # manager = Manager()
#             # q = manager.Queue()
#             # p1_status = manager.Queue()

#             p = Process(target=playstream, args=[
#                 q,p1_status,cam_path
#             ])
#             p.start()
#             global main_loop,found_cam
#             main_loop=1
#             while main_loop:  #wathing queue, if there is no call than sleep, otherwise break
                
#                 if q.empty():
#                     print("q.empty")
#                     time.sleep(1)
#                 else:
#                     while True: 
#                         found_cam=p1_status.get()
#                         # print("q.empty",found_cam)
#                         if found_cam:  
#                             yield (b'--frame\r\n'
#                         b'Content-Type: image/jpeg\r\n\r\n' + q.get() + b'\r\n')
#                         if found_cam==False:
#                             print('Cam Not found')
#                             p.terminate()
#                             yield '0'
#                             main_loop=0
#                             break
#                         # break
#             # abort(404)
#             p.terminate()  #terminate flaskapp and then restart the app on subprocess
#             # print("bye bye") 

           
def StreamMultiprocessing():
    global p,cam_path
    print('cam_path',cam_path)
    # if you hit / from another browser it will not create process
    if p is None:
        q = Queue()
        p1_status=Queue()
        # manager = Manager()
        # q = manager.Queue()
        # p1_status = manager.Queue()

        p = Process(target=playstream, args=[
            q,p1_status,cam_path
        ])
        p.start()
        global main_loop,found_cam
        main_loop=1
        while main_loop:  #wathing queue, if there is no call than sleep, otherwise break
            
            if q.empty():
                print("q.empty")
                time.sleep(1)
            else:
                while True: 
                    found_cam=p1_status.get()
                    # print("q.empty",found_cam)
                    if found_cam:  
                        yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + q.get() + b'\r\n')
                    if found_cam==False:
                        print('Cam Not found')
                        p.terminate()
                        yield '0'
                        main_loop=0
                        break
                    if force_stop==1:
                        abort(404)
                    # break
        # abort(404)
        p.terminate()  #terminate flaskapp and then restart the app on subprocess
        # print("bye bye")    
@app.route('/kill', methods=['POST'])
def kill():
    global p,main_loop,force_stop
    if p:
        print("request to about")
        main_loop=0
        p.terminate()
        p=None
        force_stop=1
        check_stop()
        return "request about"
    return "False"    

def check_stop():
    global force_stop
    if force_stop==0:
        check_stop()
    else:
        pass    

@app.route('/', methods=['GET'])
def stream():
    global p,main_loop,force_stop
    force_stop=0
    print("got get request")
    # if p:
    #     main_loop=0
    #     print("request to about")
    #     p.terminate()
    #     print("request about")
    p=None
    stream=None
    # obj=testMain()
    stream=StreamMultiprocessing()
    try:
        next_data=next(stream)
        # print(next_data)
        if next_data=="0":
            print("if purpose")

            # return redirect("/hehehe",code=404)
            p.terminate()
            abort(404)

        return Response(stream,mimetype='multipart/x-mixed-replace; boundary=frame')  
    except:
        print("except purpose")
        # return redirect("/hehehe",code=404)  
        p.terminate()
        abort(404)
            

if __name__ == '__main__':
    # global some_queue
    # some_queue = queue
    app.run(host='0.0.0.0',port=args.port,debug=True,threaded=True)
    # run_simple('localhost', int(args.port), app)
    # q = Queue()
    # p1 = Process(target=start_flaskapp, args=[
    #     q,
    # ])
    # p1.start()

    # while True:  #wathing queue, if there is no call than sleep, otherwise break
    #     if q.empty():
    #         time.sleep(1)
    #     else:
    #         break
    # p1.terminate()  #terminate flaskapp and then restart the app on subprocess
    # args = [sys.executable] + [sys.argv[0]]
    # subprocess.call(args)
