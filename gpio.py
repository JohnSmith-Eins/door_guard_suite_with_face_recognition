import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.OUT, initial=GPIO.LOW)
GPIO.output(3,GPIO.HIGH)
time.sleep(5)
GPIO.output(3,GPIO.LOW)
GPIO.cleanup()