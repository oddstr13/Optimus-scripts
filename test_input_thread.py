#!/usr/bin/env python

import time

import threading
import queue
from decimal import Decimal as dec

import inputs
import serial

XY_SENS = 0.2
Z_SENS = 0.01

XY_DIV = 2**16/2
Z_DIV = 255

class State:
    def __init__(self, x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z
    
    def __str__(self):
        return "{},{},{}".format(self.x, self.y, self.z)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z
    

left = State()
right = State()

eventq = queue.Queue()
exitq = queue.Queue()

BTN_B = False
BTN_A = False
BTN_X = False
BTN_Y = False
BTN_START = False

class Eventgrabber(threading.Thread):
    def run(self):
        while True:
            try:
                exitq.put(exitq.get_nowait())
                return
            except queue.Empty:
                pass
            try:
                for event in inputs.get_gamepad():
                    #print("thread",event)
                    eventq.put(event)
            except inputs.UnpluggedError:
                print("No controller")
                time.sleep(5)

def inputhandler():
    global BTN_A, BTN_B, BTN_X, BTN_Y, BTN_START
    while True:
        try:
            event = eventq.get_nowait()
        except queue.Empty:
            break

        #print(event)
        #print(dir(event))
        if event.ev_type == 'Sync':
            #if abs(left.x) >= XY_SENS or abs(left.y) >= XY_SENS or abs(left.z) >= Z_SENS:
            #    print("Left: {x: .3f},{y: .3f},{z: .2f}".format(x=left.x, y=left.y, z=left.z))
            #print("Right: {x:.3f},{y:.3f},{z:.2f}".format(x=right.x, y=right.y, z=right.z))
            continue
        elif event.ev_type == 'Absolute':
            p=True
            if event.code == 'ABS_X':
                left.x = event.state/XY_DIV
            elif event.code == 'ABS_Y':
                left.y = event.state/XY_DIV
            elif event.code == 'ABS_Z':
                left.z = event.state/Z_DIV
            elif event.code == 'ABS_RX':
                right.x = event.state/XY_DIV
            elif event.code == 'ABS_RY':
                right.y = event.state/XY_DIV
            elif event.code == 'ABS_RZ':
                right.z = event.state/Z_DIV
            else:
                p=False
            if p:
                continue
        elif event.ev_type == "Key":
            if event.code == "BTN_EAST":
                BTN_B = not not event.state
                continue
            elif event.code == "BTN_SOUTH":
                BTN_A = not not event.state
                continue
            elif event.code == "BTN_NORTH":
                BTN_Y = not not event.state
                continue
            elif event.code == "BTN_WEST":
                BTN_X = not not event.state
                continue
            elif event.code == "BTN_SELECT":
                BTN_START = not not event.state
                continue
        print(event.ev_type, event.code, event.state)


def posdecode(s):
    res = State()
    for i in s.split()[1:]:
        k,v = i.split(':', 1)
        if k == 'X':
            res.x = dec(v[:-2])
        elif k == 'Y':
            res.y = dec(v[:-2])
        elif k == 'Z':
            res.z = dec(v[:-2])
    # ok LMP: X:144.0770 Y:54.3770 Z:0.0000
    return res

def main():
    gt = Eventgrabber()
    gt.start()
    with serial.Serial('COM4', baudrate=115200, timeout=1) as ser:
        def cmd(c):
            c = c.encode('utf-8') if type(c) == str else c
            print("<<- {}".format(c.decode("utf-8")))
            ser.write(c + b"\n")
            ser.flush()
            res = ser.readline().decode("utf-8")
            print("->> {}".format(res.strip()))
            return res

        def gcodeflush():
            res = cmd("M400").strip()
            while res != "ok":
                res = ser.readline().decode("utf-8").strip()
            print("->> {}".format(res))
            

        # Use relative coordinates
        cmd("G91")

        while True:
            #time.sleep(5)

            inputhandler()

            if BTN_START:
                cmd("G28 $H")
                gcodeflush()
            else:
                moved = False

                speed = 2000 if BTN_B else 100
                MUL = 4 if BTN_B else 1
                POW = 2 if BTN_B else 1
                
                if left.z or right.z:
                    z = (left.z**POW) - (right.z**POW)
                    if z:
                        cmd("G0 Z{z:.3f} F{speed}".format(speed=speed, z=z))
                        moved = True

                x = abs(left.x) - XY_SENS
                x = (x*MUL)**POW
                if left.x < 0:
                    x *= -1
                
                y = abs(left.y) - XY_SENS
                y = (y*MUL)**POW
                if left.y < 0:
                    y *= -1
                
                if abs(left.x) > XY_SENS and abs(left.y) > XY_SENS:
                    cmd("G0 X{x:.3f} Y{y:.3f} F{speed}".format(speed=speed, x=x, y=y))
                    moved = True
                elif abs(left.x) >= XY_SENS:
                    cmd("G0 X{x:.3f} F{speed}".format(speed=speed, x=x))
                    moved = True
                elif abs(left.y) >= XY_SENS:
                    cmd("G0 Y{y:.3f} F{speed}".format(speed=speed, y=y))
                    moved = True
                
                if moved:
                    gcodeflush()

            while ser.in_waiting:
                print("?>> {}".format(ser.readline().decode("utf-8").strip()))


if __name__ == "__main__":
    try:
        main()
    except:
        print("Exiting...")
        exitq.put(True)
        raise
    finally:
        exitq.put(True)
