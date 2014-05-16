/*
 * K9OS drive motor sketch
 * Controls Scooter Motors,
 * Compass, RC Receiver and
 * Ultrasonic Rangefinder
 */

#include <Wire.h> //I2C Arduino Library
#include <math.h>
#include <aJSON.h>

const float pi=3.14159;

// Megamoto Resources
int EnablePin = 8;
int PWMPin = 11;  // Timer2
int PWMPin2 = 3;
int PWMPinA = 9;  // Timer2
int PWMPinA2 = 10;
const int DIRECTION_FORWARD=1;
const int DIRECTION_BACKWARD=-1;
const int DIRECTION_STOP=0;
const int SPEED_STOP=0;
const int SPEED_SLOW=20;
const int SPEED_FAST=40;
const int SPEED_FASTER=60;
const int SPEED_FASTEST=70;
const int SPEED_RIDICULOUS=70;
const int SPEED_LUDICROUS=80;
const int NO_ROTATION=0;
const int LEFT_ROTATION=1;
const int RIGHT_ROTATION=-1;
const int SAFE_DISTANCE=15;
// Compass Constants
const int compassI2CAddress=0x1E;

// Remote Control
const int ultrasonicRangeFinderPin= 4;

// Globals
float lastHeading=-2;
float lastRange=-1;
float persistantBias=0;
int persistantDirection=0;
int persistantSpeed=0;
int persistantRotation=0;
int safetyStop=0;

void setup() {
  // Megamoto
  // initialize the digital pin as an output.
  // Pin 13 has an LED connected on most Arduino boards:
  pinMode(EnablePin, OUTPUT);
  pinMode(PWMPin, OUTPUT);
  pinMode(PWMPin2, OUTPUT);
  pinMode(PWMPinA, OUTPUT);
  pinMode(PWMPinA2, OUTPUT);
  setPwmFrequency(PWMPin, 8);  // change Timer2 divisor to 8 gives 3.9kHz PWM freq
  setPwmFrequency(PWMPinA, 8);  // change Timer2 divisor to 8 gives 3.9kHz PWM freq

  // Remote Control
  pinMode(5, INPUT); // Set our input pins as such
  pinMode(6, INPUT);
  pinMode(7, INPUT);
  pinMode(2, INPUT);

  // Set up compass
  Wire.begin();

  // Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(compassI2CAddress); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();

  Serial.begin(115200); // Establish connection with raspberri pi 115200

}

void loop() {

  processReceivedMessages();
  int currentRange=echoRangeFinder();
  if(abs(lastRange-currentRange)>1){
    Serial.print("{\"onRangeChange\":");
    Serial.print(currentRange);
    Serial.println("}");
    lastRange=currentRange;
  }

  float heading=readHeading();
  if(abs(lastHeading-heading)>=2){
    Serial.print("{\"onHeadingChange\":");
    Serial.print(heading);
    Serial.println("}");
    lastHeading=heading;
  }
  
  processRcTransmitter(currentRange);

}

/**
 * Map RC receiver values to motor control 
 *  actions.
 */
