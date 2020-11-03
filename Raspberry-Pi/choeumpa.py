import RPi.GPIO as GPIO
import time
import motor


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

GPIO_TRIGGER = 11
GPIO_ECHO = 13

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)

def distance():
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.1)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2

    return distance

if __name__ == '__main__':
    try:
        while True:

            dist = distance()
    #             
            if dist > 7:
                print ("Measured Distance = %.1f cm" % dist)
                print("Foward")
                motor.Forward(12)

            elif dist <= 7:
                print ("Measured Distance = %.1f cm" % dist)
                print("stop")
                motor.Stop()



        # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

    
        

