    ### BEGIN INIT INFO
    # Provides:          piTemp
    # Required-Start:    autofs $all
    # Required-Stop:     $remote_fs
    # Default-Start:     2 3 4 5
    # Default-Stop:      0 1 6
    # Short-Description: Starts and stops the Raspberry Radio
    # Description:       Starts and stops the Raspberry Radio
    ### END INIT INFO

    PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
    DAEMON=/home/pi/projects/k9/pi/panel/sample_control_panel.py
    NAME=pik9comm
    DESC="K9 Serial Communications Daemon"

    test -x $DAEMON || exit 0

    . /lib/lsb/init-functions

    set -e

    case "$1" in
      start)
        echo -n "Starting $DESC: "
        start-stop-daemon --start --quiet --pidfile /var/run/$NAME.pid --background --make-pidfile --exec $DAEMON
        echo "$NAME."
        ;;
      stop)
        echo -n "Stopping $DESC: "
        start-stop-daemon --stop --oknodo --quiet --pidfile /var/run/$NAME.pid
        echo "$NAME."
        ;;
      restart)
        $0 stop
        sleep 1
        $0 start
        ;;
      *)
        echo "Usage: $0 {start|stop|restart}" >&2
        exit 1
        ;;
    esac
    exit 0
