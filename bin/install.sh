# OSX ARD_SKETCH=/Users/wreichardt/Documents/Arduino
# OSX $ARD_LIB=/Users/wreichardt/Documents/Arduino/libraries
# PI ARD_SKETCH=/home/pi/sketchbook/
# PI $ARD_LIB=/usr/share/arduino/libraries
export ARD_SKETCH=/home/pi/sketchbook/
export ARD_LIB=/home/pi/sketchbook/libraries
mkdir $ARD_LIB
cd ..
ln -s `pwd`/arduino/panel/libraries/LiquidCrystal $ARD_LIB/LiquidCrystal
ln -s `pwd`/arduino/panel/libraries/aJson $ARD_LIB/aJason
ln -s `pwd`/arduino/panel/src/k9os $ARD_SKETCH
ln -s `pwd`/arduino/motion/src/drive $ARD_SKETCH

# Install daemon (Must be run as root)
sudo cp `pwd`/pi/daemon/k9pidaemon /etc/init.d
sudo update-rc.d k9pidaemon defaults