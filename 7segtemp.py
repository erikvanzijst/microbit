import time
from microbit import *


uart.init(115200, bits=8, parity=None, stop=1)
uart.write('Starting...\r\n')


def write_segment(seg_val, msb):
    v = int(seg_val / 10 if msb else seg_val % 10)
    if msb and v == 0:
        v = 10  # don't show leading zero
    (pin0 if msb else pin1).write_digital(0)
    pin13.write_digital(bool(v & 0x1))
    pin14.write_digital(bool(v & 0x2))
    pin15.write_digital(bool(v & 0x4))
    pin16.write_digital(bool(v & 0x8))
    (pin1 if msb else pin0).write_digital(1)

def main():
    calibration = -1  # calibrate down by 1 degree by default
    try:
        with open('calibration', 'r') as f:
            calibration = int(f.read())  # read from EEPROM
    except Exception as e:
        uart.write(str(e))
        uart.write('\r\n')
    
    msb = False  # the left segment (True) or the right segment (False)
    last_tick = time.ticks_ms()
    interval = 1
    last_sample = time.ticks_ms()
    sample_interval = 500
    temp = temperature()
    uart.write(str(temp) + ' degrees (' + str(calibration) + ' calibration)\r\n')

    while True:
        now = time.ticks_ms()
    
        if time.ticks_diff(now, last_tick) > interval:
            msb = not msb
            write_segment(max(0, temp + calibration), msb)
            last_tick = now

        if time.ticks_diff(now, last_sample) > sample_interval:
            temp = temperature()
            last_sample = now

        a = button_a.was_pressed()
        b = button_b.was_pressed()
    
        if a or b:
            calibration += 1 if b else -1
            calibration = min(10, max(-10, calibration))  # clamp
            with open('calibration', 'w') as f:
                f.write(str(calibration))  # write to EEPROM
            uart.write('Calibration: ' + str(calibration) + '\r\n')

import os
for fn in os.listdir():
    uart.write(fn)
    uart.write('\r\n')

main()
