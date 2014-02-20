#include <stdint.h>
#include <stddef.h>

#include "radio.h"
#include "radio_msg.h"

/* DO NOT REMOVE THIS LINE: */
;
/* THIS IS ADVANCED MAGIC SEE: 
  http://forum.arduino.cc/index.php?topic=84412.0
*/


#ifdef RADIO_USE_SERIAL
  #define SERIAL (Serial)
#else
  // include needed libs if SoftwareSerial is used
  #include <SoftwareSerial.h>
  // Setup SoftwareSerial Ports
  static SoftwareSerial radioSerial(RADIO_RX_PORT, RADIO_TX_PORT);
  #define SERIAL (radioSerial)
#endif




/* setupRadioLink(): init RadioLink call this in setup() */
void setupRadioLink() {
#ifndef RADIO_USE_SERIAL
  // pinMode calls might be superficial
  pinMode(RADIO_RX_PORT, INPUT);
  pinMode(RADIO_TX_PORT, OUTPUT);
#endif
  SERIAL.begin(RADIO_BAUDRATE);
}

/* writeToRadio(...): write binary data to the reciever */
size_t writeToRadio(uint8_t* payload, size_t len) {
  size_t out_len = 0;
  uint8_t* data = buildRadioMesg(payload, len, &out_len);
  SERIAL.flush();
  SERIAL.write((uint8_t)0x00);
  SERIAL.write(data,out_len);
}



