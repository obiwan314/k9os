#!/usr/bin/python
from flask import Flask, render_template , request
import datetime
import rpyc
import os
import commands
from datetime import timedelta
import piUptime
import math

runLocally=not os.path.isdir('/home/pi')

if runLocally:
    app = Flask(__name__, template_folder='/Users/wreichardt/projects/k9os/pi/web/templates',static_url_path='/Users/wreichardt/projects/k9os/pi/web/static')
    conn = rpyc.connect('k9mk5',12345)
    sound_directory=os.listdir("/Users/wreichardt/Desktop/Desk/K9/k9 Sounds")
    appPort = 8080
else:
    app = Flask(__name__, template_folder='/home/pi/projects/k9os/pi/web/templates',static_url_path='/home/pi/projects/k9os/pi/web/static')
    conn = rpyc.connect('localhost',12345)
    sound_directory=os.listdir("/home/pi/sounds")
    appPort = 80

@app.route("/")
def hello():
   now = datetime.datetime.now()
   timeString = now.strftime("%Y-%m-%d %H:%M")
   # with open('/proc/uptime', 'r') as f:
   #    uptime_seconds = float(f.readline().split()[0])

   if os.path.isfile("/proc/uptime"):
       Time = piUptime.piUptime()
       uptime_string = Time.Uptime
   else:
       uptime_string="Not Available"

   heading="0"

   templateData = {
      'title' : 'HELLO!',
      'time': timeString,
      'tab':'home',
      'uptime': uptime_string,
      'heading':conn.root.get_last_heading(),
      'range': conn.root.get_last_range()
      }
   return render_template('main.html', **templateData)

@app.route("/sounds")
def sounds():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':sound_directory,
        'tab':'sounds'
    }
    return render_template('sounds.html', **templateData)

@app.route("/controls")
def controls():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':sound_directory,
        'tab':'controls'

    }
    return render_template('controls.html', **templateData)

@app.route("/panel")
def panel():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':sound_directory ,
        'tab':'panel'
    }
    return render_template('panel.html', **templateData)

@app.route("/lcd")
def lcd():
    templateData = {
        'title' : 'HELLO!',
        'tab':'lcd'
    }
    return render_template('lcd.html', **templateData)

@app.route("/wag_horizontal")
def wag_horizontal():
    conn.root.wag_horizontal()
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
        'title' : 'HELLO!',
        'time': timeString,
        'sounds':sound_directory
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
        'sounds':sound_directory
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
        'sounds':sound_directory
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
        'sounds':sound_directory
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
        'sounds':sound_directory
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
        'sounds':sound_directory
    }
    return render_template('main.html', **templateData)

@app.route("/backward")
def backward():
    conn.root.go_backward(30)
    templateData = {
        'title' : 'HELLO!'
    }
    return render_template('ok.html', **templateData)

@app.route("/lcd_write",methods=['POST'])
def lcd_write():
    line1=request.form['line1']
    line2=request.form['line2']
    line3=request.form['line3']
    line4=request.form['line4']
    if line1!='':
        conn.root.lcd_write(1,line1.ljust(20))
    if line2!='':
        conn.root.lcd_write(2,line2.ljust(20))
    if line3!='':
        conn.root.lcd_write(3,line3.ljust(20))
    if line4!='':
        conn.root.lcd_write(4,line4.ljust(20))
    templateData = {
        'title' : 'HELLO!'
    }
    return render_template('ok.html', **templateData)

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
        'sounds':sound_directory
    }
    return render_template('ok.html', **templateData)

@app.route("/animate/<animation>")
def animate(animation=None):
    if(animation=='vertical_sweep_right'):
        conn.root.animation_vertical_sweep_right()
    if(animation=='vertical_sweep_left'):
        conn.root.animation_vertical_sweep_left()
    if(animation=='cancel'):
        conn.root.cancel_animation()
    if(animation=='diagonal_lr_top'):
        conn.root.animation_diagonal_lr_top()
    if(animation=='diagonal_rl_top'):
        conn.root.animation_diagonal_rl_top()
    if(animation=='strobe'):
        conn.root.animation_strobe()
    if(animation=='right_arrow'):
        conn.root.animation_blinking_right_arrow()
    if(animation=='left_arrow'):
        conn.root.animation_blinking_left_arrow()
    if(animation=='random'):
        conn.root.animation_random()

    templateData = {
        'title' : 'HELLO!'
    }
    return render_template('ok.html', **templateData)

@app.route("/restart")
def restart():
    conn.root.restart()

@app.route("/shutdown")
def shutdown():
    conn.root.shutdown()


if __name__ == "__main__":
   app.run(host='0.0.0.0', port=appPort, debug=True)

