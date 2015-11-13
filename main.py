#!/usr/bin/env python


###############################################################################
#  
#   Project : Video Streaming with Flask 
#   Author  : Peter Guan, Xu Guo
#   Date    : 11/11/2015  
#   
#   Description:
#   Modified to support streaming out with webcams, and not just raw JPEGs.
#   Most of the code credits to Miguel Grinberg.
#   Credits : http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#             http://www.chioka.in/
#   
#
###############################################################################
from __future__ import print_function
from flask import Flask, render_template, Response, send_from_directory
from camera import VideoCamera
import smbus
import datetime
import time

# for RPI version 1, use "bus = smbus.SMBus(0)"
xbus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04
flag = 0

serverCmd = {'forward':1,
			'backward':2,
			'turnleft':3,
			'turnright':4,
			'stop':5
}

def writeNumber( value):
    global flag
    try:
        xbus.write_byte(address, value)
    except IOError:
        subprocess.call('i2cdetect','-y','1')
        flag = 1
    return -1
	
	
def readNumber( ):
    try:
        num = xbus.read_byte(address )
    except IOError:
        subprocess.call('i2cdetect','-y','1')
        flag = 1
        return -1
    return num


app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)

@app.route('/index2')
def index2():
    return render_template('index2.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/forward')
def forward_world():
    # do some operation for the cart
	#writeNumber(serverCmd['forward'])
	writeNumber(serverCmd.forward)
	response=readNumber():
	if response is not None:
		return true
	else
		return false
		
		
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='10.1.15.97', debug=True)