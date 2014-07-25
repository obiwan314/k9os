#!/usr/bin/python
__author__ = 'wreichardt'
import sys
sys.path.append("/home/pi/projects/k9os/pi/lib")

import rpyc
import thread
import sample_arduino_manager

from rpyc.utils.server import ThreadPoolServer # or ForkingServer ThreadPoolServer

class K9Service(rpyc.Service):
    def on_connect(self):
        "Do some things when a connection is made"
    def on_disconnect(self):
        "Do some things AFTER a connection is dropped"
    def exposed_func1(self, *args, **kws):
        return "Do something useful and maybe return a value"
    def exposed_func2(self, *args, **kws):
        return "Like func1, but do something different"
    def exposed_rotate_left(self, *args, **kws):
        arduino_manager.rotate(arduino_manager.DIRECTION_LEFT)
    def exposed_wag_horizontal(self, *args, **kws):
        arduino_manager.wag(arduino_manager.DIRECTION_HORIZONTAL)
    def exposed_wag_vertical(self, *args, **kws):
        arduino_manager.wag(arduino_manager.DIRECTION_VERTICAL)
    def exposed_rotate_right(self, *args, **kws):
        arduino_manager.rotate(arduino_manager.DIRECTION_RIGHT)
    def exposed_stop(self, *args, **kws):
        arduino_manager.rotate(arduino_manager.DIRECTION_STOP)
    def exposed_go_forward(self, *args, **kws):
        arduino_manager.go_forward(args[0])
    def exposed_go_backward(self, *args, **kws):
        arduino_manager.go_backward(args[0])
    def exposed_clear_lcd(self, *args, **kws):
        arduino_manager.clear_lcd()
    def exposed_lcd_back_light_on(self, *args, **kws):
        arduino_manager.lcd_back_light_on()
    def exposed_lcd_back_light_off(self, *args, **kws):
        arduino_manager.lcd_back_light_off()
    def exposed_test_mode_on(self, *args, **kws):
        arduino_manager.test_mode_on()
    def exposed_test_mode_off(self, *args, **kws):
        arduino_manager.test_mode_off()
    def exposed_lcd_write(self, *args, **kws):
        arduino_manager.lcd_write(args[0],args[1])
    def exposed_lcd_write_bulk(self, *args, **kws):
        arduino_manager.lcd_write_bulk(args[0],args[1],args[2])
    def exposed_lcd_write_line1(self, *args, **kws):
        arduino_manager.lcd_write_line1(args[0])
    def exposed_lcd_write_line2(self, *args, **kws):
        arduino_manager.lcd_write_line2(args[0])
    def exposed_lcd_write_line3(self, *args, **kws):
        arduino_manager.lcd_write_line3(args[0])
    def exposed_lcd_write_line4(self, *args, **kws):
        arduino_manager.lcd_write_line4(args[0])
    def exposed_cancel_animation(self, *args, **kws):
        arduino_manager.cancel_animation()
    def exposed_set_light_code(self, *args, **kws):
        arduino_manager.set_light_code(args[0])
    def exposed_animation_vertical_sweep_right(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_vertical_sweep_right())
    def exposed_animation_vertical_sweep_left(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_vertical_sweep_left())
    def exposed_animation_horizontal_sweep_down(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_horizontal_sweep_down())
    def exposed_animation_diagonal_lr_top(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_diagonal_lr_top())
    def exposed_animation_diagonal_rl_top(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_diagonal_rl_top())
    def exposed_animation_strobe(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_strobe())
    def exposed_animation_blinking_right_arrow(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_blinking_right_arrow())
    def exposed_animation_blinking_left_arrow(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_blinking_left_arrow())
    def exposed_animation_diagonal_lr_bottom(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_diagonal_lr_bottom())
    def exposed_animation_diagonal_rl_bottom(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_diagonal_rl_bottom())
    def exposed_animation_horizontal_sweep_up(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_horizontal_sweep_up())
    def exposed_animation_random(self, *args, **kws):
        arduino_manager.set_animation(arduino_manager.animation_random())
    def exposed_play(self,sound_file_name):
        print sound_file_name
        arduino_manager.play("/home/pi/sounds/"+sound_file_name)
    def exposed_restart(self):
        arduino_manager.restart()
    def exposed_shutdown(self):
        arduino_manager.shutdown()

if __name__ == '__main__':
    s=rpyc.utils.server.ThreadedServer(K9Service, port=12345)
    thread.start_new(s.start, ())
    print "Server Running"

    arduino_manager = sample_arduino_manager.SampleArduinoManager()
    arduino_manager.start_control_panel()

    arduino_manager.lcd_write_line2("       ONLINE         ")
    arduino_manager.lcd_write_line3(" [OFF] [SLEEP] [MENU] ")

    arduino_manager.idle()
