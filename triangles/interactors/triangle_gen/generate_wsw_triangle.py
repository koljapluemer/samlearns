import math
import random
from triangles.interactors.triangle_gen.utils import (
    arc_path, angle_arc_points, get_sweep_flag, canonical_triangle_points, rotate_and_scale_points, normalize_and_scale_triangles
)


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
    
    # First triangle (no rotation)
    points = canonical_triangle_points(side, side1, angle1)
    t1_points = points
    # Second triangle (rotated)
    rotation = random.uniform(30, 330)
    def rotate_point(x, y, angle_deg, cx, cy):
        angle_rad = math.radians(angle_deg)
        x0, y0 = x - cx, y - cy
        xr = x0 * math.cos(angle_rad) - y0 * math.sin(angle_rad)
        yr = x0 * math.sin(angle_rad) + y0 * math.cos(angle_rad)
        return xr + cx, yr + cy
    centroid_x = sum(x for x, y in points) / 3
    centroid_y = sum(y for x, y in points) / 3
    t2_points = [rotate_point(x, y, rotation, centroid_x, centroid_y) for x, y in points]
    # Normalize and scale both triangles together
    t1, t2 = normalize_and_scale_triangles(t1_points, t2_points)
    side_color = "#4CAF50"
    angle_color = "#2196F3"
    radius = 28
    # Highlight one side (AB) and the two adjacent angles (at A and B)
    highlight_lines1 = [ (t1[0], t1[1]) ]
    highlight_lines2 = [ (t2[0], t2[1]) ]
    # Angle arc at A
    p1x, p1y, p2x, p2y = angle_arc_points(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1], radius)
    sweep_flag1 = get_sweep_flag(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y)
    a1 = f'<path d="{arc_path(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y, radius, sweep_flag1)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    # Angle arc at B
    p1x2, p1y2, p2x2, p2y2 = angle_arc_points(t1[1][0], t1[1][1], t1[0][0], t1[0][1], t1[2][0], t1[2][1], radius)
    sweep_flag2 = get_sweep_flag(t1[1][0], t1[1][1], p1x2, p1y2, p2x2, p2y2)
    a2 = f'<path d="{arc_path(t1[1][0], t1[1][1], p1x2, p1y2, p2x2, p2y2, radius, sweep_flag2)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    # For the rotated triangle
    p1x3, p1y3, p2x3, p2y3 = angle_arc_points(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1], radius)
    sweep_flag3 = get_sweep_flag(t2[0][0], t2[0][1], p1x3, p1y3, p2x3, p2y3)
    a3 = f'<path d="{arc_path(t2[0][0], t2[0][1], p1x3, p1y3, p2x3, p2y3, radius, sweep_flag3)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    p1x4, p1y4, p2x4, p2y4 = angle_arc_points(t2[1][0], t2[1][1], t2[0][0], t2[0][1], t2[2][0], t2[2][1], radius)
    sweep_flag4 = get_sweep_flag(t2[1][0], t2[1][1], p1x4, p1y4, p2x4, p2y4)
    a4 = f'<path d="{arc_path(t2[1][0], t2[1][1], p1x4, p1y4, p2x4, p2y4, radius, sweep_flag4)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    polygon_points1 = f"{t1[0][0]},{t1[0][1]} {t1[1][0]},{t1[1][1]} {t1[2][0]},{t1[2][1]}"
    polygon_points2 = f"{t2[0][0]},{t2[0][1]} {t2[1][0]},{t2[1][1]} {t2[2][0]},{t2[2][1]}"
    svg1 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            {a1}
            {a2}
            <polygon points="{polygon_points1}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines1])}
        </g>
    </svg>
    '''
    svg2 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            {a3}
            {a4}
            <polygon points="{polygon_points2}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines2])}
        </g>
    </svg>
    '''
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'wsw',
        'highlighted_elements': {
            'side': side,  # The side that is the same
            'angles': [angle1, angle2]  # The two angles adjacent to the side
        }
    }