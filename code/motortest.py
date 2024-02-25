import numpy as np
from src import motor as motor_module
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

def right_turn():
    motor1.forward(0.5)
    motor2.backward(0.5)
    time.sleep(0.5)

def stop():
    motor1.forward(0)
    motor2.backward(0)
    time.sleep(1)

motor1.forward(0.5)
motor2.forward(0.5)
time.sleep(0.5)

stop()
right_turn()
stop()

motor1.forward(0.5)
motor2.forward(0.5)
time.sleep(1)

stop()
right_turn()
stop()

motor1.forward(0.5)
motor2.forward(0.5)
time.sleep(1)

stop()
right_turn()
stop()

motor1.forward(0.5)
motor2.forward(0.5)
time.sleep(1)

stop()
right_turn()
stop()

motor1.forward(0.5)
motor2.forward(0.5)
time.sleep(0.5)


motor1.stop()
motor2.stop()
