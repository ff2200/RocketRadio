import struct
from collections import namedtuple
from cobs import cobs
from zlib import crc32
from json import dumps

CRTL_CHAR = { 0x00: 'NUL',  # Absolut termination of every message
              0x01: 'SOH',  # Start of every message -- NOT USED
              0x02: 'STX',  # Start of every sub message, payload
              0x03: 'ETX',  # End of every sub message, payload
              0x04: 'ETB',  # Signal that message is over -- NOT USED
              0x1D: 'GS',   # Used for seperation -- NOT USED
              0x1B: 'ESC',  # PRAEAMBLE
             }


class RgsLibException(Exception):
    pass


class FormatInvalidException(RgsLibException):
    pass


class CrcInvalidException(RgsLibException):
    pass


class MsgBuffer():

    def __init__(self, source: 'must implement read/close'):
        self._stack = []
        self._source = source

    def getChar(self):
        char = ''
        if len(self._stack) > 0:
            char = self._stack.pop()
        else:
            char = self._source.read(1)
        return char

    def pushBack(self, x):
        self._stack.append(x)

    def _clearBuffer(self):
        self._stack = []


class TestMsg():

    # change x to real bytes , could make check format more object oriented
    STUCTURE = struct.Struct('<xxxIffBxI')
    RocketData = namedtuple('RocketData', 'len b a tick crc')

    def construct(self, clear_data):
        if clear_data is None: return None
        self._checkFormat(clear_data)
        if not self._checkFormat(clear_data): raise FormatInvalidException()
        data = self.RocketData._make(self.STUCTURE.unpack(clear_data))
        if not self._checkCrc(clear_data, data.crc): raise CrcInvalidException()
        return data

    def _checkFormat(self, clear_data):
        if CRTL_CHAR[clear_data[0]] != 'ESC': return False
        if CRTL_CHAR[clear_data[1]] != 'ESC': return False
        if CRTL_CHAR[clear_data[2]] != 'STX': return False
        if CRTL_CHAR[clear_data[16]] != 'ETX': return False
        return True

    def _checkCrc(self, clear_data, datacrc):
        msg_crc = crc32(clear_data[:-4])  # -4 for CRC
        return datacrc == msg_crc


class ReceiveLoop():
    MSG_BREAK = b'\x00'

    def __init__(self, msgfac, msgbuffer, filelog_data=None,
                 filelog_raw=None):
        self._buffer = msgbuffer
        self._msgfac = msgfac
        self.msgs = []
        self.filelog_data = filelog_data
        self.filelog_raw = filelog_raw
        self._log_data_raw(self.MSG_BREAK)  # ensure correct beginning

    def _sync(self):
        # incooperate this into _read_block() ?
        # and how to unittest ?
        while(1):
            recv = self._buffer.getChar()
            if (recv == self.MSG_BREAK):
                break

    def _read_block(self):
        char = b''
        while(char == b''): char = self._buffer.getChar()
        self._log_data_raw(char)
        if (char == self.MSG_BREAK):
            self._buffer.pushBack(char)
            return None  # finish block

        return ord(char)  # get int code point of byte

    def start(self):
        while(1):
            try:
                data = self._msgfac.construct(self._start_functionality())
                self.msgs.append(data)
                self._log_data_json(data)
                yield data
            except Exception as ex:
                #logging.error(ex)
                raise ex

    def _log_data_raw(self, char):
        if self.filelog_raw is not None:
            try:
                self.filelog_raw.write(char)
            except Exception as ex:
                raise ex

    def _log_data_json(self, data):
        if self.filelog_data is not None and data is not None:
            try:
                # Note: can't use dump -> repeated calls to 'dump()' with same
                # fp result in invalid JSON file (see documentation)
                self.filelog_data.write(dumps(data._asdict()) + '\n')
            except Exception as ex:
                raise ex

    def _start_functionality(self):
        raw_data = bytearray()
        clear_data = None

        self._sync()  # wait till wie get the break
        while(1):
            char = self._read_block()
            if char is not None:
                raw_data.append(char)
            else:
                break  # if block finished
        if (not len(raw_data) > 0): return None
        clear_data = cobs.decode(raw_data)
        return clear_data


def receive(source: 'must implement open/close', filelog_data=None,
            filelog_raw=None):
    buffer = MsgBuffer(source)
    factory = TestMsg()
    mainLoop = ReceiveLoop(factory, buffer, filelog_data, filelog_raw)
    try:
        for item in mainLoop.start():
            yield item
    except Exception as ex:
        raise ex

