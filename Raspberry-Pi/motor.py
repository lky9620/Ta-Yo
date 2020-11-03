import RPi.GPIO as GPIO
import time
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

DCpin1 = 32
DCpin2 = 33

GPIO.setup(DCpin1, GPIO.OUT)
GPIO.setup(DCpin2, GPIO.OUT)

pwm1 = GPIO.PWM(DCpin1, 100)
pwm2 = GPIO.PWM(DCpin2, 100)
pwm1.start(0)
pwm2.start(0)

def Forward(speed):
    pwm2.ChangeDutyCycle(speed)

def Backward(speed):
    pwm1.ChangeDutyCycle(speed)

def Stop():
    pwm2.ChangeDutyCycle(0)
    pwm1.ChangeDutyCycle(0)

if __name__ == '__main__':
    try:
        while True:
            Backward(12)
 
 
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        pwm1.stop()
        pwm2.stop()
        GPIO.cleanup()
        sys.exit()
     
