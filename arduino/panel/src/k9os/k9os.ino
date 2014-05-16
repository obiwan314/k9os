/**
 * K9 OS v1.0
 *
 */
#include <Wire.h>
#include <LCD.h>
#include <LiquidCrystal_I2C.h>
#include <aJSON.h>

#define I2C_ADDR    0x3F  // Define I2C Address where the PCF8574A is
#define BACKLIGHT_PIN     3
#define En_pin  2
#define Rw_pin  1
#define Rs_pin  0
#define D4_pin  4
#define D5_pin  5
#define D6_pin  6
#define D7_pin  7
byte U4PortAP=0, U4PortBP=0, U4PortA=0, U4PortB =0; // Define variables to hold I/O port readings.
int testModeCounter=0;
int n = 1;
int debug=0;
int testmodeStatus=0;
unsigned long last_print = 0;
//aJsonStream serial_stream(&Serial);
LiquidCrystal_I2C lcd(I2C_ADDR,En_pin,Rw_pin,Rs_pin,D4_pin,D5_pin,D6_pin,D7_pin);
int pattern=0;
void setup()
{
  lcd.begin (20,4);
  
  // Switch on the backlight
  lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
  lcd.setBacklight(HIGH);
  lcd.home ();                   // go home

  lcd.print(" *** K9 OS 0.1a *** ");  
  lcd.setCursor ( 0, 1 );        // go to the 2nd line
  lcd.print("   SYSTEM BOOTING    ");
  lcd.setCursor ( 0, 2 );        // go to the third line
  lcd.print("    PLEASE WAIT");
  lcd.setCursor ( 0, 3 );        // go to the fourth line
  lcd.print("");
  
  // Setup Serial Communications
  Serial.begin(115200);
  setupKeypad();
  
}

void setupKeypad()
{
   Wire.begin();                                  // Begin I2C bus
   /* 
    *  The following code starts I2C communication with MCP23017(U2).Please refer MCP23017 datasheet
    *  for register addresses. Sets all GPIOs of this IC to OUTPUT 
    */
   Wire.beginTransmission(0x20);                  // Starts communication with MCP23017(U2) IC
   Wire.write(0x00);                              // Set MCP23017 memory pointer to IODIRA address
   Wire.write(0x00);                              // Set all pins of PORTA to outputs
   Wire.endTransmission();                        // Ends I2C communication with MCP23017(U2) IC

   Wire.beginTransmission(0x20);                  // Starts communication with MCP23017(U2) IC
   Wire.write(0x01);                              // Set MCP23017 memory pointer to IODIRB address
   Wire.write(0x00);                              // Set all pins of PORTB to outputs
   Wire.endTransmission();                        // Ends I2C communication with MCP23017(U2) IC

   /* 
    *  The following code starts I2C communication with MCP23017(U4).Please refer MCP23017 datasheet
    *  for register addresses. Sets all GPIOs of this IC to OUTPUT 
    */
   Wire.beginTransmission(0x21);                  // Starts communication with MCP23017(U4) IC
   Wire.write(0x00);                              // Set MCP23017 memory pointer to IODIRA address
   Wire.write(0xFF);                              // Set all PORTA pins to OUTPUT
   Wire.endTransmission();                        // Ends I2C communication with MCP23017(U4) IC

   Wire.beginTransmission(0x21);                  // Starts communication with MCP23017(U4) IC
   Wire.write(0x01);                              // Set MCP23017 memory pointer to IODIRB address
   Wire.write(0xFF);                              // Set all PORTB pins to OUTPUT
   Wire.endTransmission();                        // Ends I2C communication with MCP23017(U4) IC
   DigitalIO(0);
}

void clearlcdnow(){
//  lcd.setCursor ( 0, 0 );
//  lcd.print("                    ");
  lcd.setCursor ( 0, 1 );
  lcd.print("                    ");
  lcd.setCursor ( 0, 2 );
  lcd.print("                    ");
  lcd.setCursor ( 0, 3 );
  lcd.print("                    ");
}

