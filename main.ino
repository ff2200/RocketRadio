/* 
  Commands for picocom:
    Arduino Serial: picocom --omap crcrlf -b 9600 /dev/ttyACMX
    3dR Radio: picocom -b 57600 /dev/ttyUSBX
*/


#include <stdint.h>
#include "radio.h"
#include "input_util.h"



typedef struct data {
  uint32_t datalen;
  double b;
  float a;
  uint8_t tick;

} data;

typedef union {
  data* dat;
  uint8_t* ptr;
} sdata;
  


void setup() {
  // put your setup code here, to run once:
  setupRadioLink();
  
  Serial.begin(9600);

}

data pl = { sizeof(data), 8.3, 16.5, 255 };


void loop() {
  Serial.println("\n++++++++++++++++++++++++++++++++++++\nDATA Size");
  Serial.println(sizeof(data), DEC);
  Serial.println(sizeof(float), DEC);
  // put your main code here, to run repeatedly:
  sdata spl;
  spl.dat = &pl;
  
  writeToRadio(spl.ptr,sizeof(data));  
  delay(1000);
}



