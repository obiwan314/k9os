# !/usr/bin/python
import arduino_manager
import pygame

__author__ = 'wreichardt'


class SampleArduinoManager(arduino_manager.ArduinoManager):
    pass

    def start_control_panel(self):
        self.lcd_write_bulk("Keyboard Test", "                    ", "Try buttons...")
        arduino_manager.ArduinoManager.start_control_panel(self)
        pygame.init()
        pygame.mixer.init()

    def on_key_down(self, key_number):
        if key_number == 1:
            self.set_animation(self.animation_blinking_left_arrow())
            self.lcd_write_line4("Blinking Arrow")
        if key_number == 2:
            self.cancel_animation()
            self.lcd_write_line4("              ")
        if key_number == 3:
            self.set_animation(self.animation_horizontal_sweep_up())
            self.lcd_write_line4("Horizontal Sweep Up")
        if key_number == 4:
            self.set_animation(self.animation_diagonal_rl_bottom())
            self.lcd_write_line4("Diagonal Sweep RL Bottom")
        if key_number == 9:
            self.set_animation(self.animation_diagonal_lr_top())
            self.lcd_write_line4("Diagonal Sweep LR Top")
        if key_number == 11:
            self.set_animation(self.animation_horizontal_sweep_down())
            self.lcd_write_line4("Horizontal Sweep Down")
        if key_number == 6:
            self.set_animation(self.animation_strobe())
            self.lcd_write_line4("Strobe")
        if key_number == 7:
            self.set_animation(self.animation_random())
            self.lcd_write_line4("Random")

    def play(self, file):
        pygame.mixer.music.load(file)
        pygame.mixer.music.play()

    def on_key_up(self, key_number):
        x = 1

    def onHeadingChange(self, key_number):
        x = 1

    def onRangeChange(self, key_number):
        x = 1

    def onSafetyStop(self):
        print("SAFETY STOP")
        self.play("/home/pi/sounds/malfunction_in_drive_systems.mp3")


if __name__ == '__main__':
    panel = SampleArduinoManager()
    panel.idle()
