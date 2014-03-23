import struct
from collections import namedtuple
from cobs import cobs
from zlib import crc32


CRTL_CHAR = { 0x00: 'NUL', # Absolut termination of every message
              0x01: 'SOH', # Start of every message -- NOT USED
              0x02: 'STX', # Start of every sub message, payload
              0x03: 'ETX', # End of every sub message, payload
              0x04: 'ETB', # Signal that message is over -- NOT USED
              0x1D: 'GS' , # Used for seperation -- NOT USED
              0x1B: 'ESC', # PRAEAMBLE
             }


class MsgBuffer():
    def __init__(self, source: 'must implement read/close'):
        self._stack = []
        self._source = source

    def getChar(self):
        if len(self._stack) > 0:
            yield self._stack.pop()
        else:
            yield self._source.read()

    def pushBack(self, x):
        self._stack.append(x)


class TestMsg():
    #TODO: unschoen, construct sollte in constructor sein, fehlerbhandlung ausserhalb, oder auslagerung in funktion
    STUCTURE = struct.Struct('<xxxIffBxI')
    RocketData = namedtuple('RocketData', 'len b a tick crc')

    def __init__(self, clear_data):
        self.clear_data = clear_data
        self.msgvalid = False

    def construct(self):
        try:
            self.formatvalid = self.checkFormat()
            self.data = self.RocketData._make(self.STUCTURE.unpack(self.clear_data)
            self.crcvalid = self.checkCrc()
            self.msgvalid = (self.crcvalid and self.formatvalid)
        except Exception:
            self.msgvalid = False
            return None
        else: return self

    def _checkFormat(self):
        if CRTL_CHAR[self.clear_data[0]] != 'ESC': return False
        if CRTL_CHAR[self.clear_data[1]] != 'ESC': return False
        if CRTL_CHAR[self.clear_data[2]] != 'STX': return False
        if CRTL_CHAR[self.clear_data[16]] != 'ETX': return False
        return True

    def _checkCrc(self):
        msg_crc = crc32(self.clear_data(:-5))  # -4 for CRC , -1 for ETX BYTE (if ETX is in arduino included into CRC calculation , modify here)
        return self.data == msg_crc


def RecieveLoop():
    MSG_BREAK = b'\x00'
    def __init__(self,msgfac, msgbuffer):
        self._buffer =  msgbuffer
        self._msgfac = msgfac
        self.msgs = []

    def _sync(self):
        while(1):
            recv = next(self._buffer.getChar())
            if (recv == MSG_BREAK):
               break

    def _read_block():
        char = yield from self._buffer.getChar()
        if (char == MSG_BREAK):
            self._buffer.pushBack(char)
            return None # finish block
        yield ord(char) # get int code point of byte

    def start():
        while(1):
            try:
                raw_data = bytearray()
                clear_data = None

                self._sync() # wait till wie get the break
                for char in self._read_block():
                    if char is not None:
                        raw_data.append(char)
                    else: break # if block finished
                clear_data = cobs.decode(raw_data)
                self.msgs.append(self._msgfac(clear_data).construct())
            except Exception as ex:
                logging.error(ex)



