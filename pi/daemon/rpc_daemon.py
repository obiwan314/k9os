#!/usr/bin/python
__author__ = 'wreichardt'

import rpyc
import pygame
import thread
import sample_control_panel
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
        panel.rotate(panel.DIRECTION_LEFT)
    def exposed_rotate_right(self, *args, **kws):
        panel.rotate(panel.DIRECTION_RIGHT)
    def exposed_stop(self, *args, **kws):
        panel.rotate(panel.DIRECTION_STOP)
    def exposed_go_forward(self, *args, **kws):
        panel.go_forward(args[0])
    def exposed_go_backward(self, *args, **kws):
        panel.go_backward(args[0])
    def exposed_clear_lcd(self, *args, **kws):
        panel.clear_lcd()
    def exposed_lcd_back_light_on(self, *args, **kws):
        panel.lcd_back_light_on()
    def exposed_lcd_back_light_off(self, *args, **kws):
        panel.lcd_back_light_off()
    def exposed_test_mode_on(self, *args, **kws):
        panel.test_mode_on()
    def exposed_test_mode_off(self, *args, **kws):
        panel.test_mode_off()
    def exposed_lcd_write(self, *args, **kws):
        panel.lcd_write(args[0],args[1])
    def exposed_lcd_write_bulk(self, *args, **kws):
        panel.lcd_write_bulk(args[0],args[1],args[2])
    def exposed_lcd_write_line1(self, *args, **kws):
        panel.lcd_write_line1(args[0])
    def exposed_lcd_write_line2(self, *args, **kws):
        panel.lcd_write_line2(args[0])
    def exposed_lcd_write_line3(self, *args, **kws):
        panel.lcd_write_line3(args[0])
    def exposed_lcd_write_line4(self, *args, **kws):
        panel.lcd_write_line4(args[0])
    def exposed_cancel_animation(self, *args, **kws):
        panel.cancel_animation()
    def exposed_set_light_code(self, *args, **kws):
        panel.set_light_code(args[0])
    def exposed_animation_vertical_sweep_right(self, *args, **kws):
        panel.animation_vertical_sweep_right()
    def exposed_animation_vertical_sweep_left(self, *args, **kws):
        panel.animation_vertical_sweep_left()
    def exposed_animation_horizontal_sweep_down(self, *args, **kws):
        panel.animation_horizontal_sweep_down()
    def exposed_animation_diagonal_lr_top(self, *args, **kws):
        panel.animation_diagonal_lr_top()
    def exposed_animation_diagonal_rl_top(self, *args, **kws):
        panel.animation_diagonal_rl_top()
    def exposed_animation_strobe(self, *args, **kws):
        panel.animation_strobe()
    def exposed_animation_blinking_right_arrow(self, *args, **kws):
        panel.animation_blinking_right_arrow()
    def exposed_animation_blinking_left_arrow(self, *args, **kws):
        panel.animation_blinking_left_arrow()
    def exposed_animation_diagonal_lr_bottom(self, *args, **kws):
        panel.animation_diagonal_lr_bottom()
    def exposed_animation_diagonal_rl_bottom(self, *args, **kws):
        panel.animation_diagonal_rl_bottom()
    def exposed_animation_horizontal_sweep_up(self, *args, **kws):
        panel.animation_horizontal_sweep_up()
    def exposed_animation_random(self, *args, **kws):
        panel.animation_random()
    def exposed_play(self,sound_file_name):
        print sound_file_name
        panel.play("/home/pi/sounds/"+sound_file_name)
        #pygame.mixer.music.load("/home/pi/sounds/"+sound_file_name)
        #pygame.mixer.music.play()

if __name__ == '__main__':
    s=rpyc.utils.server.ThreadedServer(K9Service, port=12345)
    thread.start_new(s.start, ())
    #pygame.init()
    #pygame.mixer.init()
    print "Server Running"
    panel = sample_control_panel.SampleArduinoManager()
    panel.start_control_panel()
    panel.idle()
