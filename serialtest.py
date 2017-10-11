import serial
import time


with serial.Serial('COM3', baudrate=115200, timeout=0.2) as ser:
    while ser.in_waiting: ser.read(ser.in_waiting)

    def cmd(c):
        c = c.encode('utf-8') if type(c) == str else c
        ser.write(c + b"\n")
        ser.flush()

    print(cmd("G91"))

    while True:
        time.sleep(1)
        print(cmd("G0 X100"))
        print(ser.in_waiting)
        while ser.in_waiting:
            print("->> {}".format(ser.readline()))