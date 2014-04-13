__author__ = 'wreichardt'

import rpyc
import sample_control_panel
from rpyc.utils.server import ThreadedServer # or ForkingServer

class K9Service(rpyc.Service):

server = ThreadedServer(K9Service, port=12345)
server.start()

