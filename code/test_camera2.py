import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
from src import camera as camera_module


def process(arr):
    """
    Turns arr into contours
    """
    
    gray = cv2.cvtColor(arr,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7,7), 0)
    ret, bw_img = cv2.threshold(blur, 127, 255, cv2.THRESH_BINARY)
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

if __name__ == '__main__':
    camera = camera_module.Camera({
        "show_preview": False
    })
    camera.capture()
    arr = np.array((camera.image_array))
    contours, processed = process(arr)
    path = makepath(contours)
    

    if len(path)>2000:
    
        pathcut = path[::3]

        start_point = np.array([0, 0])
        remaining_points = set(map(tuple, pathcut))

        pathalgo = [start_point]

        while remaining_points:
            nearest_point = min(remaining_points, key=lambda x: euclidean_distance(np.array(pathalgo[-1]), np.array(x)))
            pathalgo.append(np.array(nearest_point))
            remaining_points.remove(nearest_point)
        
        use = pathalgo
    else:
        use = path[::2]


    x = [0]
    y = [0]

    for i in range(len(use)):
        x.append(use[i][0])
        y.append(use[i][1])
    
    plt.figure(dpi=200)
    plt.plot(x,y)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.show()

    plt.figure(dpi=200)


    plt.imshow(processed)
    plt.show()
