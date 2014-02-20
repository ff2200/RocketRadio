#include <stdint.h>
#include "input_util.h"


static char buf[BUF_SIZE] = { 0 };
static unsigned int pos = 0;

static char* clearBuffer();

static char* clearBuffer() {
  for (int i = 0; i < BUF_SIZE; ++i)
    buf[i] = '\0';
  pos = 0;
  return buf;
}

char* readLine() {
  clearBuffer();
  char c;
  while (true) {
    // make IO blocking
    if (Serial.available()) {
      c = (char)Serial.read();
      if (c == '\n' || pos >= BUF_SIZE) {
        break;
      }
      buf[pos++] = c;
    }
  }
  buf[--pos] = '\0';
  pos = 0;
  return buf;
}
