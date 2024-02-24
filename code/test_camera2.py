from src import camera as camera_module
import numpy as np
import matplotlib.pyplot as plt
import time

if __name__ == '__main__':

    camera = camera_module.Camera({
        "show_preview": False
    })

    camera.capture()
    arr = np.array(camera.image_array)
    plt.plot(arr[:,0], arr[:,1])
    plt.show()