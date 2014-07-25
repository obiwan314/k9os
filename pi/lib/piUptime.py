# Original code for this script is from here
# https://github.com/JochenB/rpisysinfo
# I just took the uptime part and changed it into piUptime class

class piUptime:

    def __init__(self):
        self.Uptime = self.getUptime()

    def getUptime(self):
        dataFile       = open("/proc/uptime", 'r')
        # In contents[0] we store the Raspberry Pi
        # Uptime in unix time format
        contents       = dataFile.read().split()
        dataFile.close()
        unixTime       = float(contents[0])
        minute         = 60
        hour           = minute * 60
        day            = hour * 24
        days           = int(unixTime / day)
        hours          = int((unixTime % day) / hour)
        minutes        = int((unixTime % hour) / minute)
        seconds        = int(unixTime % minute)

        raspberryUptime = ''
        if days > 0:
            raspberryUptime += str(days) + ' ' + (days == 1 and 'Day' or 'Days') + ' '
        if len (raspberryUptime) > 0 or hours > 0:
            raspberryUptime     += str(hours) + ' ' + (hours == 1 and 'Hour' or 'Hours') + ' '
        if len (raspberryUptime) > 0 or minutes > 0:
            raspberryUptime     += str(minutes) + ' ' + (minutes == 1 and 'Min' or 'Mins') + ' '
        raspberryUptime += str( seconds ) + ' ' + ( seconds == 1 and 'Sec' or 'Sec' )
        return raspberryUptime