import math
import matplotlib.pyplot as plt

from itertools import count, islice, zip_longest
from functools import reduce
from matplotlib.patches import Polygon

def draw_polygons(polygons, title="Polygons"):
    fig, ax = plt.subplots(figsize=(10, 6))

    for poly in polygons:
        patch = Polygon(
            poly,
            closed=True,
            fill=False,
            edgecolor='black',
            linewidth=1.5
        )
        ax.add_patch(patch)

    ax.set_aspect('equal')
    ax.grid(True)
    ax.set_xlim(-5, 25)
    ax.set_ylim(-10, 15)
    plt.title(title)
    plt.show()

def gen_rectangle():
    for i in count(0):
        x = i * 4
        yield (
            (x, 0),
            (x + 2, 0),
            (x + 2, 2),
            (x, 2)
        )

def gen_triangle():
    for i in count(0):
        x = i * 4
        yield (
            (x, 0),
            (x + 2, 0),
            (x + 1, 2)
        )

def gen_hexagon():
    for i in count(0):
        center = i * 4
        points = []

        for k in range(6):
            angle = math.pi / 3 * k
            px = center + math.cos(angle)
            py = math.sin(angle)
            points.append((px, py))

        yield tuple(points)

def translate_polygon(poly, dx, dy):
    result = []

    for x, y in poly:
        result.append((x + dx, y + dy))

    return tuple(result)

def rotate_polygon(poly, angle):
    result = []
    rad = math.radians(angle)

    for x, y in poly:
        nx = x * math.cos(rad) - y * math.sin(rad)
        ny = x * math.sin(rad) + y * math.cos(rad)
        result.append((nx, ny))

    return tuple(result)

def symmetry_x(poly):
    result = []

    for x, y in poly:
        result.append((x, -y))

    return tuple(result)

def symmetry_y(poly):
    result = []

    for x, y in poly:
        result.append((-x, y))

    return tuple(result)

def homothety(poly, k):
    result = []

    for x, y in poly:
        result.append((x * k, y * k))

    return tuple(result)

def polygon_area(poly):
    s = 0
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        s += x1 * y2 - x2 * y1

    return abs(s) / 2

def polygon_perimeter(poly):
    p = 0

    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        p += math.hypot(x2 - x1, y2 - y1)

    return p

def side_lengths(poly):
    result = []

    for i in range(len(poly)):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % len(poly)]
        side = math.hypot(x2 - x1, y2 - y1)
        result.append(side)

    return result

def flt_square(max_area):
    def check(poly):
        return polygon_area(poly) < max_area
    return check

def flt_short_side(max_len):
    def check(poly):
        sides = side_lengths(poly)
        return min(sides) < max_len
    return check

def flt_convex_polygon(poly):
    n = len(poly)
    sign = 0

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        x3, y3 = poly[(i + 2) % n]
        cross = (x2 - x1) * (y3 - y2) - (y2 - y1) * (x3 - x2)

        if cross != 0:
            current = 1 if cross > 0 else -1

            if sign == 0:
                sign = current
            elif sign != current:
                return False

    return True

def flt_angle_point(point):
    def check(poly):
        return point in poly
    return check

def point_inside(point, poly):
    x, y = point
    inside = False
    n = len(poly)

    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        cond = ((y1 > y) != (y2 > y))

        if cond:
            px = (x2 - x1) * (y - y1) / (y2 - y1) + x1

            if x < px:
                inside = not inside

    return inside

def flt_point_inside(point):
    def check(poly):
        return point_inside(point, poly)
    return check

def flt_polygon_angles_inside(other):
    def check(poly):
        for point in other:
            if point_inside(point, poly):
                return True
        return False
    return check

def agr_area(polygons):
    return reduce(lambda total, poly: total + polygon_area(poly), polygons, 0)

def agr_perimeter(polygons):
    return reduce(lambda total, poly: total + polygon_perimeter(poly), polygons, 0)

def agr_min_area(polygons):
    return reduce(lambda a, b: a if polygon_area(a) < polygon_area(b) else b, polygons)

def agr_origin_nearest(polygons):
    points = []

    for poly in polygons:
        for point in poly:
            points.append(point)

    return reduce(lambda a, b: a if math.hypot(a[0], a[1]) < math.hypot(b[0], b[1]) else b, points)

def agr_max_side(polygons):
    max_side = 0

    for poly in polygons:
        current = max(side_lengths(poly))

        if current > max_side:
            max_side = current

    return max_side

def zip_polygons(*iterators):
    result = []

    for polygons in zip_longest(*iterators, fillvalue=()):
        merged = []

        for poly in polygons:
            for point in poly:
                merged.append(point)

        result.append(tuple(merged))

    return result

def tr_translate(dx, dy):
    def decorator(func):
        def wrapper(*args, **kwargs):
            polygons = func(*args, **kwargs)
            result = []

            for poly in polygons:
                result.append(translate_polygon(poly, dx, dy))

            return result
        return wrapper
    return decorator

def tr_rotate(angle):
    def decorator(func):
        def wrapper(*args, **kwargs):
            polygons = func(*args, **kwargs)
            result = []

            for poly in polygons:
                result.append(rotate_polygon(poly, angle))

            return result
        return wrapper
    return decorator

def tr_symmetry(axis='x'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            polygons = func(*args, **kwargs)
            result = []

            for poly in polygons:
                if axis == 'x':
                    result.append(symmetry_x(poly))
                else:
                    result.append(symmetry_y(poly))

            return result
        return wrapper
    return decorator

def tr_homothety(k):
    def decorator(func):
        def wrapper(*args, **kwargs):
            polygons = func(*args, **kwargs)
            result = []

            for poly in polygons:
                result.append(homothety(poly, k))

            return result
        return wrapper
    return decorator

rectangles = list(islice(gen_rectangle(), 5))
triangles = list(islice(gen_triangle(), 5))
hexagons = list(islice(gen_hexagon(), 5))

draw_polygons(rectangles, "Rectangles")
draw_polygons(triangles, "Triangles")
draw_polygons(hexagons, "Hexagons")

translated = []

for rect in rectangles:
    translated.append(translate_polygon(rect, 0, 5))

draw_polygons(translated, "Translated")

rotated = []

for triangle in triangles:
    rotated.append(rotate_polygon(triangle, 30))

draw_polygons(rotated, "Rotated")

symmetric = []

for triangle in triangles:
    symmetric.append(symmetry_x(triangle))

draw_polygons(symmetric, "Symmetry")

scaled = []
k = 1

for rect in rectangles:
    scaled.append(homothety(rect, k))
    k += 0.5

draw_polygons(scaled, "Scaled")

filtered_area = list(filter(flt_square(5), rectangles))
draw_polygons(filtered_area, "Area filter")

filtered_side = list(filter(flt_short_side(2.5), triangles))
draw_polygons(filtered_side, "Short side filter")

convex_only = list(filter(flt_convex_polygon, rectangles))
draw_polygons(convex_only, "Convex polygons")

point_filtered = list(filter(flt_point_inside((1, 1)), rectangles))
draw_polygons(point_filtered, "Point inside")

print("Total area:", agr_area(rectangles))
print("Total perimeter:", agr_perimeter(rectangles))
print("Min area polygon:", agr_min_area(rectangles))
print("Nearest point:", agr_origin_nearest(rectangles))
print("Max side:", agr_max_side(rectangles))

zipped = zip_polygons(rectangles[:3], triangles[:3])
draw_polygons(zipped, "Zip polygons")
