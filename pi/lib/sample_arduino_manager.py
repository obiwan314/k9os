# !/usr/bin/python
import arduino_manager
import pygame
import time
import subprocess
import rpyc

__author__ = 'wreichardt'

class SampleArduinoManager(arduino_manager.ArduinoManager):

    def __init__(self):
        arduino_manager.ArduinoManager.__init__(self)
        self.remote_callback=False

    def start_control_panel(self):
        arduino_manager.ArduinoManager.start_control_panel(self)
        pygame.init()
        pygame.mixer.init()
        self.play("/home/pi/sounds/system_restarting.mp3")
        self.last_heading = 0
        self.last_range = 0

    def shutdown(self):
        self.lcd_write_line4("Shutting Down...")
        self.play("/home/pi/sounds/closing_down.mp3")
        subprocess.call(['/sbin/shutdown', '-h', 'now'])

    def restart(self):
        self.lcd_write_line4("Restarting...")
        self.play("/home/pi/sounds/restarting.mp3")
        subprocess.call(['/sbin/shutdown', '-r', 'now'])

    def play(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def get_last_heading(self):
        return self.last_heading

    def get_last_range(self):
        return self.last_range

    def set_remote_callback(self,remote_function):
        self.remote_callback=remote_function

    def perform_callback(self,*args):
        if self.remote_callback:
            async=rpyc.async(self.remote_callback)
            async(args)

    # Event Handlers
    def on_key_down(self, key_number):
        self.perform_callback("key_down",key_number)


    def on_key_up(self, key_number):
        self.perform_callback("key_up",key_number)

    def onHeadingChange(self, heading):
        self.last_heading = heading
        self.perform_callback("heading_change",heading)

    def onRangeChange(self, range):
        self.last_range=range
        self.perform_callback("range_change",range)

    def onSafetyStop(self):
        self.play("/home/pi/sounds/malfunction_in_drive_systems.mp3")
        self.perform_callback("safety_stop")

if __name__ == '__main__':
    panel = SampleArduinoManager()
    panel.idle()
