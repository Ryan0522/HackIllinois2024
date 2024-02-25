import cv2
import matplotlib.pyplot as plt
import numpy as np
import sys
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
    x = [0]
    y = [0]

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

def make_equally_spaced(contour, spacing=10):
    new_path = [contour[0]]  # Start with the first point

    distances = np.linalg.norm(np.roll(contour, 1, axis=0) - contour, axis=1)

    for i in range(1, len(contour) - 1):
        if (50 >= distances[i] >= 2 *  spacing):
            x_values = np.linspace(contour[i][0], contour[i+1][0], int(distances[i] / spacing))
            y_values = np.linspace(contour[i][1], contour[i+1][1], int(distances[i] / spacing))
            new_points = np.column_stack((x_values[1:], y_values[1:]))
            new_path.extend(new_points)
        elif distances[i] < spacing / 2:
            continue
        else:
            new_path.append(contour[i])

    new_path.append(contour[-1])

    return np.array(new_path)

if __name__ == '__main__':
    camera = camera_module.Camera({
        "show_preview": False
    })
    camera.capture()
    arr = np.array((camera.image_array))

    contours, filtered = process(arr)
    path = path_splicing(makepath(contours))
    contours = makepath(contours)
    equal_path = make_equally_spaced(path, spacing=3)
    use_equal = get_coords(equal_path)
    use_spliced = get_coords(path)
    use = get_coords(contours)
    
    plt.figure(dpi=90)
    plt.plot(use_equal[0], use_equal[1], 'b-')
    plt.plot(use_equal[0], use_equal[1], 'ro', markersize=2)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.savefig('equal_coords.png')
    plt.show()
    
    plt.figure(dpi=90)
    plt.plot(use_spliced[0], use_spliced[1], 'b-')
    plt.plot(use_spliced[0], use_spliced[1], 'ro', markersize=2)
    ax = plt.gca()
    ax.set_aspect('equal', adjustable='box')
    plt.savefig('coords.png')
    plt.show()
    
    plt.figure(dpi=70)
    plt.imshow(filtered)
    plt.savefig('filtered.png')
    plt.show()
