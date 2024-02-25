import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from src import motor as motor_module
from src import led as led_module
import time
import math
from src import camera as camera_module

def process(img):
    """
    Turns image into contours
    """
    
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    edges = cv2.Canny(blur, 30, 100)
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    min_contour_area = 10 
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_contour_area]
    contour_image = cv2.drawContours(np.ones_like(edges), filtered_contours, -1, (0, 255, 0), -1)
    
    return filtered_contours, contour_image

def euclidean_distance(point1, point2):
    return np.linalg.norm(point1 - point2)

def makepath(contours):
    path = []
    for contour in contours:
        for point in contour:
            path.append(point[0])
    path = np.array(path)
    return path

def path_splicing(path):
    if len(path) <= 2000:
        return path

    # pathalgo = path
    while (len(path)) > 2000:
        path = path[::2]

    start_point = np.array([0, 0])
    remaining_points = set(map(tuple, path))

    pathalgo = [start_point]

    while remaining_points:
        nearest_point = min(remaining_points, key=lambda x: euclidean_distance(np.array(pathalgo[-1]), np.array(x)))
        pathalgo.append(np.array(nearest_point))
        remaining_points.remove(nearest_point)
    
    return pathalgo

def get_coords(path):
    x = []
    y = []

    for i in range(len(path)):
        x.append(path[i][0])
        y.append(path[i][1])
    return np.array([x, y])    

def calculate_angle(vector1, vector2):
    """
    Calculates angle (in degrees) between two vectors.

    Parameters:
        vector1 (tuple): Components of the first vector (dx1, dy1).
        vector2 (tuple): Components of the second vector (dx2, dy2).

    Returns:
        float: angle btw the two vectors in degrees.
    """
    v1_u = vector1 / np.linalg.norm(vector1)
    v2_u = vector2 / np.linalg.norm(vector2)

    angle_rad = np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))
    angle_deg = np.degrees(angle_rad)
    cross_product = np.cross(vector1, vector2)
    if cross_product < 0:
        angle_deg *= -1  # Negative angle for clockwise rotation

    return angle_deg

def make_equally_spaced(contour, spacing=1):
    new_path = [contour[0]]  # Start with the first point

    x, y = np.array(contour).T

    # print(contour, x, y)

    distances = [np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2) for i in range(len(x) - 1)]

    for i in range(1, len(contour) - 1):
        if (2 * spacing <= distances[i] <= 30 *  spacing):
            x_values = np.linspace(contour[i][0], contour[i+1][0], int(distances[i] / spacing))[:-1]
            y_values = np.linspace(contour[i][1], contour[i+1][1], int(distances[i] / spacing))[:-1]
            new_points = np.column_stack((x_values[1:], y_values[1:]))
            new_path.extend(new_points)
        elif distances[i] < spacing / 2:
            continue
        else:
            new_path.append(contour[i])

    new_path.append(contour[-1])

    return np.array(new_path)



def drive(use_equal, angles, scale):
    x, y = use_equal
    distances = [np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2) for i in range(len(x) - 1)]

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
        motor1.forward(0.925)
        motor2.forward(1)
        time.sleep(t)

    def rturn(t):
        motor1.forward(0.925)
        motor2.backward(1)
        time.sleep(t)

    def lturn(t):
        motor2.forward(1)
        motor1.backward(0.925)
        time.sleep(t)

    def pause():
        motor1.forward(0)
        motor2.forward(0)
        time.sleep(0.2)
        
    stop()
    stop()
    stop()

    led1.on()
    time.sleep(0.2)
    led1.off()
    led2.on()
    
    for i in range(0, len(angles) - 1):
        t = distances[i] / scale
        angle = angles[1]
        tangle = abs(angles[i]) * 0.325 / 90
        zoom(t)
        if (abs(angle) > 4):
            if (angle > 0):
                lturn(tangle)
            else:
                rturn(tangle)
            pause()
        
    led2.off()
    motor1.stop()
    motor2.stop()


if __name__ == '__main__':


    camera = camera_module.Camera({
        "show_preview": False
    })
    camera.capture()
    arr = np.array((camera.image_array))
    
    led2.on()
    time.sleep(cycle_time)
    led2.off()
    time.sleep(cycle_time)

    img = cv2.imread(sys.argv[1])
    contours, filtered = process(img)
    path = path_splicing(makepath(contours))
    contours = makepath(contours)
    equal_path = make_equally_spaced(path, spacing=25)
    use_equal = get_coords(equal_path)

    led1.on()
    time.sleep(cycle_time)
    led1.off()
    time.sleep(cycle_time)
        
    plt.figure(dpi=200)
    plt.plot(use_equal[0], use_equal[1], '-')
    plt.plot(use_equal[0], use_equal[1], 'ro', markersize=2)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.savefig('contour.png')
    plt.show()
    
    plt.figure(dpi=70)
    
    plt.imshow(filtered)
    plt.savefig('filtered.png')
    plt.show()
    
    x, y = use_equal
    
    distances = [np.sqrt((x[i+1] - x[i])**2 + (y[i+1] - y[i])**2) for i in range(len(x) - 1)]
    
    initial_angle = np.degrees(np.arctan(y[0] / x[0]))
    initial_vector = np.array([x[0],y[0]])
    
    vectors = [initial_vector]
    angles = [initial_angle]
    for i in range(1, len(x) - 1):
        vector1 = vectors[i - 1]
        vector2 = np.array([x[i+1] - x[i], y[i+1] - y[i]])
        angles.append(calculate_angle(vector1, vector2))
        vectors.append(vector2)
    
    drive(use_equal, angles, 300)