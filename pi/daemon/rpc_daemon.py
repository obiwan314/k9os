__author__ = 'wreichardt'

import rpyc
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

if __name__ == '__main__':
    s=rpyc.utils.server.ThreadedServer(K9Service, port=12345)
    thread.start_new(s.start, ())
    print "Server Running"
    panel = sample_control_panel.SampleControlPanel()
    panel.idle()
