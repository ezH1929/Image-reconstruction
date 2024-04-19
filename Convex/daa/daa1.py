"""
@date: April 5, 2024
@brief: Implementation of the Jarvis March algorithm for computing the convex hull of a set of points.


# Time Complexity: O(n^2)
#   - The time complexity of the Jarvis March algorithm is O(n^2), where n is the number of input points.
#     This is because for each point, we iterate through all other points to find the next point on the convex hull.
#
![](time.png)
# Space Complexity: O(h)
#   - The space complexity of the Jarvis March algorithm is O(h), where h is the number of points on the convex hull.
#     In the worst case, the convex hull could contain all input points, leading to O(n) space complexity.
#
# Note: These complexities are based on the algorithm's characteristics and may vary depending on the implementation.
"""

import argparse
import numpy as np 
import random
import cv2

# Define default values for parameters
defaults = {    
    'num_of_points': 30,
    'visualize': False,
    'save': False,
    'height': 200,
    'width': 200,
    'padding': 30
}

# Parse command-line arguments
parser = argparse.ArgumentParser()
parser.add_argument('--num_of_points', default=defaults['num_of_points'], type=int, help="Define the number of points to be generated.")
parser.add_argument('--visualize', action='store_true', default=defaults['visualize'], help="If you want to visualize the working of the algorithm")
parser.add_argument('--save', action='store_true', default=defaults['save'], help='If you want to save the end result as an image.')
parser.add_argument('--height', default=defaults['height'], type=int, help='Define the image height')
parser.add_argument('--width', default=defaults['width'], type=int, help='Define the image width.')
parser.add_argument('--padding', default=defaults['padding'], type=int, help='Define the padding size.')

args = parser.parse_args()

# Check argument values
assert args.num_of_points > 3, "Number of points must be more than 3 !"
assert args.height >= 20, "Image height must be at least 20!"
assert args.width >= 20, "Image width must be at least 20!"
assert args.padding*2 <= args.width or args.padding*2 <= args.height, "Padding size cannot exceed half of the width nor height of the image!"

# Extract argument values
image_height = args.height
image_width  = args.width
padding = args.padding

image = np.zeros((image_height, image_width, 3))




def draw_points(im, points):
    '''
    Draw the generated points on the image.
    @param im: Image to draw on.
    @param points: List of points to draw.
    @return: Image with points drawn.
    '''

    # Make a copy so the original image is not altered
    img = im.copy()

    for i in range(len(points)):
        # Access by row, column
        img[points[i][1], points[i][0]] = 255

    return img


def orientation_length(p,q,r):
    '''
    Determine the orientation of the vectors and the length of the vectors.
    @param p: First point.
    @param q: Second point.
    @param r: Third point.
    @return: Tuple containing cross product, length of the first vector, and length of the second vector.
    '''

    # Convert lists into numpy arrays
    p = np.asarray(p, dtype='int32')
    q = np.asarray(q, dtype='int32')
    r = np.asarray(r, dtype='int32')

    vector_1 = q - p
    vector_2 = r - p

    # Calculate the length of the vectors
    length_1 = np.linalg.norm(vector_1)
    length_2 = np.linalg.norm(vector_2)

    cross_product = np.cross(vector_1,vector_2)

    return (cross_product, length_1, length_2)


def draw_temp_line(im, points1, points2, red_colour=255):
    '''
    Draw the temporary lines during the visualization process.
    @param im: Image to draw on.
    @param points1: Starting point of the line.
    @param points2: Ending point of the line.
    @param red_colour: Color of the line.
    @return: Image with temporary line drawn.
    '''

    img = im.copy()

    # Plot the lines
    cv2.line(img, (points1[0], points1[1]),
                  (points2[0], points2[1]), (255,255,red_colour), 1)

    return img


def jarvis_march(points, animation=False):
    '''
    Generate the convex polygon using Jarvis March algorithm.
    @param points: List of points.
    @param animation: Whether to visualize the algorithm.
    @return: List of points representing the convex hull.
    '''

    # Get the leftmost point based on the x values
    leftmost_point = min(points, key = lambda x:x[0])

    # Index of that leftmost point
    leftmost_point_index = points.index(leftmost_point)

    p = leftmost_point_index

    hull_list = []

    # Append the leftmost point as it is surely one of the points in the convex polygon
    hull_list.append(points[p])

    num_of_points = len(points)

    # Plot the points on the image if animation is enabled
    if animation:
        img = draw_points(image, points)

    while True:

        # Initialize a second point to start the comparing process
        q = (p + 1) % num_of_points

        # Iterate through all points
        for r in range(num_of_points):

            # Skip the current loop if it's the leftmost point
            if r == p:
                continue

            # Draw the temporary lines during the process if animation is enabled
            if animation:
                img_temp = draw_temp_line(img, points[p], points[q])
                img_temp = draw_temp_line(img_temp, points[p], points[r], 0)
                cv2.imshow('img_temp', img_temp)
                cv2.waitKey(50)

            orientation, length_1, length_2 = orientation_length(points[p], points[q], points[r])

            # If orientation is more than 0, that means it is an anticlockwise rotation
            # If orientation is 0, the vectors are colinear, hence we choose the largest length vector
            if orientation > 0 or (orientation == 0 and length_2 > length_1):
                q = r

        if animation:
            img = draw_temp_line(img, points[p], points[q])

        # Declare a new p
        p = q

        # Break the loop if the starting point has been reached
        if p == leftmost_point_index:
            break

        hull_list.append(points[q])

    return hull_list


def gen_points(num):
    '''
    Randomly generate num number of points.
    @param num: Number of points to generate.
    @return: List of generated points.
    '''

    points = []

    for i in range(num):
        # Generate within the range of the padded values
        points.append([random.randint(padding,image_height-padding), random.randint(padding,image_width-padding)])

    return points


def draw_lines(im, points):
    '''
    Draw the lines on the image as per the hull_list generated from the algorithm.
    @param im: Image to draw on.
    @param points: List of points representing the convex hull.
    @return: Image with lines drawn.
    '''

    img = im.copy()

    for i in range(len(points)):

        # The next_index cannot be more than the number of points
        next_index = (i+1)%len(points)

        cv2.line(img, (points[i][0], points[i][1]),
                     (points[next_index][0], points[next_index][1]),
                     (255,255,255),1)

    return img

