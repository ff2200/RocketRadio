#include <stdlib.h>
#include <stdint.h>
#include "radio_msg.h"
#include "crc32.h"
/*
   Basic frame example:
     ESC ESC,
       STX,
           DATA,
         ETX,
           CRC (unsigned long),
*/
// TODO: encapsulate generation of header,payload and CRC so that in one frame more than one msg can fit

uint8_t radioMsg[MAX_FRAME_SIZE] = { 0x00 };

// calculate worst case size stuffed Msg:
#define MAX_STUFFED_FRAME_SIZE (MAX_FRAME_SIZE + (MAX_FRAME_SIZE/254))
static uint8_t stuffedRadioMsg[MAX_STUFFED_FRAME_SIZE] = { 0x00 };
// COBS Functionality:http://www.stuartcheshire.org/papers/COBSforToN.pdf
size_t cobs_encode(const uint8_t * input, size_t len, uint8_t * output);

static uint8_t* clearRadioMsg();
static uint8_t* calculateCRC(uint8_t* payload);

uint8_t* buildRadioMesg(uint8_t* payload, size_t const in_len, size_t * const out_len) {
  clearRadioMsg();
  
  size_t i = 0;
    
  // build header
  radioMsg[i++] = ESC;
  radioMsg[i++] = ESC;
  
  // build payload, data length is first in payload
  radioMsg[i++] = STX;
  for(size_t x=0; x<in_len; ++x)
    radioMsg[i++] = *payload++;

  radioMsg[i++] = ETX;

  // build CRC
  uint32_t crc = crc_string(radioMsg, i-1); // ETX is not in crc. change? yes/no?

//  Serial.print("CRC: ");
//  Serial.println(crc,HEX);

  void* cast_ptr = NULL;
  uint8_t* byte_ptr = NULL;
  cast_ptr = (void*)&crc;
  byte_ptr = (uint8_t*)cast_ptr;
  
  for(size_t x=0; x<sizeof(uint32_t); ++x)
    radioMsg[i++] = *byte_ptr++;
  
  cast_ptr = byte_ptr = NULL;

  
/*  
  Serial.println("======");
  Serial.println(i, HEX);

  int x = 0;
  while(x < i) {
    char q = radioMsg[x++];
    Serial.println(q, HEX);
  }
*/
  *out_len = cobs_encode(radioMsg, i, stuffedRadioMsg);
  //Serial.println(*out_len,HEX);

  return stuffedRadioMsg;
}


static uint8_t* clearRadioMsg() {
  for (size_t i = 0; i < MAX_FRAME_SIZE; ++i)
    radioMsg[i] = '\0';
  for (size_t i = 0; i < MAX_STUFFED_FRAME_SIZE; ++i)
    stuffedRadioMsg[i] = 0x00;
  return radioMsg;
}


size_t cobs_encode(const uint8_t * input, size_t len, uint8_t * output) {
    size_t read_index = 0;
    size_t write_index = 1;
    size_t code_index = 0;
    uint8_t code = 1;

    while(read_index < len) {
        if(input[read_index] == 0)  {
            output[code_index] = code;
            code = 1;
            code_index = write_index++;
            read_index++;
        }
        else  {
            output[write_index++] = input[read_index++];
            code++;
            if(code == 0xFF) {
                output[code_index] = code;
                code = 1;
                code_index = write_index++;
            }
        }
    }

    output[code_index] = code;

    return write_index;
}