void sendKeyboardEvents(byte a, byte ax,byte b,byte bx){
  String response="";
  if((bx&1)==1){
    if((b&1)==1){
      response=response+"\"key1\":\"down\",";  
    } else {
      response=response+"\"key1\":\"up\",";  
    }  
  }
  if((bx&2)==2){
    if((b&2)==2){
      response=response+"\"key2\":\"down\",";  
    } else {
      response=response+"\"key2\":\"up\",";  
    }  
  }
  if((bx&4)==4){
    if((b&4)==4){
      response=response+"\"key3\":\"down\",";  
    } else {
      response=response+"\"key3\":\"up\",";  
    }  
  }
  if((bx&8)==8){
    if((b&8)==8){
      response=response+"\"key4\":\"down\",";  
    } else {
      response=response+"\"key4\":\"up\",";  
    }  
  }
  if((bx&16)==16){
    if((b&&16)==16){
      response=response+"\"key5\":\"down\",";  
    } else {
      response=response+"\"key5\":\"up\",";  
    }  
  }
  if((bx&32)==32){
    if((b&32)==32){
      response=response+"\"key6\":\"down\",";  
    } else {
      response=response+"\"key6\":\"up\",";  
    }  
  }
  if((bx&64)==64){
    if((b&64)==64){
      response=response+"\"key7\":\"down\",";  
    } else {
      response=response+"\"key7\":\"up\",";  
    }  
  }
  if((bx&128)==128){
    if((b&128)==128){
      response=response+"\"key8\":\"down\",";  
    } else {
      response=response+"\"key8\":\"up\",";  
    }  
  }
  if((ax&16)==16){
    if((a&16)==16){
      response=response+"\"key9\":\"down\",";  
    } else {
      response=response+"\"key9\":\"up\",";  
    }  
  }
  if((ax&32)==32){
    if((a&32)==32){
      response=response+"\"key10\":\"down\",";  
    } else {
      response=response+"\"key10\":\"up\",";  
    }  
  }
  if((ax&64)==64){
    if((a&64)==64){
      response=response+"\"key11\":\"down\",";  
    } else {
      response=response+"\"key11\":\"up\",";  
    }  
  }
  if((ax&128)==128){
    if((a&128)==128){
      response=response+"\"key12\":\"down\",";  
    } else {
      response=response+"\"key12\":\"up\",";  
    }  
  }
  
  response="{"+response.substring(0, response.length() - 1)+"}";
  Serial.println(response);

}

void readKeyboard(){
   Wire.beginTransmission(0x21);            // Start I2C communication with MCP23017(U4)
   Wire.write(0x12);                        // Set MCP23017 memory pointer to PORTA address
   Wire.endTransmission();                  // Ends I2C communication with U4
   Wire.requestFrom(0x21, 1);               // Request one byte of data from MCP20317(U4)
   U4PortA=Wire.read();                     // Store the incoming byte of PORTA into "U4PortA"
 
   Wire.beginTransmission(0x21);            // Start I2C communication with U4
   Wire.write(0x13);                        // Set MCP23017 memory pointer to PORTB address
   Wire.endTransmission();                  // Ends I2C communication with U4
   Wire.requestFrom(0x21, 1);               // Request one byte of data from MCP20317
   U4PortB=Wire.read();                     // Store the incoming byte of PORTB into "U4PortB"
//   if((U4PortA^U4PortAP)>0){
//     Serial.print("U4 PORTA: " );
//     Serial.print(U4PortAP, BIN);
//     Serial.print("|");
//     Serial.print(U4PortA, BIN);            // Print the contents of the PORTA register in binary
//     Serial.print("+");
//     Serial.println(U4PortA^U4PortAP);            // Print the contents of the PORTA register in binary
//   }
//   if((U4PortB^U4PortBP)>0){
//     Serial.print("U4 PORTB: " );
//     Serial.print(U4PortBP, BIN);            // Print the contents of the PORTB register in binary
//     Serial.print("|");
//     Serial.print(U4PortB, BIN);            // Print the contents of the PORTB register in binary
//     Serial.print("+");
//     Serial.println(U4PortBP^U4PortB);            // Print the contents of the PORTB register in binary
//   }
   
   if((U4PortA^U4PortAP)>0){     
     sendKeyboardEvents(U4PortA,U4PortA^U4PortAP,0,0);
   }
   if((U4PortB^U4PortBP)>0){     
     sendKeyboardEvents(0,0,U4PortB,(U4PortB^U4PortBP));
   }

   
   U4PortAP=U4PortA;
   U4PortBP=U4PortB;
  
}


