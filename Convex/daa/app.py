from flask import Flask, render_template, request, jsonify
import numpy as np
import random

app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    return render_template('jarv.html')

def gen_points(num, height, width, padding):
    points = []
    for i in range(num):
        points.append([random.randint(padding, height - padding), random.randint(padding, width - padding)])
    return points

def orientation_length(p, q, r):
    p = np.asarray(p, dtype='int32')
    q = np.asarray(q, dtype='int32')
    r = np.asarray(r, dtype='int32')

    vector_1 = q - p
    vector_2 = r - p

    length_1 = np.linalg.norm(vector_1)
    length_2 = np.linalg.norm(vector_2)

    cross_product = np.cross(vector_1, vector_2)

    return (cross_product, length_1, length_2)

def jarvis_march(points):
    # Find the leftmost point as the starting point of the convex hull
    leftmost_point = min(points, key=lambda x: x[0])
    hull = [leftmost_point]

    # Define a function to check if three points form a counterclockwise turn
    def ccw(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0]) > 0

    while True:
        endpoint = points[0]
        for point in points[1:]:
            # If this point is the leftmost or forms a counterclockwise turn, update the endpoint
            if endpoint == hull[-1] or ccw(hull[-1], endpoint, point):
                endpoint = point

        # If we've returned to the starting point, exit the loop
        if endpoint == hull[0]:
            break
        else:
            hull.append(endpoint)

    # Add the starting point again to close the convex hull
    hull.append(hull[0])

    return hull



@app.route('/convex_hull', methods=['POST'])
def convex_hull():
    data = request.json
    num_of_points = int(data.get('num_of_points', 30))
    height = int(data.get('height', 400))
    width = int(data.get('width', 400))
    padding = int(data.get('padding', 30))

    points = gen_points(num_of_points, height, width, padding)
    hull_list = jarvis_march(points)

    return jsonify({'hull_list': hull_list, 'points': points})

if __name__ == '__main__':
    app.run(debug=True)
