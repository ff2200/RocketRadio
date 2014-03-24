
import unittest
import os
import io

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
        self.assertTrue(next(self.obj.getChar()) == b'\x01')
        self.assertFalse(next(self.obj.getChar()) == b'\x03')

    def test_pushBack(self):
        self.obj.pushBack(b'\x00')
        self.assertTrue(next(self.obj.getChar()) == b'\x00')

    def test_getChar_empty(self):
        self.fd.seek(0, io.SEEK_END)
        self.assertTrue(next(self.obj.getChar()) == b'')

    def test_fdClosed(self):
        fd = io.StringIO()
        obj = rgslib.MsgBuffer(fd)
        fd.close()
        self.assertRaises(ValueError,next, obj.getChar())


if __name__ == '__main__':
    unittest.main()
    '''
    fd = io.BytesIO(b'\x01\x02\x03')
    obj = rgslib.MsgBuffer(fd)
    print(next(obj.getChar()))
    '''
