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
    
motor1.forward(1)
motor2.forward(1)
time.sleep(0.25)
motor1.forward(1)
motor2.forward(0.25)
time.sleep(0.25)
motor1.forward(2)
motor2.forward(2)
time.sleep(0.25)

motor1.stop()
motor2.stop()
