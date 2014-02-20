#include <SPI.h>
#include <SD.h>
#include "sdcard.h"

// On the Ethernet Shield, CS is pin 4. Note that even if it's not
// used as the CS pin, the hardware CS pin (10 on most Arduino boards,
// 53 on the Mega) must be left as an output or the SD library
// functions will not work.
static int const chipSelect = 53;

static File dataFile;

void setupSD(void) {
  pinMode(10, OUTPUT);
  if (!SD.begin(chipSelect))
    Serial.println("SD is fucked up");
  return;
}

void writeToSdCard(uint8_t* payload, size_t len) {
  if (!dataFile) {
    Serial.println("opening file");
    dataFile = SD.open("datalog.bin", FILE_WRITE);
    
  }
  if (dataFile) {
    Serial.println("writing to file");
    dataFile.write((uint8_t)0x00);
    dataFile.write(payload, len);
    dataFile.close();
  }
}
  
