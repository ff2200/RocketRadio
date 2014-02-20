#ifndef SD_H_INCLUDED
#define SD_H_INCLUDED

void setupSD(void);
void writeToSdCard(uint8_t* payload, size_t len);

#endif // SD_H_INCLUDED

