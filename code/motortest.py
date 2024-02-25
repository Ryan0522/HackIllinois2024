import numpy as np
from src import motor as motor_module
from src import led as led_module
import time

if __name__ == '__main__':

    motor1 = motor_module.Motor({
        "pins": {
            "speed": 13,
            "control1": 5,
            "control2": 6
        }
    })

    motor2 = motor_module.Motor({
        "pins": {
            "speed": 12,
            "control1": 7,
            "control2": 8
        }
    })
    led1 = led_module.LED({
        "pin": 20
    })

    led2 = led_module.LED({
        "pin": 21
    })

def right_turn():
    motor1.forward(1)
    motor2.backward(1)
    time.sleep(0.355)

def right_full_turn():
    motor1.forward(1)
    motor2.backward(1)
    time.sleep(0.71)

def right_big_full_turn():
    motor1.forward(1)
    motor2.forward(0)
    time.sleep(1.25)

def right_full_circle():
    motor1.forward(1)
    motor2.backward(1)
    time.sleep(1.42)

def stop():
    motor1.forward(0)
    motor2.backward(0)
    led1.on()
    time.sleep(0.5)
    motor1.forward(0)
    motor2.backward(0)
    led1.off()
    led2.on()
    time.sleep(0.5)
    led2.off()

def zoom(t):
    motor1.forward(1)
    motor2.forward(1)
    time.sleep(t)

right_full_circle()

stop()
zoom(1.2)

stop()
right_big_full_turn()
stop()

zoom(1.3)

stop()
right_full_circle()
right_full_turn()
stop()

# right_turn()
# stop()

# zoom(0.5)

# stop()
# right_turn()
# stop()

# zoom(0.5)

# zoom(1)

motor1.stop()
motor2.stop()
