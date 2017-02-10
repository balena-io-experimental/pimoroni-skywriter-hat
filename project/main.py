#!/usr/bin/env python
# main.py

import sys, os, time, signal

try:
    import skywriter
except ImportError:
    print "Error: importing skywriter"
except IOError:
    print "I/O Error: maybe you need to modprobe i2c-dev?"

def signal_term_handler(signal, frame):
    # handle the sigterm signal and write that to a persisted file in /data
    with open("/data/signals.log","a+") as f:
        f.write('got SIGTERM')
    print 'got SIGTERM'
    sys.exit(0)

def signal_int_handler(signal, frame):
    with open("/data/signals.log","a+") as f:
        f.write('got SIGINT')
    print 'got SIGINT'
    sys.exit(0)

def signal_kill_handler(signal, frame):
    with open("/data/signals.log","a+") as f:
        f.write('got SIGKILL')
    print 'got SIGKILL'
    sys.exit(0)

# Register our signal handlers to clean up gracefully
signal.signal(signal.SIGTERM, signal_term_handler)
signal.signal(signal.SIGINT, signal_int_handler)
signal.signal(signal.SIGHUP, signal_kill_handler)

# Print all the available RESIN_* variables in the environment.
print "RESIN envvars\n"
for key in os.environ.keys():
    if 'RESIN' in key:
        print key,os.environ[key]

some_value = 5000

@skywriter.move()
def move(x, y, z):
    print( x, y, z )

@skywriter.flick()
def flick(start,finish):
    print('Got a flick!', start, finish)

@skywriter.airwheel()
def spinny(delta):
    global some_value
    some_value += delta
    if some_value < 0:
        some_value = 0
    if some_value > 10000:
        some_value = 10000
    print('Airwheel:', some_value/100)

@skywriter.double_tap()
def doubletap(position):
    print('Double tap!', position)

@skywriter.tap()
def tap(position):
    print('Tap!', position)

@skywriter.touch()
def touch(position):
    print('Touch!', position)

signal.pause()
