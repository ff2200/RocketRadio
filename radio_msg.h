#ifndef RADIO_MSG_INCLUDED
#define RADIO_MSG_INCLUDED

/* ASCII Controll Characters
   Used to build a message frame
   
   

   Basic frame example:
     ESC ESC,
       STX,
           DATA,
         ETX,
           CRC (unsigned long),
       
     
      
*/

#define MAX_FRAME_SIZE 255 // be sure that this is large enough

/* Control Characters to build frame */
#define NUL 0x00      // Absolut termination of every message
#define SOH 0x01      // Start of every message
#define STX 0x02      // Start of every sub message, payload
#define ETX 0x03      // End of every sub message, payload
#define ETB 0x04      // Signal that message is over
#define ESC 0x1B      // Praeamble

/* buildRadioMesg(...): build a message frame to send to radio, args must be null terminated*/
uint8_t* buildRadioMesg(uint8_t* payload, size_t const, size_t * const);


#endif // RADIO_MSG_INCLUDED
