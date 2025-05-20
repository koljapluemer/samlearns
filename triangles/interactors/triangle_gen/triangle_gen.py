import random
import math

def generate_ssw_triangle():
    # Generate a random triangle with two sides and the angle opposite the longer side
    # Returns data for two congruent triangles with different rotations
    
    # Generate random side lengths (ensuring triangle inequality)
    side1 = random.uniform(50, 100)
    side2 = random.uniform(50, 100)
    while abs(side1 - side2) < 10:  # Ensure sides are noticeably different
        side2 = random.uniform(50, 100)
    
    # Generate random angle (in degrees)
    angle = random.uniform(30, 150)
    
    # Calculate third side using law of cosines
    angle_rad = math.radians(angle)
    side3 = math.sqrt(side1**2 + side2**2 - 2*side1*side2*math.cos(angle_rad))
    
    # Generate SVG data for two triangles
    # First triangle
    svg1 = generate_svg_triangle(side1, side2, side3, angle, 0, 'ssw')
    # Second triangle (rotated)
    rotation = random.uniform(30, 330)
    svg2 = generate_svg_triangle(side1, side2, side3, angle, rotation, 'ssw')
    
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'ssw',
        'highlighted_elements': {
            'sides': [side1, side2],  # The two sides that are the same
            'angle': angle  # The angle opposite the longer side
        }
    }

def generate_wsw_triangle():
    # Generate a random triangle with one side and its two adjacent angles
    # Returns data for two congruent triangles with different rotations
    
    # Generate random side length
    side = random.uniform(50, 100)
    
    # Generate random angles (ensuring they sum to less than 180)
    angle1 = random.uniform(30, 60)
    angle2 = random.uniform(30, 60)
    while angle1 + angle2 >= 150:  # Leave room for third angle
        angle1 = random.uniform(30, 60)
        angle2 = random.uniform(30, 60)
    
    # Calculate third angle
    angle3 = 180 - angle1 - angle2
    
    # Calculate other sides using law of sines
    angle1_rad = math.radians(angle1)
    angle2_rad = math.radians(angle2)
    angle3_rad = math.radians(angle3)
    side1 = side * math.sin(angle1_rad) / math.sin(angle3_rad)
    side2 = side * math.sin(angle2_rad) / math.sin(angle3_rad)
    
    # Generate SVG data for two triangles
    # First triangle
    svg1 = generate_svg_triangle(side, side1, side2, angle1, 0, 'wsw')
    # Second triangle (rotated)
    rotation = random.uniform(30, 330)
    svg2 = generate_svg_triangle(side, side1, side2, angle1, rotation, 'wsw')
    
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'wsw',
        'highlighted_elements': {
            'side': side,  # The side that is the same
            'angles': [angle1, angle2]  # The two angles adjacent to the side
        }
    }

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

def generate_svg_triangle(side1, side2, side3, angle, rotation, theorem_type):
    ax, ay = 0, 0
    bx, by = side1, 0
    angle_rad = math.radians(angle)
    cx = side2 * math.cos(angle_rad)
    cy = side2 * math.sin(angle_rad)
    points = [(ax, ay), (bx, by), (cx, cy)]
    def rotate_point(x, y, angle_deg, cx=0, cy=0):
        angle_rad = math.radians(angle_deg)
        x0, y0 = x - cx, y - cy
        xr = x0 * math.cos(angle_rad) - y0 * math.sin(angle_rad)
        yr = x0 * math.sin(angle_rad) + y0 * math.cos(angle_rad)
        return xr + cx, yr + cy
    svg_center = (100, 100)
    margin = 30
    min_x = min(x for x, y in points)
    max_x = max(x for x, y in points)
    min_y = min(y for x, y in points)
    max_y = max(y for x, y in points)
    width = max_x - min_x
    height = max_y - min_y
    scale = min((200 - 2 * margin) / width, (200 - 2 * margin) / height)
    center_x = (min_x + max_x) / 2
    center_y = (min_y + max_y) / 2
    def transform_point(x, y):
        x = (x - center_x) * scale + 100
        y = (y - center_y) * scale + 100
        return x, y
    ax, ay = transform_point(ax, ay)
    bx, by = transform_point(bx, by)
    cx, cy = transform_point(cx, cy)
    points = [(ax, ay), (bx, by), (cx, cy)]
    rotated_points = [rotate_point(x, y, rotation, 100, 100) for x, y in points]
    min_rx = min(x for x, y in rotated_points)
    max_rx = max(x for x, y in rotated_points)
    min_ry = min(y for x, y in rotated_points)
    max_ry = max(y for x, y in rotated_points)
    dx = 0
    dy = 0
    if min_rx < margin:
        dx = margin - min_rx
    elif max_rx > 200 - margin:
        dx = (200 - margin) - max_rx
    if min_ry < margin:
        dy = margin - min_ry
    elif max_ry > 200 - margin:
        dy = (200 - margin) - max_ry
    ax += dx
    bx += dx
    cx += dx
    ay += dy
    by += dy
    cy += dy
    side_color = "#4CAF50"
    angle_color = "#2196F3"
    a1 = a2 = a3 = ''
    radius = 28
    # Highlighted sides logic
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
    # SVG polygon points string
    polygon_points = f"{ax},{ay} {bx},{by} {cx},{cy}"
    svg = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g transform="rotate({rotation} 100 100)">
            {a1}
            {a2}
            {a3}
            <polygon points="{polygon_points}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines])}
        </g>
    </svg>
    '''
    return svg 