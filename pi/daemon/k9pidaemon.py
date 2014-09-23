# !/usr/bin/python
# /etc/init.d/k9pidaemon

### BEGIN INIT INFO
# Provides:          k9pidaemon
# Required-Start:    $syslog
# Required-Stop:     $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Starts up serial communication to the k9 robot
# Description:       Reponsible for auto starting the k9 robot. A script which will start / stop a program a boot / shutdown.
### END INIT INFO

sys.path.append('/pi/projects/k9os/pi/daemon/lib')

from daemon import Daemon
import sys
import time
import logging
import subprocess

__author__ = 'wreichardt'

PIDFILE = '/var/run/rphaldaemon.pid'
LOGFILE = '/var/log/rphaldaemon.log'

# Configure logging
logging.basicConfig(filename=LOGFILE, level=logging.DEBUG)


class K9Daemon(Daemon):
    def run(self):
        # Define your tasks here
        # Anything written in python is permitted
        # For example you can clean up your server logs every hour


        # Logging errors and exceptions
        try:
            pass
        except Exception, e:
            logging.exception(
                'Human friendly error message, the exception will be captured and added to the log file automaticaly')

        while True:
            # The daemon will repeat your tasks according to this variable
            # it's in second so 60 is 1 minute, 3600 is 1 hour, etc.
            time.sleep(60)


if __name__ == "__main__":

    daemon = K9Daemon(PIDFILE)

    if len(sys.argv) == 2:

        if 'start' == sys.argv[1]:
            try:
                print "Starting Instance..."
                daemon.start()
            except:
                pass

        elif 'stop' == sys.argv[1]:
            print "Stopping ..."
            subprocess.call(['aplay', '/home/pi/sounds/goodbye.wav'])
            daemon.stop()

        elif 'restart' == sys.argv[1]:
            print "Restaring ..."
            daemon.restart()

        elif 'status' == sys.argv[1]:
            try:
                pf = file(PIDFILE, 'r')
                pid = int(pf.read().strip())
                pf.close()
            except IOError:
                pid = None
            except SystemExit:
                pid = None

            if pid:
                print 'K9Daemon is running as pid %s' % pid
            else:
                print 'K9Daemon is not running.'

        else:
            print "Unknown command"
            sys.exit(2)
            sys.exit(0)
    else:
        print "usage: %s start|stop|restart|status" % sys.argv[0]
        sys.exit(2)
