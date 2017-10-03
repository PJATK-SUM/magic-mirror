# -*- coding: utf-8 -*-
import struct
import time
from pirc522 import RFID

def hex2str(bytes):
    return ''.join('{:02x}'.format(x) for x in bytes)

class Rfid():
    def __init__(self):
        self.isRunning = True
        self.rdr = RFID()  # initialize rfid reader

    def scan(self, callback):
        if __debug__:
            print("Starting")
        while self.isRunning:
            (error, data) = self.rdr.request()

            if not error and __debug__:
                print("\nDetected: " + format(data, "02x"))

                (error, uid) = self.rdr.anticoll()
                if not error:
                    callback(uid)
                    if __debug__:
                        print("Mifare: %d" % (hex2str(uid)))
            time.sleep(1)

    def close(self):
        self.isRunning = False
        self.rdr.cleanup()

    @staticmethod
    def mifareDataToInt(data):
        return struct.unpack("I", bytearray(data[:4]))[0]

    @staticmethod
    def reversedMifareDataToInt(data):
        return struct.unpack("I", bytearray(reversed(data[:4])))[0]
