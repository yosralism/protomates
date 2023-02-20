#!/usr/bin/python3
import io
import pynmea2
import serial
import sys


ser = serial.Serial('/dev/ttyACM0', 57600, timeout=5.0)
#sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))

while 1:
    try:
        line = ser.readline()
        if sys.version_info[0] == 3:
        	line = line.decode("utf-8","ignore")
        	msg = pynmea2.parse(line)
        	print(repr(msg))
    except serial.SerialException as e:
        print('Device error: {}'.format(e))
        break
    except pynmea2.ParseError as e:
        print('Parse error: {}'.format(e))
        continue
