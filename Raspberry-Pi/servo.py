import RPi.GPIO as GPIO
import time

pin =7
GPIO.setmode(GPIO.BOARD)
GPIO.setup(pin, GPIO.OUT)
p= GPIO.PWM(pin, 50)
p.start(7)
cnt = 0

def HardTurnright():
    return p.ChangeDutyCycle(2.8)

def Turnright():
    return p.ChangeDutyCycle(3.5)

def Go():
    return p.ChangeDutyCycle(7.5)

def Turnleft():
    return p.ChangeDutyCycle(9.8)

def HardTurnleft():
    return p.ChangeDutyCycle(12.5)

if __name__ == '__main__':
    try:
        while True:
            p.ChangeDutyCycle(12.5)
            time.sleep(10)
            
    except KeybordInterrupt:
         p.stop()
         GPIO.cleanup()
