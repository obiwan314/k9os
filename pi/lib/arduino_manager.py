import serial
import io
import json
import time
import thread
import threading
import random

__author__ = 'wreichardt'

def center_message(message):
    isLeft=True
    while(len(message)<20):
        if isLeft:
            message=' '+message
            isLeft=False
        else:
            message=message+' '
            isLeft=True

    return message

class Operation(threading._Timer):
    def __init__(self, *args, **kwargs):
        threading._Timer.__init__(self, *args, **kwargs)
        self.setDaemon(True)

    def run(self):
        while True:
            self.finished.clear()
            self.finished.wait(self.interval)
            if not self.finished.isSet():
                self.function(*self.args, **self.kwargs)
            else:
                return
            self.finished.set()

class Manager(object):

    ops = []

    def add_operation(self, operation, interval, args=[], kwargs={}):
        op = Operation(interval, operation, args, kwargs)
        self.ops.append(op)
        thread.start_new_thread(op.run, ())

    def stop(self):
        for op in self.ops:
            op.cancel()
        self._event.set()

class ArduinoManager():
    BUTTON_1=1
    BUTTON_2=2
    BUTTON_3=4
    BUTTON_4=8
    BUTTON_5=16
    BUTTON_6=32
    BUTTON_7=64
    BUTTON_8=128
    BUTTON_9=256
    BUTTON_10=512
    BUTTON_11=1024
    BUTTON_12=2048
    DIRECTION_LEFT='LEFT'
    DIRECTION_RIGHT='RIGHT'
    DIRECTION_STOP='STOP'
    DIRECTION_HORIZONTAL='HORIZONTAL'
    DIRECTION_VERTICAL='VERTICAL'
    SPEED_STOP=0;
    SPEED_SLOW=20;
    SPEED_FAST=40;
    SPEED_FASTER=60;
    SPEED_FASTEST=70;
    SPEED_RIDICULOUS=80;
    SPEED_LUDICROUS=90;

    current_animation = None
    current_animation_frame = 0
    start_control_panel_called = False

    def __init__(self):
        try:
            self.ser=serial.Serial('/dev/ttyUSB0',115200)
            self.ser1=serial.Serial('/dev/serial/by-path/platform-bcm2708_usb-usb-0:1.3.2:1.0',115200)
        except OSError:
            self.ser=serial.Serial('/dev/tty.usbserial-A9007VIR',115200)
        self.sioMotor = io.TextIOWrapper(io.BufferedRWPair(self.ser, self.ser, 1), encoding='ascii')
        self.sioPanel = io.TextIOWrapper(io.BufferedRWPair(self.ser1, self.ser1, 1), encoding='ascii')
        self.last_light_code=0
        self.confirm_signal = False
        self.timer= Manager()
        self.timer.add_operation(self.tick, .5)
        #self.timer.add_operation(self.start_control_panel, .5)

    def wag(self,direction):
        if direction==self.DIRECTION_HORIZONTAL:
            self.sioPanel.write(unicode('{"waghorizontal":true}'))
        if direction==self.DIRECTION_VERTICAL:
            self.sioPanel.write(unicode('{"wagvertical":true}'))

        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()

    def rotate(self,direction):
        if direction==self.DIRECTION_LEFT:
            self.sioMotor.write(unicode('{"rotate":"'+self.DIRECTION_LEFT+'"}'))
        if direction==self.DIRECTION_RIGHT:
            self.sioMotor.write(unicode('{"rotate":"'+self.DIRECTION_RIGHT+'"}'))
        if direction==self.DIRECTION_STOP:
            self.sioMotor.write(unicode('{"stop":true}'))

        self.sioMotor.write(unicode("\r"))
        self.sioMotor.flush()

    def go_forward(self,speed):
        self.sioMotor.write(unicode('{"goforward":'+str(speed)+'}'))
        self.sioMotor.write(unicode("\r"))
        self.sioMotor.flush()

    def go_backward(self,speed):
        self.sioMotor.write(unicode('{"gobackward":'+str(speed)+'}'))
        self.sioMotor.write(unicode("\r"))
        self.sioMotor.flush()

    def stop(self,speed):
        self.sioMotor.write(unicode('{"stop":true}'))
        self.sioMotor.write(unicode("\r"))
        self.sioMotor.flush()

    def clear_lcd(self):
        self.sioPanel.write(unicode('{"clearlcd":true}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()
        self.wait_for_confirm()

    def lcd_back_light_on(self):
        self.sioPanel.write(unicode('{"backlighton":true}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()

    def lcd_back_light_off(self):
        self.sioPanel.write(unicode('{"backlightoff":true}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()

    def test_mode_on(self):
        self.sioPanel.write(unicode('{"testmodeon":true}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()

    def test_mode_off(self):
        self.sioPanel.write(unicode('{"testmodeoff":true}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()

    def lcd_write(self,line,message):
        if len(message)>20:
            short_message=message[:20]
        else:
            short_message=message
        self.sioPanel.write(unicode('{"line'+str(line)+'":"'+short_message+'"}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()
        self.wait_for_confirm()
        #time.sleep(3)

    def lcd_write_bulk(self,message1,message2,message3):
        if len(message1)>20:
            short_message1=message1[:20]
        else:
            short_message1=message1

        if len(message2)>20:
            short_message2=message2[:20]
        else:
            short_message2=message2

        if len(message3)>20:
            short_message3=message3[:20]
        else:
            short_message3=message3

        self.sioPanel.write(unicode('{'))
        self.sioPanel.write(unicode('"line2":"'+center_message(short_message1)+'",'))
        self.sioPanel.write(unicode('"line3":"'+center_message(short_message2)+'",'))
        self.sioPanel.write(unicode('"line4":"'+center_message(short_message3)+'"'))
        self.sioPanel.write(unicode("}\r"))
        self.sioPanel.flush()

    def lcd_write_line1(self,message):
        self.lcd_write(1,center_message(message));

    def lcd_write_line2(self,message):
        self.lcd_write(2,center_message(message));

    def lcd_write_line3(self,message):
        self.lcd_write(3,center_message(message));

    def lcd_write_line4(self,message):
        self.lcd_write(4,center_message(message));

    def cancel_animation(self):
        self.current_animation=None
        self.current_animation_frame=0
        self.set_light_code(0)

    def start_control_panel(self):
        X=1

    def tick(self):
        # A timer thread enters here to update animations
        # Only do one command at a time in this thread
        # if not self.start_control_panel_called:
        #     self.start_control_panel_called=True
        #     self.start_control_panel()
        #     return

        if self.current_animation is None:
            return
        self.set_light_code(self.current_animation[self.current_animation_frame])
        self.current_animation_frame=self.current_animation_frame+1
        if(self.current_animation_frame>=len(self.current_animation)):
            self.current_animation_frame=0

    def set_light_code(self,code):
        self.sioPanel.write(unicode('{"lightcode":'+str(code)+'}'))
        self.sioPanel.write(unicode("\r"))
        self.sioPanel.flush()
        self.last_light_code=code

    def animation_vertical_sweep_right(self):
        return [
            self.BUTTON_9+self.BUTTON_5+self.BUTTON_1,
            self.BUTTON_10+self.BUTTON_6+self.BUTTON_2,
            self.BUTTON_11+self.BUTTON_7+self.BUTTON_3,
            self.BUTTON_12+self.BUTTON_8+self.BUTTON_4
        ]

    def animation_vertical_sweep_left(self):
        return [
            self.BUTTON_12+self.BUTTON_8+self.BUTTON_4,
            self.BUTTON_11+self.BUTTON_7+self.BUTTON_3,
            self.BUTTON_10+self.BUTTON_6+self.BUTTON_2,
            self.BUTTON_9+self.BUTTON_5+self.BUTTON_1
        ]

    def animation_horizontal_sweep_down(self):
        return [
            self.BUTTON_9+self.BUTTON_10+self.BUTTON_11+self.BUTTON_12,
            self.BUTTON_5+self.BUTTON_6+self.BUTTON_7+self.BUTTON_8,
            self.BUTTON_1+self.BUTTON_2+self.BUTTON_3+self.BUTTON_4
        ]

    def animation_diagonal_lr_top(self):
        return [
            self.BUTTON_9,
            self.BUTTON_10+self.BUTTON_5,
            self.BUTTON_1+self.BUTTON_6+self.BUTTON_11,
            self.BUTTON_2+self.BUTTON_7+self.BUTTON_12,
            self.BUTTON_3+self.BUTTON_8,
            self.BUTTON_4
        ]

    def animation_diagonal_rl_top(self):
        return [
            self.BUTTON_12,
            self.BUTTON_11+self.BUTTON_8,
            self.BUTTON_10+self.BUTTON_7+self.BUTTON_4,
            self.BUTTON_9+self.BUTTON_6+self.BUTTON_3,
            self.BUTTON_5+self.BUTTON_2,
            self.BUTTON_1
        ]

    def animation_strobe(self):
        return[0,self.BUTTON_1,self.BUTTON_2,self.BUTTON_3,
               self.BUTTON_4,self.BUTTON_5,self.BUTTON_6,
               self.BUTTON_7,self.BUTTON_8,self.BUTTON_9,
               self.BUTTON_10,self.BUTTON_11,self.BUTTON_12
               ]

    def animation_blinking_right_arrow(self):
        return[0,self.BUTTON_5+self.BUTTON_6+self.BUTTON_7+self.BUTTON_8+self.BUTTON_11+self.BUTTON_3]

    def animation_blinking_left_arrow(self):
        return[0,self.BUTTON_5+self.BUTTON_6+self.BUTTON_7+self.BUTTON_8+self.BUTTON_10+self.BUTTON_2]

    def animation_diagonal_lr_bottom(self):
        return self.animation_diagonal_rl_top()[::-1]

    def animation_diagonal_rl_bottom(self):
        return self.animation_diagonal_lr_top()[::-1]

    def animation_horizontal_sweep_up(self):
        return self.animation_horizontal_sweep_down()[::-1]

    def animation_random(self):
        rand_animation=[]
        chosen_lights=[]
        for x in range(10):
            number_of_lights= random.randrange(1,12+1)
            for y in range(number_of_lights):
                chosen_light=random.randrange(0,4095)
                rand_animation.append(chosen_light)
        return rand_animation

    def set_animation(self,current_animation):
        self.cancel_animation()
        self.current_animation=current_animation

    def wait_for_confirm(self):
        X=1
        # print('Waiting for confirmation')
        # while(not self.confirm_signal):
        #     time.sleep(1)
        # self.confirm_signal = False
        # print('Confirmed')


    def confirm(self):
        self.confirm_signal = True

    def read_serial_panel(self):
        while True:
            received_message=self.sioPanel.readline()[:-1]
            print received_message+"\n"
            try:
                object=json.loads(received_message)
            except ValueError:
                object={}

            self.dispatch_message(object)

    def read_serial_motor(self):
        while True:
            received_message=self.sioMotor.readline()[:-1]
            print received_message+"\n"
            try:
                object=json.loads(received_message)
            except ValueError:
                object={}

            self.dispatch_message(object)

    def idle(self):
        # The main thread lives here and empties the
        # serial buffer of data from the Arduino
        #    time.sleep(.1)
        thread = threading.Thread(target=self.read_serial_panel)#, args=(serial_port,)
        thread.start()
        self.read_serial_motor()

    def dispatch_message(self,object):

        if 'response' in object:
            self.confirm()

        if 'key1' in object:
            if object.get('key1') == 'down':
                self.on_key_down(1)
            else:
                self.on_key_up(1)

        if 'key2' in object:
            if object.get('key2') == 'down':
                self.on_key_down(2)
            else:
                self.on_key_up(2)

        if 'key3' in object:
            if object.get('key3') == 'down':
                self.on_key_down(3)
            else:
                self.on_key_up(3)

        if 'key4' in object:
            if object.get('key4') == 'down':
                self.on_key_down(4)
            else:
                self.on_key_up(4)

        if 'key5' in object:
            if object.get('key5') == 'down':
                self.on_key_down(5)
            else:
                self.on_key_up(5)

        if 'key6' in object:
            if object.get('key6') == 'down':
                self.on_key_down(6)
            else:
                self.on_key_up(6)

        if 'key7' in object:
            if object.get('key7') == 'down':
                self.on_key_down(7)
            else:
                self.on_key_up(7)

        if 'key8' in object:
            if object.get('key8') == 'down':
                self.on_key_down(8)
            else:
                self.on_key_up(8)

        if 'key9' in object:
            if object.get('key9') == 'down':
                self.on_key_down(9)
            else:
                self.on_key_up(9)

        if 'key10' in object:
            if object.get('key10') == 'down':
                self.on_key_down(10)
            else:
                self.on_key_up(10)

        if 'key11' in object:
            if object.get('key11') == 'down':
                self.on_key_down(11)
            else:
                self.on_key_up(11)

        if 'key12' in object:
            if object.get('key12') == 'down':
                self.on_key_down(12)
            else:
                self.on_key_up(12)

        if 'onHeadingChange' in object:
            self.onHeadingChange(object.get('onHeadingChange'))

        if 'onRangeChange' in object:
            self.onRangeChange(object.get('onRangeChange'))

        if 'safetystop' in object:
            self.onSafetyStop()

    def on_key_down(self,key_number):
        raise NotImplementedError("must be implemented in subclass")

    def on_key_up(self,key_number):
        raise NotImplementedError("must be implemented in subclass")

    def onHeadingChange(self,heading):
        print "HEADING CHANGED "+heading
        raise NotImplementedError("must be implemented in subclass")

    def onRangeChange(self,range):
        raise NotImplementedError("must be implemented in subclass")

    def onSafetyStop(self):
       raise NotImplementedError("must be implemented in subclass")
