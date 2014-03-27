
import unittest
import os
import io
from unittest import mock

from zlib import crc32
import struct
from collections import namedtuple
from cobs import cobs

import rgslib


class TestMsgBuffer(unittest.TestCase):

    def setUp(self):
        self.fd = io.BytesIO(b'\x01\x02\x03')
        self.obj = rgslib.MsgBuffer(self.fd)

    def tearDown(self):
        self.fd.close()
        del self.fd
        del self.obj

    def test_getChar(self):
        self.fd.seek(0)
        self.assertTrue(self.obj.getChar() == b'\x01')
        self.assertFalse(self.obj.getChar() == b'\x03')

    def test_pushBack(self):
        self.obj.pushBack(b'\x00')
        self.assertTrue(self.obj.getChar() == b'\x00')

    def test_getChar_empty(self):
        self.fd.seek(0, io.SEEK_END)
        self.assertTrue(self.obj.getChar() == b'')

    def test_fdClosed(self):
        fd = io.StringIO()
        obj = rgslib.MsgBuffer(fd)
        fd.close()
        self.assertRaises(ValueError, obj.getChar)

    def test_clearBuffer(self):
        obj = rgslib.MsgBuffer(None)
        obj._stack = [1,2,3]
        obj._clearBuffer()
        self.assertTrue(len(obj._stack) == 0)

class TestTestMsg(unittest.TestCase):

    def setUp(self):
        RocketData = namedtuple('RocketData', 'len b a tick crc')
        self.testdata = struct.pack('<bbbIffB', 0x1B, 0x1B, 0x02,  1, 1.5 ,2.5 , 155 )
        self.crc = crc32(self.testdata)
        self.testdata = struct.pack('<bbbIffBbI', 0x1B, 0x1B, 0x02,  1, 1.5 ,2.5 , 155, 0x03, self.crc)
        self.testtuple = RocketData._make(struct.unpack('<xxxIffBxI',self.testdata))

    def test_checkFormat(self):
        obj = rgslib.TestMsg()
        self.assertTrue(True, obj._checkFormat(self.testdata))

    def test_checkCrc(self):
        obj = rgslib.TestMsg()
        self.assertTrue(True, obj._checkCrc(self.testdata, self.crc))

    def test_construct(self):
        obj = rgslib.TestMsg()
        obj1 = obj.construct(self.testdata)
        self.assertTrue(obj1.len, self.testtuple.len)
        self.assertTrue(obj1.b, self.testtuple.b)
        self.assertTrue(obj1.a, self.testtuple.a)
        self.assertTrue(obj1.tick, self.testtuple.tick)
        self.assertTrue(obj1.crc, self.testtuple.crc)

    def tearDown(self):
        del self.testdata
        del self.crc
        del self.testtuple


class TestReceiveLoop(unittest.TestCase):
    def setUp(self):
        self.testdata = struct.pack('<bbbIffB', 0x1B, 0x1B, 0x02,  1, 1.5 ,2.5 , 155 )
        self.crc = crc32(self.testdata)
        self.testdata = struct.pack('<bbbIffBbI', 0x1B, 0x1B, 0x02,  1, 1.5 ,2.5 , 155, 0x03, self.crc)
        self.bufferobj = rgslib.MsgBuffer(io.BytesIO())
        self.da = b'\x00' + cobs.encode(self.testdata)

    def test_read_block(self):
        self.bufferobj._clearBuffer()
        self.bufferobj._source = io.BytesIO(b'\x01\x02\x03\x00')
        factorymock = rgslib.TestMsg()
        obj = rgslib.ReceiveLoop(factorymock, self.bufferobj)
        self.assertTrue(obj._read_block() == ord(b'\x01'))
        self.assertTrue(obj._read_block() == ord(b'\x02'))
        self.assertTrue(obj._read_block() == ord(b'\x03'))
        self.assertTrue(obj._read_block() is None)


    def test_Start(self):
        self.bufferobj._clearBuffer()
        self.bufferobj._source = io.BytesIO(b'\x00' + cobs.encode(self.testdata) + b'\x00')
        factorymock = rgslib.TestMsg()
        factorymock.construct = mock.MagicMock()
        obj = rgslib.ReceiveLoop(factorymock, self.bufferobj)
        self.assertTrue(obj._start_functionality() == self.testdata)




if __name__ == '__main__':
     unittest.main()
