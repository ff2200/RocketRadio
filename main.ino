/* 
  Commands for picocom:
    Arduino Serial: picocom --omap crcrlf -b 9600 /dev/ttyACMX
    3dR Radio: picocom -b 57600 /dev/ttyUSBX
*/


#include <stdint.h>
#include "radio.h"
#include "input_util.h"
#include "sdcard.h"



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
  setupSD();
  Serial.begin(9600);
}

data pl = { sizeof(data), 8.3, 16.5, 255 };
uint8_t tick = 0;

void loop() {
  // put your main code here, to run repeatedly:
  pl.tick = tick++;
  sdata spl;
  spl.dat = &pl;
  
  writeToRadio(spl.ptr,sizeof(data));  

  delay(1000);
}



