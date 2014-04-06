/*
  MegaMoto Test Sketch
  Simply runs a motor back and forth
  ramping the speed from 0 to full (255)
 
  This example code is in the public domain.
 */
#include <Wire.h> //I2C Arduino Library
#include <math.h>
// megamoto
int EnablePin = 8;
int duty;
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
const byte CPin = 0;  // analog input channel
const float pi = 3.14159;
const int address=0x1E;
float lastHeading=-2;
float lastRange=-1;
int pingPin= 4;
int CRaw;      // raw A/D value
float CVal;    // adjusted Amps value

// Remote Controll
int ch1; // Here's where we'll keep our channel values
int ch2;
int ch3;

int speed=0;

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

  // Set up compass
  Wire.begin();
  
  //Put the HMC5883 IC into the correct operating mode
  Wire.beginTransmission(address); //open communication with HMC5883
  Wire.write(0x02); //select mode register
  Wire.write(0x00); //continuous measurement mode
  Wire.endTransmission();

  Serial.begin(9600); // Pour a bowl of Serial
  
}
static inline int8_t sgn(int val) {
  if (val < 0) return -1;
  if (val==0) return 0;
  return 1;
}
void controlMotor(int speed,int direction,float bias){
  
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
}

void loop() {
  // To drive the motor in H-bridge mode
  // the power chip inputs must be opposite polarity
  // and the Enable input must be HIGH
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
  ch1 = pulseIn(5, HIGH, 25000); // Read the pulse width of 
  ch2 = pulseIn(6, HIGH, 25000); // each channel
  ch3 = pulseIn(7, HIGH, 25000);
  float bias=0;
  //Serial.print("CH3=");Serial.println(ch3);
  if(ch3<1500&&ch3>1490)
    bias=0;
  if(ch3<=1490)
    bias=-((ch3-1490)/190.0)*0.8;
  if(ch3>=1500)
    bias=((ch3-1500)/200.0)*0.8;
  //Serial.print("Bias=");Serial.println(bias);

  if(ch1<996){ // This sets SWB as the master motor cut off
    controlMotor(0,0,bias);
  } else {
     if(ch2<1400){
        controlMotor(SPEED_FASTER,DIRECTION_BACKWARD,bias);
     }
     if(ch2>=1400&&ch2<1425){
        controlMotor(SPEED_FAST,DIRECTION_BACKWARD,bias);
      }
      if(ch2>=1425&&ch2<1450){
          controlMotor(SPEED_SLOW,DIRECTION_BACKWARD,bias);
      }
      if(ch2>=1450&&ch2<1500){
        controlMotor(0,DIRECTION_STOP,bias);
      }
      if(currentRange>12.0){
        if(ch2>=1500&&ch2<1525){
            controlMotor(SPEED_SLOW,DIRECTION_FORWARD,bias);
        }
        if(ch2>=1525&&ch2<1550){
            controlMotor(SPEED_FAST,DIRECTION_FORWARD,bias);
         }
         if(ch2>=1550&&ch2<1575){
            controlMotor(SPEED_FASTER,DIRECTION_FORWARD,bias);
         }
         if(ch2>=1575&&ch2<1600){
            controlMotor(SPEED_FASTEST,DIRECTION_FORWARD,bias);
         }
         if(ch2>=1600&&ch2<1625){
            controlMotor(SPEED_RIDICULOUS,DIRECTION_FORWARD,bias);
         }
         if(ch2>=1625){
            controlMotor(SPEED_LUDICROUS,DIRECTION_FORWARD,bias);
         }
       }
      
  }
 // Serial.print("Channel 1:"); // Print the value of 
 // Serial.println(ch1);        // each channel

//  Serial.print("Channel 2:");
//  Serial.println(ch2);

//  Serial.print("Channel 3:");
//  Serial.println(ch3);

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
  pinMode(pingPin, OUTPUT);          // Set pin to OUTPUT
  digitalWrite(pingPin, LOW);        // Ensure pin is low
  delayMicroseconds(2);
  digitalWrite(pingPin, HIGH);       // Start ranging
  delayMicroseconds(5);              //   with 5 microsecond burst
  digitalWrite(pingPin, LOW);        // End ranging
  pinMode(pingPin, INPUT);           // Set pin to INPUT
  int duration = pulseIn(pingPin, HIGH); // Read echo pulse
  float inches = duration / 74 / 2;        // Convert to inches
  //Serial.println(inches);            // Display result
  return inches;
}
float readHeading(){
  int x,y,z; //triple axis data

  //Tell the HMC5883 where to begin reading data
  Wire.beginTransmission(address);
  Wire.write(0x03); //select register 3, X MSB register
  Wire.endTransmission();
  
  //Read data from each axis, 2 registers per axis
  Wire.requestFrom(address, 6);
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
