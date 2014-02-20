#!/usr/bin/env python

CRTL_CHAR = { 0x00: 'NUL', # Absolut termination of every message
              0x01: 'SOH', # Start of every message
              0x02: 'STX', # Start of every sub message, payload
              0x03: 'ETX', # End of every sub message, payload
              0x04: 'ETB', # Signal that message is over
              0x1D: 'GS' , # Used for seperation
              0x1B: 'ESC', # PRAEAMBLE
             }



if __name__ == '__main__':
    import serial
    import struct
    from argparse import ArgumentParser
    optp = ArgumentParser(description='Open a port, with buadrate to communicate with arduino radio')
    optp.add_argument('port', type=str, help='port to open')
    optp.add_argument('baudrate', type=int, help='baudrate to use')

    args = optp.parse_args()
    ser = serial.Serial(args.port, args.baudrate)

    structure = struct.Struct('<xxxIffBxI')
    from collections import namedtuple
    from cobs import cobs
    from zlib import crc32
    try:

        stack = []
        def pushStack(x):
            stack.append(x)
        def popStack():
            if len(stack) > 0:
                return stack.pop()
            return ser.read(1)

        def checkMsg(data):
            if CRTL_CHAR[data[0]] != 'ESC': return False
            if CRTL_CHAR[data[1]] != 'ESC': return False
            if CRTL_CHAR[data[2]] != 'STX': return False
            if CRTL_CHAR[data[16]] != 'ETX': return False
            return True

        while(1):
            recv = popStack()
            if (recv != b'\x00'):
               print("SYNC..\t {0}".format(recv))
               continue

            data = bytearray()

            while(1):
                recv = popStack()
                if recv == b'\x00':
                    pushStack(recv)
                    break
                data.append(ord(recv))

            if (len(data) <=0): continue

            print("\nNEW MESSAGE \t {0}".format(recv))
            data = cobs.decode(data)
            print(data)
            print(checkMsg(data))
            crc = crc32(data[:-5])
            print(crc)
            datatuple = namedtuple('DATA', 'len  b a tick crc')
            print(datatuple._make(structure.unpack(data)))
    finally:
        ser.close()
