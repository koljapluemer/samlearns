import random
import math




def arc_path(cx, cy, p1x, p1y, p2x, p2y, radius, sweep_flag):
    # SVG arc path from p1 to p2 with center at (cx, cy) and given radius
    # Always use large-arc-flag=0 for triangle interior
    return f"M {p1x:.2f} {p1y:.2f} A {radius:.2f} {radius:.2f} 0 0 {sweep_flag} {p2x:.2f} {p2y:.2f}"

def get_sweep_flag(vx, vy, p1x, p1y, p2x, p2y):
    # Vectors from vertex to arc endpoints
    v1x, v1y = p1x - vx, p1y - vy
    v2x, v2y = p2x - vx, p2y - vy
    # Cross product (z-component)
    cross = v1x * v2y - v1y * v2x
    # If cross > 0, sweep_flag=1 (counterclockwise), else 0 (clockwise)
    return 1 if cross > 0 else 0

def angle_arc_points(vx, vy, v1x, v1y, v2x, v2y, radius):
    # Get two points at 'radius' along the directions from vertex to v1 and v2
    def unit(x, y):
        d = math.hypot(x, y)
        return (x/d, y/d) if d else (0, 0)
    u1x, u1y = unit(v1x-vx, v1y-vy)
    u2x, u2y = unit(v2x-vx, v2y-vy)
    p1x, p1y = vx + u1x*radius, vy + u1y*radius
    p2x, p2y = vx + u2x*radius, vy + u2y*radius
    return p1x, p1y, p2x, p2y

def canonical_triangle_points(side1, side2, angle):
    # Returns canonical triangle points (ax, ay), (bx, by), (cx, cy)
    ax, ay = 0, 0
    bx, by = side1, 0
    angle_rad = math.radians(angle)
    cx = side2 * math.cos(angle_rad)
    cy = side2 * math.sin(angle_rad)
    return (ax, ay), (bx, by), (cx, cy)

def rotate_and_scale_points(points, rotation, margin=30, viewbox_size=200):
    # Rotate around centroid, then scale and translate to fit in viewBox
    def rotate_point(x, y, angle_deg, cx=0, cy=0):
        angle_rad = math.radians(angle_deg)
        x0, y0 = x - cx, y - cy
        xr = x0 * math.cos(angle_rad) - y0 * math.sin(angle_rad)
        yr = x0 * math.sin(angle_rad) + y0 * math.cos(angle_rad)
        return xr + cx, yr + cy
    centroid_x = sum(x for x, y in points) / 3
    centroid_y = sum(y for x, y in points) / 3
    rotated_points = [rotate_point(x, y, rotation, centroid_x, centroid_y) for x, y in points]
    min_x = min(x for x, y in rotated_points)
    max_x = max(x for x, y in rotated_points)
    min_y = min(y for x, y in rotated_points)
    max_y = max(y for x, y in rotated_points)
    width = max_x - min_x
    height = max_y - min_y
    scale = min((viewbox_size - 2 * margin) / width, (viewbox_size - 2 * margin) / height)
    def transform_point(x, y):
        x = (x - min_x) * scale + margin
        y = (y - min_y) * scale + margin
        return x, y
    return [transform_point(*pt) for pt in rotated_points]

def generate_svg_triangle(side1, side2, side3, angle, rotation, theorem_type):
    # Step 1: Canonical triangle points (unrotated)
    ax, ay = 0, 0
    bx, by = side1, 0
    angle_rad = math.radians(angle)
    cx = side2 * math.cos(angle_rad)
    cy = side2 * math.sin(angle_rad)
    points = [(ax, ay), (bx, by), (cx, cy)]

    # Step 2: Rotate all points
    def rotate_point(x, y, angle_deg, cx=0, cy=0):
        angle_rad = math.radians(angle_deg)
        x0, y0 = x - cx, y - cy
        xr = x0 * math.cos(angle_rad) - y0 * math.sin(angle_rad)
        yr = x0 * math.sin(angle_rad) + y0 * math.cos(angle_rad)
        return xr + cx, yr + cy
    # Rotate around centroid for best visual centering
    centroid_x = sum(x for x, y in points) / 3
    centroid_y = sum(y for x, y in points) / 3
    rotated_points = [rotate_point(x, y, rotation, centroid_x, centroid_y) for x, y in points]

    # Step 3: Compute bounding box of rotated points
    min_x = min(x for x, y in rotated_points)
    max_x = max(x for x, y in rotated_points)
    min_y = min(y for x, y in rotated_points)
    max_y = max(y for x, y in rotated_points)
    width = max_x - min_x
    height = max_y - min_y

    # Step 4: Compute scale and translation to fit in viewBox
    margin = 30
    viewbox_size = 200
    scale = min((viewbox_size - 2 * margin) / width, (viewbox_size - 2 * margin) / height)
    # Center after scaling
    def transform_point(x, y):
        x = (x - min_x) * scale + margin
        y = (y - min_y) * scale + margin
        return x, y
    ax, ay = transform_point(*rotated_points[0])
    bx, by = transform_point(*rotated_points[1])
    cx, cy = transform_point(*rotated_points[2])

    # Step 5: SVG drawing logic (unchanged)
    side_color = "#4CAF50"
    angle_color = "#2196F3"
    a1 = a2 = a3 = ''
    radius = 28
    highlight_lines = []
    if theorem_type == 'ssw':
        if side1 >= side2:
            highlight_lines = [((ax, ay), (bx, by)), ((ax, ay), (cx, cy))]
            p1x, p1y, p2x, p2y = angle_arc_points(bx, by, ax, ay, cx, cy, radius)
            sweep_flag = get_sweep_flag(bx, by, p1x, p1y, p2x, p2y)
            a2 = f'<path d="{arc_path(bx, by, p1x, p1y, p2x, p2y, radius, sweep_flag)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
        else:
            highlight_lines = [((ax, ay), (bx, by)), ((bx, by), (cx, cy))]
            p1x, p1y, p2x, p2y = angle_arc_points(ax, ay, bx, by, cx, cy, radius)
            sweep_flag = get_sweep_flag(ax, ay, p1x, p1y, p2x, p2y)
            a1 = f'<path d="{arc_path(ax, ay, p1x, p1y, p2x, p2y, radius, sweep_flag)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    else:
        highlight_lines = [((ax, ay), (bx, by))]
        p1x, p1y, p2x, p2y = angle_arc_points(ax, ay, bx, by, cx, cy, radius)
        sweep_flag1 = get_sweep_flag(ax, ay, p1x, p1y, p2x, p2y)
        a1 = f'<path d="{arc_path(ax, ay, p1x, p1y, p2x, p2y, radius, sweep_flag1)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
        p1x, p1y, p2x, p2y = angle_arc_points(bx, by, ax, ay, cx, cy, radius)
        sweep_flag2 = get_sweep_flag(bx, by, p1x, p1y, p2x, p2y)
        a2 = f'<path d="{arc_path(bx, by, p1x, p1y, p2x, p2y, radius, sweep_flag2)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    polygon_points = f"{ax},{ay} {bx},{by} {cx},{cy}"
    svg = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            {a1}
            {a2}
            {a3}
            <polygon points="{polygon_points}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines])}
        </g>
    </svg>
    '''
    return svg 