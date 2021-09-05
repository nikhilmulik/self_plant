# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BCM)  # Broadcom pin-numbering scheme


def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"


def get_status(pin=8):
    GPIO.setup(pin, GPIO.IN)
    return GPIO.input(pin)


def init_output(pin):
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)


def auto_water(delay=5, pump_pin=7, water_sensor_pin=8):
    consecutive_water_count = 0
    init_output(pump_pin)
    print("Here we go! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 10:
            time.sleep(delay)
            wet = get_status(pin=water_sensor_pin) == 0
            if not wet:
                if consecutive_water_count < 5:
                    pump_on(pump_pin, 1)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt:  # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup()  # cleanup all GPI


def pump_on(delay=2, pump_number=2):
    print(">>>>", pump_number)
    pump_pin = config_pump(pump_number)
    print('>>>>', pump_pin, '  >>', delay)
    init_output(pump_pin)
    f = open("last_watered.txt", "w")
    f.write("{}".format(datetime.datetime.now()))
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(delay)
    GPIO.output(pump_pin, GPIO.HIGH)


def config_pump(pump_number):
    if pump_number == 1:
        return 17
    if pump_number == 2:
        return 22