void processRcTransmitter(int currentRange){
  // poll current RC receiver values
  int ch1 = pulseIn(5, HIGH, 25000); // B Switch, Disables everything
  int ch2 = pulseIn(6, HIGH, 25000); // B Stick vertical
  int ch3 = pulseIn(7, HIGH, 25000); // B Stick horizontal
  int ch4 = pulseIn(2, HIGH, 25000); // A Stick horizontal
  float bias=0;

  // Special case, in place rotation
  if(ch2>=1450&&ch2<1500){    
    // throttle at zero
    if(ch4<=1450){ // Spin Left
       controlMotor(SPEED_FASTER,DIRECTION_FORWARD,0.5,LEFT_ROTATION);
       return;
    } else if(ch4>=1500){ // Spin Right
       controlMotor(SPEED_FASTER,DIRECTION_FORWARD,-0.5,RIGHT_ROTATION);
       return;
    }     
  }
  
  // Calculate current bias
  if(ch4<1500&&ch4>1490)
    bias=0;
  if(ch4<=1490)
    bias=-((ch4-1490)/190.0)*0.8;
  if(ch4>=1500)
    bias=((ch3-1500)/200.0)*0.8;

  
  if(ch1<996){ // This sets SWB as the master motor cut off
      // Master cutoff switch is on or remote is off, autonomous behavior permitted
      if(persistantSpeed>0) {
          // We are moving autonomously
          if(currentRange<SAFE_DISTANCE&&persistantDirection==DIRECTION_FORWARD){
              // Shut down forward motion in from of an obsticle
              controlMotor(0,0,bias,NO_ROTATION);
              if(safetyStop==0){
                 Serial.println("{\"safetystop\":true}");
                 safetyStop=1;
              } 
              return;
          } else {
              // Execute raspberry pi commands if no remote is available and no obsticles present
              controlMotor(persistantSpeed,persistantDirection,persistantBias,persistantRotation);
              return;
          }
      }
   } else {
       // We are in remote control mode
       
       // Reverse
       if(ch2<1400){
          controlMotor(SPEED_FASTER,DIRECTION_BACKWARD,0,NO_ROTATION);
          return;
       }
       if(ch2>=1400&&ch2<1425){
          controlMotor(SPEED_FAST,DIRECTION_BACKWARD,0,NO_ROTATION);
          return;
        }
        if(ch2>=1425&&ch2<1450){
          controlMotor(SPEED_SLOW,DIRECTION_BACKWARD,0,NO_ROTATION);
          return;
        }
        
        // Stop
        if(ch2>=1450&&ch2<1500){
          controlMotor(SPEED_STOP,DIRECTION_STOP,0,NO_ROTATION);
          return;
        }
        
        // Forward
        if(currentRange>SAFE_DISTANCE){
            safetyStop=0;
            if(ch2>=1500&&ch2<1525){
                controlMotor(SPEED_SLOW,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
            }
            if(ch2>=1525&&ch2<1550){
                controlMotor(SPEED_FAST,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
             }
             if(ch2>=1550&&ch2<1575){
                controlMotor(SPEED_FASTER,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
             }
             if(ch2>=1575&&ch2<1600){
                controlMotor(SPEED_FASTEST,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
             }
             if(ch2>=1600&&ch2<1625){
                controlMotor(SPEED_RIDICULOUS,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
             }
             if(ch2>=1625){
                controlMotor(SPEED_LUDICROUS,DIRECTION_FORWARD,0,NO_ROTATION);
                return;
             }
        } else {
              if(safetyStop==0){
                 Serial.println("{\"safetystop\":true}");
                 safetyStop=1;
              } 
             controlMotor(SPEED_STOP,DIRECTION_STOP,0,NO_ROTATION);
        }
  } // end remote control Mode

}

static inline int8_t sgn(int val) {
  if (val < 0) return -1;
  if (val==0) return 0;
  return 1;
}

void controlMotor(int speed,int direction,float bias,int rotate){
  int biasSpeedL=0.0;
  int biasSpeedR=0.0;
  if(bias==0){
    biasSpeedR=speed;
    biasSpeedL=speed;
  } else {
    if(bias*sgn(-direction)>0){
      biasSpeedL=abs(round(speed*bias));
      biasSpeedR=abs(round(speed*(1.0-bias)));
    } else {
      biasSpeedR=abs(round(speed*bias));
      biasSpeedL=abs(round(speed*(1.0-bias)));
    }
  }
//  Serial.print("bias=");Serial.println(bias);
//  Serial.print("Speed=");Serial.println(speed);
//  Serial.print("L=");Serial.println(biasSpeedL);
//  Serial.print("R=");Serial.println(biasSpeedR);
  if(rotate==0){
    if(direction==0){
      // Stop the motor fast
      speed=0;
      analogWrite(PWMPin, 0);
      analogWrite(PWMPinA, 0);
      analogWrite(PWMPin2, 0);
      analogWrite(PWMPinA2, 0);
      digitalWrite(EnablePin, LOW);
    } if(direction>0){
      // Forward
      analogWrite(PWMPin, biasSpeedL);
      analogWrite(PWMPinA, biasSpeedR);
      analogWrite(PWMPin2, 0);
      analogWrite(PWMPinA2, 0);
      digitalWrite(EnablePin, HIGH);
    } else {
      // Backward
      analogWrite(PWMPin, 0);
      analogWrite(PWMPinA, 0);
      analogWrite(PWMPin2, biasSpeedL);
      analogWrite(PWMPinA2,biasSpeedR);
      digitalWrite(EnablePin, HIGH);
    }
  } else {
    // Rotation makes wheels always run in opposite directions
    if(direction==0){
      // Stop the motor fast
      speed=0;
      analogWrite(PWMPin, 0);
      analogWrite(PWMPinA,0);
      analogWrite(PWMPin2, 0);
      analogWrite(PWMPinA2, 0);
      digitalWrite(EnablePin, LOW);
    } if(rotate>0){
      // Left
      //Serial.println("lf");
      analogWrite(PWMPin, 50);
      analogWrite(PWMPinA, 0);
      analogWrite(PWMPin2, 0);
      analogWrite(PWMPinA2,50);
      digitalWrite(EnablePin, HIGH);
    } if(rotate<0) {
      // Backward
      analogWrite(PWMPin, 0);
      analogWrite(PWMPinA,50 );
      analogWrite(PWMPin2,50);
      analogWrite(PWMPinA2,0);
      digitalWrite(EnablePin, HIGH);
    }
  }
}

/*
 * Divides a given PWM pin frequency by a divisor.
 *
 * The resulting frequency is equal to the base frequency divided by
 * the given divisor:
 *   - Base frequencies:
 *      o The base frequency for pins 3, 9, 10, and 11 is 31250 Hz.
 *      o The base frequency for pins 5 and 6 is 62500 Hz.
 *   - Divisors:
 *      o The divisors available on pins 5, 6, 9 and 10 are: 1, 8, 64,
 *        256, and 1024.
 *      o The divisors available on pins 3 and 11 are: 1, 8, 32, 64,
 *        128, 256, and 1024.
 *
 * PWM frequencies are tied together in pairs of pins. If one in a
 * pair is changed, the other is also changed to match:
 *   - Pins 5 and 6 are paired (Timer0)
 *   - Pins 9 and 10 are paired (Timer1)
 *   - Pins 3 and 11 are paired (Timer2)
 *
 * Note that this function will have side effects on anything else
 * that uses timers:
 *   - Changes on pins 5, 6 may cause the delay() and
 *     millis() functions to stop working. Other timing-related
 *     functions may also be affected.
 *   - Changes on pins 9 or 10 will cause the Servo library to function
 *     incorrectly.
 *
 * Thanks to macegr of the Arduino forums for his documentation of the
 * PWM frequency divisors. His post can be viewed at:
 *   http://www.arduino.cc/cgi-bin/yabb2/YaBB.pl?num=1235060559/0#4
 */

void setPwmFrequency(int pin, int divisor) {
  byte mode;
  if(pin == 5 || pin == 6 || pin == 9 || pin == 10) { // Timer0 or Timer1
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 64: mode = 0x03; break;
      case 256: mode = 0x04; break;
      case 1024: mode = 0x05; break;
      default: return;
    }
    if(pin == 5 || pin == 6) {
      TCCR0B = TCCR0B & 0b11111000 | mode; // Timer0
    } else {
      TCCR1B = TCCR1B & 0b11111000 | mode; // Timer1
    }
  } else if(pin == 3 || pin == 11) {
    switch(divisor) {
      case 1: mode = 0x01; break;
      case 8: mode = 0x02; break;
      case 32: mode = 0x03; break;
      case 64: mode = 0x04; break;
      case 128: mode = 0x05; break;
      case 256: mode = 0x06; break;
      case 1024: mode = 0x7; break;
      default: return;
    }
    TCCR2B = TCCR2B & 0b11111000 | mode; // Timer2
  }
}

float echoRangeFinder() {
  pinMode(ultrasonicRangeFinderPin, OUTPUT);          // Set pin to OUTPUT
  digitalWrite(ultrasonicRangeFinderPin, LOW);        // Ensure pin is low
  delayMicroseconds(2);
  digitalWrite(ultrasonicRangeFinderPin, HIGH);       // Start ranging
  delayMicroseconds(5);              //   with 5 microsecond burst
  digitalWrite(ultrasonicRangeFinderPin, LOW);        // End ranging
  pinMode(ultrasonicRangeFinderPin, INPUT);           // Set pin to INPUT
  int duration = pulseIn(ultrasonicRangeFinderPin, HIGH); // Read echo pulse
  float inches = duration / 74 / 2;        // Convert to inches
  //Serial.println(inches);            // Display result
  return inches;
}

float readHeading(){
  int x,y,z; //triple axis data

  //Tell the HMC5883 where to begin reading data
  Wire.beginTransmission(compassI2CAddress);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();

  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(compassI2CAddress, 6);
  if(6<=Wire.available()){
    x = Wire.read()<<8; //X msb
    x |= Wire.read(); //X lsb
    z = Wire.read()<<8; //Z msb
    z |= Wire.read(); //Z lsb
    y = Wire.read()<<8; //Y msb
    y |= Wire.read(); //Y lsb
  }
//  Serial.print(x);
//    Serial.print("\t");
//      Serial.println(y);
//    Serial.print(",");
//        Serial.println(z);
  int cy=-330;
  int cx=33;

  int dy=y-cy;
  int dx=x-cx;
//    Serial.print("dx,dy=");
//    Serial.print(dx);
//    Serial.print(",");
//        Serial.println(dy);
  float ratio=(float)dy/(float)dx;
//    Serial.print("Ratio=");
//        Serial.println(ratio);
  float rawAngle=abs(atan(ratio)*180.0/pi);
  if(dx>0&&dy<=0){
    //Serial.println("+-");
    return 360-rawAngle;
  }
  if(dx<=0&&dy<=0){
    //Serial.println("--");
    return rawAngle+180;
  }
  if(dx<=0&&dy>0){
    //Serial.println("-+");
    return 180-rawAngle;
  }
  if(dx>0&&dy>0){
    //Serial.println("++");
    return rawAngle;
  }

}

int readline(int readch, char *buffer, int len){

  static int pos = 0;
  int rpos;

  if (readch > 0) {

    switch (readch) {
      case '\r':
        rpos = pos;
        pos = 0;  // Reset position index ready for next time
        return rpos;
      default:
        if (pos < len-1) {
          buffer[pos++] = readch;
          buffer[pos] = 0;
        }
    }
  }
  // No end of line has been found, so return -1.
  return -1;
}

void processMessage(aJsonObject *msg){
    aJsonObject  *rotate = aJson.getObjectItem(msg, "rotate");
    aJsonObject  *goforward = aJson.getObjectItem(msg, "goforward");
    aJsonObject  *gobackward = aJson.getObjectItem(msg, "gobackward");
    aJsonObject  *stopnow = aJson.getObjectItem(msg, "stop");

   if (rotate->type == aJson_String) {
      String direction=(String(rotate->valuestring));
      float bias=0;
      if(direction.equals("LEFT")){
        persistantSpeed=SPEED_FAST;
        persistantDirection=DIRECTION_FORWARD;
        persistantBias=0.5;
        persistantRotation=LEFT_ROTATION;
      } else {
        persistantSpeed=SPEED_FAST;
        persistantDirection=DIRECTION_FORWARD;
        persistantBias=-0.5;
        persistantRotation=RIGHT_ROTATION;
      }
      Serial.println("{\"response\":\"OK rotate\"}");
      return;
    }
    if (goforward->type == aJson_Int) {
      int aspeed=goforward->valueint;
      persistantSpeed=aspeed;
      persistantDirection=DIRECTION_FORWARD;
      persistantBias=0;
      persistantRotation=NO_ROTATION;
      Serial.println("{\"response\":\"OK goforward\"}");
      return;
    }

    if (gobackward->type == aJson_Int) {
      int aspeed=gobackward->valueint;
      persistantSpeed=aspeed;
      persistantDirection=DIRECTION_BACKWARD;
      persistantBias=0;
      persistantRotation=NO_ROTATION;
     Serial.println("{\"response\":\"OK gobackward\"}");
     return;
    }

    if (gobackward->type == aJson_String) {
      //lcd.print(String(line3->valuestring));
      persistantSpeed=SPEED_FAST;
      persistantDirection=DIRECTION_BACKWARD;
      persistantBias=0;
      persistantRotation=NO_ROTATION;
     Serial.println("{\"response\":\"OK gobackward\"}");
     return;
    }

    if (stopnow->type == aJson_True) {
      float bias=0;
      controlMotor(0,DIRECTION_STOP,bias,NO_ROTATION);
      persistantSpeed=SPEED_STOP;
      persistantDirection=DIRECTION_STOP;
      persistantBias=0;
      persistantRotation=NO_ROTATION;
      Serial.println("{\"response\":\"OK stop\"}");
      return;

    }
    Serial.println("{\"response\":\"ERROR unknown\"}");
}

void processReceivedMessages(){
    static char buffer[200];
    if (readline(Serial.read(), buffer, 200) > 0) {
        Serial.println(buffer);
        aJsonObject *msg = aJson.parse(buffer);
        processMessage(msg);
        aJson.deleteItem(msg);
    }
}
