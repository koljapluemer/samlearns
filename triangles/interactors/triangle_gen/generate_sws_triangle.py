import math
import random
from triangles.interactors.triangle_gen.utils import (
    arc_path, angle_arc_points, get_sweep_flag, canonical_triangle_points, rotate_and_scale_points, normalize_and_scale_triangles
)


def generate_sws_triangle():
    # Generate a random triangle with two sides and the included angle
    # Returns data for two congruent triangles with different rotations
    
    # Generate random side lengths
    side1 = random.uniform(50, 100)
    side2 = random.uniform(50, 100)
    
    # Generate random included angle (in degrees)
    # Keep it between 30 and 150 degrees to avoid very acute or obtuse angles
    angle = random.uniform(30, 150)
    
    # Calculate third side using law of cosines
    angle_rad = math.radians(angle)
    side3 = math.sqrt(side1**2 + side2**2 - 2*side1*side2*math.cos(angle_rad))
    
    points = canonical_triangle_points(side1, side2, angle)
    t1_points = points
    rotation = random.uniform(30, 330)
    # Rotate around centroid
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
    # Highlight two adjacent sides (AB, AC) and included angle at A
    highlight_lines1 = [ (t1[0], t1[1]), (t1[0], t1[2]) ]
    highlight_lines2 = [ (t2[0], t2[1]), (t2[0], t2[2]) ]
    # Angle arc at A
    p1x, p1y, p2x, p2y = angle_arc_points(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1], radius)
    sweep_flag = get_sweep_flag(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y)
    a1 = f'<path d="{arc_path(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y, radius, sweep_flag)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    # For the rotated triangle
    p1x2, p1y2, p2x2, p2y2 = angle_arc_points(t2[0][0], t2[0][1], t2[1][0], t2[1][1], t2[2][0], t2[2][1], radius)
    sweep_flag2 = get_sweep_flag(t2[0][0], t2[0][1], p1x2, p1y2, p2x2, p2y2)
    a2 = f'<path d="{arc_path(t2[0][0], t2[0][1], p1x2, p1y2, p2x2, p2y2, radius, sweep_flag2)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    polygon_points1 = f"{t1[0][0]},{t1[0][1]} {t1[1][0]},{t1[1][1]} {t1[2][0]},{t1[2][1]}"
    polygon_points2 = f"{t2[0][0]},{t2[0][1]} {t2[1][0]},{t2[1][1]} {t2[2][0]},{t2[2][1]}"
    svg1 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            {a1}
            <polygon points="{polygon_points1}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines1])}
        </g>
    </svg>
    '''
    svg2 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            {a2}
            <polygon points="{polygon_points2}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines2])}
        </g>
    </svg>
    '''
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'sws',
        'highlighted_elements': {
            'sides': [side1, side2],  # The two sides that are the same
            'angle': angle  # The included angle
        }
    }