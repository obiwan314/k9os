#!/usr/bin/python
from flask import Flask, render_template
import datetime
import rpyc
import os

app = Flask(__name__, template_folder='/home/pi/projects/k9os/pi/web/templates')
conn = rpyc.connect('localhost',12345)

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   templateData = {
      'title' : 'HELLO!',
      'time': timeString,
      'sounds':os.listdir("/home/pi/sounds")
      }
   return render_template('main.html', **templateData)

@app.route("/wag_horizontal")
def wag_horizontal():
    conn.root.wag_horizontal()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/wag_vertical")
def wag_vertical():
    conn.root.wag_vertical()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/rotate_left")
def rotate_left():
    conn.root.rotate_left()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/rotate_right")
def rotate_right():
    conn.root.exposed_rotate_right()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/stop")
def stop():
    conn.root.stop()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/forward")
def forward():
    conn.root.go_forward(30)
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/backward")
def backward():
    conn.root.go_backward(30)
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)

@app.route("/play/<soundname>")
def play(soundname=None):
    if(soundname==None):
         conn.root.play("insufficent_data.mp3")
    else:
         conn.root.play(soundname)
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':os.listdir("/home/pi/sounds")
    }
    return render_template('main.html', **templateData)


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=80, debug=True)

