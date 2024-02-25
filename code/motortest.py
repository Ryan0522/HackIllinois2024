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
    motor1.forward(0.925)
    motor2.backward(1)
    time.sleep(0.325) # was 0.355

def left_turn():
    motor2.forward(1)
    motor1.backward(0.925)
    time.sleep(0.325) #original on paper

def right_full_turn():
    motor1.forward(0.925)
    motor2.backward(1)
    time.sleep(0.65) #coefficient on wood

def right_big_full_turn():
    motor1.forward(0.925)
    motor2.forward(0)
    time.sleep(1.23)

def left_big_full_turn():
    motor2.forward(1)
    motor1.forward(0)
    time.sleep(1.23)

def right_full_circle():
    motor1.forward(0.925)
    motor2.backward(1)
    time.sleep(1.5)

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

def pause():
    motor1.forward(0)
    motor2.forward(0)
    time.sleep(0.3)

def zoom(t):
    motor1.forward(0.925)
    motor2.forward(1)
    time.sleep(t)

stop()
stop()
stop()

zoom(1.4)
stop()
right_turn()
zoom(0.15)
left_big_full_turn()
zoom(0.3)
left_big_full_turn()
zoom(0.3)
left_big_full_turn()
zoom(0.15)
right_turn()
zoom(0.3)

motor1.forward(1)
motor2.forward(0.35)
time.sleep(1.7)

zoom(0.7)
left_big_full_turn()
zoom(0.35)
left_big_full_turn()
zoom(0.85)

right_turn()
zoom(0.6)
right_turn()
zoom(0.4)
left_turn()
zoom(0.5)
left_turn()
zoom(0.4)
right_turn()
zoom(0.6)
# stop()
# stop()
# stop()

# for _ in range(1):
#     zoom(1.4)
#     right_full_turn()
#     pause()
#     zoom(1.4)
#     right_full_turn()
#     pause()

motor1.stop()
motor2.stop()