void DigitalIO(int i)
{
   Wire.beginTransmission(0x20);
   Wire.write(0x12);                             
   Wire.write(highByte(i));                                 // Set or clear PORTA pins of U2
   Wire.endTransmission();
   
   Wire.beginTransmission(0x20);
   Wire.write(0x13);                              
   Wire.write(lowByte(i));                                 // Set or clear PORTB pins of U2
   Wire.endTransmission();
}

int readline(int readch, char *buffer, int len)
{
  
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

void processReceivedMessages(){
    static char buffer[200];
    if (readline(Serial.read(), buffer, 200) > 0) {
        aJsonObject *msg = aJson.parse(buffer);
        processMessage(msg);        
        aJson.deleteItem(msg);
    }  
}

void loop(){
    //Serial.print("."); 
    readKeyboard();
    processReceivedMessages();
    if(testmodeStatus>0){
      if(testModeCounter>50){
         clearlcdnow();
         lcd.setCursor ( 0, 1 );
         lcd.print(" KEYBOARD TEST MODE ");
         
         int curent=pow(2,pattern); 
         lcd.setCursor ( 13, 2 );        // go to the third line
         lcd.print(curent);
         if(pattern>1)
            curent=curent+1; 
         lcd.setCursor ( 6, 2 );        // go to the third line
         lcd.print(pattern);
         DigitalIO(curent);
         pattern++;
         if(pattern>11){
           pattern=0;
          testModeCounter=0;
         }
      } else {
        testModeCounter=testModeCounter+1;
      }
     }
       
     return;
}


void processMessage(aJsonObject *msg){
      
    aJsonObject  *line1 = aJson.getObjectItem(msg, "line1");
    aJsonObject  *line2 = aJson.getObjectItem(msg, "line2");
    aJsonObject  *line3 = aJson.getObjectItem(msg, "line3");
    aJsonObject  *line4 = aJson.getObjectItem(msg, "line4");
    aJsonObject  *backlighton = aJson.getObjectItem(msg, "backlighton");
    aJsonObject  *backlightoff = aJson.getObjectItem(msg, "backlightoff");
    aJsonObject  *testmodeon = aJson.getObjectItem(msg, "testmodeon");
    aJsonObject  *testmodeoff = aJson.getObjectItem(msg, "testmodeoff");    
    aJsonObject  *lightcode = aJson.getObjectItem(msg, "lightcode");
    aJsonObject  *clearlcd = aJson.getObjectItem(msg, "clearlcd");
    
    if (clearlcd->type == aJson_True) {
      clearlcdnow();
      Serial.println("{\"response\":\"OK\"}");
    }
    
    if (line1->type == aJson_String) {
      lcd.setCursor (0,0);
      lcd.print(String(line1->valuestring));
      Serial.println("{\"response\":\"OK\"}");
    } 
   if (line2->type == aJson_String) {
      lcd.setCursor (0,1);
      lcd.print(String(line2->valuestring));
      Serial.println("{\"response\":\"OK\"}");
    } 
    if (line3->type == aJson_String) {
      lcd.setCursor (0,2);
      lcd.print(String(line3->valuestring));
      Serial.println("{\"response\":\"OK\"}");
    } 
    if (line4->type == aJson_String) {
      lcd.setCursor (0,3);
      lcd.print(String(line4->valuestring));
      Serial.println("{\"response\":\"OK\"}");
    } 
    if (backlightoff->type == aJson_True) {     
        lcd.setBacklightPin(BACKLIGHT_PIN,POSITIVE);
        Serial.println("{\"response\":\"OK\"}");
    }
    
    if (backlighton->type == aJson_True) {
        lcd.setBacklightPin(BACKLIGHT_PIN,NEGATIVE);
        Serial.println("{\"response\":\"OK\"}");
    }
     
    if (testmodeoff->type == aJson_True) {
         testmodeStatus=0;
         clearlcdnow();
         DigitalIO(0);
         Serial.println("{\"response\":\"OK\"}");
    }
          
    if (testmodeon->type == aJson_True) {
          testmodeStatus=1;
          Serial.println("{\"response\":\"OK\"}");
    }
         
    if (lightcode->type == aJson_Int) {
//      Serial.print("lightcode=");
//      Serial.print(lightcode->valueint);
      DigitalIO(lightcode->valueint);
      Serial.println("{\"response\":\"OK\"}");
    }
    
    

}

