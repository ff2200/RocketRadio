#ifndef RADIO_H_INCLUDED
#define RADIO_H_INCLUDED

#include <stdint.h>
#include <stddef.h>
/*
  
  Arduino Mega2560 Notes:
  
  For SoftwareSerial: 
  
  Not all pins on the Mega and Mega 2560 support change interrupts, so only the following can be 
  used for RX: 10, 11, 12, 13, 14, 15, 50, 51, 52, 53, A8 (62), A9 (63), A10 (64), A11 (65), A12 (66),
  A13 (67), A14 (68), A15 ( 69). 
  (see: http://arduino.cc/en/Reference/SoftwareSerial)
  
  For Serial:
  The Arduino Mega has three additional serial ports: Serial1 on pins 19 (RX) and 18 (TX),
  Serial2 on pins 17 (RX) and 16 (TX), Serial3 on pins 15 (RX) and 14 (TX).
  (see: http://arduino.cc/en/Reference/Serial)
*/

/*
  This Module provides Methods to wirte to serial output.
  Radio can be connected on Serial (the standard serial ports) or SoftwareSerial.
  To use SoftwareSerial define RADIO_USE_SOFTWARE_SERIAL.
  
  Define RADIO_RX_PORT and RADIO_TX_PORT if RADIO_USE_SOFTWARE_SERIAL is defined.
  
  Baudrate of the radio has to be defined on the radio itself (config tool) and via
  RADIO_BAUDRATE define for Arduino.
  
  If Serial is used, be aware that the setupRadioLink sets
  Serial baudrate to RADIO_BAUDRATE.
*/

/* comment this to enable SoftwareSerial: */
#define RADIO_USE_SERIAL 

#ifndef RADIO_USE_SERIAL
// set TX / RX Port for SoftwareSerial
#define RADIO_RX_PORT 62
#define RADIO_TX_PORT 63
#endif

#define RADIO_BAUDRATE 57600


void setupRadioLink();

size_t writeToRadio(uint8_t*, size_t);



#endif // RADIO_H_INCLUDED

