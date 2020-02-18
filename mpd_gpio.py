#!/usr/bin/python3

#import sys
import os
import time
import RPi.GPIO as GPIO
import threading

class ButtonHandler(threading.Thread):
    def __init__(self, pin, func, edge='both', bouncetime=200):
        super().__init__(daemon=True)

        self.edge = edge
        self.func = func
        self.pin = pin
        self.bouncetime = float(bouncetime)/1000

        self.lastpinval = GPIO.input(self.pin)
        self.lock = threading.Lock()

    def __call__(self, *args):
        if not self.lock.acquire(blocking=False):
            return

        t = threading.Timer(self.bouncetime, self.read, args=args)
        t.start()

    def read(self, *args):
        pinval = GPIO.input(self.pin)

        if (
                ((pinval == 0 and self.lastpinval == 1) and
                 (self.edge in ['falling', 'both'])) or
                ((pinval == 1 and self.lastpinval == 0) and
                 (self.edge in ['rising', 'both']))
        ):
            self.func(*args)

        self.lastpinval = pinval
        self.lock.release()

channelNo = 1

# Callback called when switch is pressed.
#def switch_callback(channel):
def switch_callback(channel):
    global channelNo
    print('Switch pressed, exiting.')
    if channelNo > 5:
        print('Switch pressed, stop, channel=>'+str(channelNo))
        os.system('mpc stop')
        channelNo = 1
    else:
        print('Switch pressed, play, channel=>'+str(channelNo))
        os.system('mpc play '+str(channelNo))
        channelNo = channelNo + 1

    time.sleep(0.5)
    #GPIO.cleanup()
    #sys.exit(0)

switch = 16 # GPIO 23

GPIO.setmode(GPIO.BOARD)
#GPIO.setup(led1, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

#GPIO.add_event_detect(switch, GPIO.FALLING, callback=switch_callback)

cb = ButtonHandler(switch, switch_callback, edge='rising', bouncetime=100)
cb.start()
GPIO.add_event_detect(switch, GPIO.RISING, callback=cb)

while True:
    time.sleep(0.05)