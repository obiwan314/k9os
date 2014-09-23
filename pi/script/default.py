#!/usr/bin/python
__author__ = 'wreichardt'
import time
import signal, os
import rpyc

conn = rpyc.connect('k9mk5',12345)
rpyc.BgServingThread(conn)
def event_handler(*args):
    print(args[0])
    event_type=args[0][0]
    event_parameter=args[0][1]

    if(event_type=='key_down'):
        key_number=event_parameter
        if key_number == 1:
            conn.root.animation_blinking_left_arrow()
            conn.root.lcd_write_line14("Blinking Arrow")
        if key_number == 2:
            conn.root.cancel_animation()
            conn.root.lcd_write_line4("              ")
        if key_number == 3:
            conn.root.animation_horizontal_sweep_up()
            conn.root.lcd_write_line4("Horizontal Sweep Up")
        if key_number == 4:
            conn.root.animation_diagonal_rl_bottom()
            conn.root.lcd_write_line4("Diagonal Sweep RL Bottom")
        # if key_number == 6:
        #     conn.root.animation(self.animation_strobe())
        #     conn.root.lcd_write_line4("Strobe")
        # if key_number ==7:
        #     conn.root.animation(self.animation_random())
        #     conn.root.lcd_write_line4("Random")
        # if key_number == 9:
        #     self.set_animation(self.animation_diagonal_lr_top())
        #     self.lcd_write_line4("Diagonal Sweep LR Top")
        if key_number == 11:
            conn.root.restart()
        if key_number == 12:
            #self.set_animation(self.animation_horizontal_sweep_down())
            conn.root.shutdown()


def handler(signum,stuff):
    print 'Signal handler called with signal', signum
    conn.root.release_handler(False);
    rpyc.BgServingThread.stop()
    conn.close()
    running=False


try:

    conn.root.remote_handler(event_handler)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGQUIT, handler)

    while True:
         time.sleep(10)

except Exception:
    pass

print "Stopped"