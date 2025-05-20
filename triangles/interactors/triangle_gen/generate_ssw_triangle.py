import math
import random
from triangles.interactors.triangle_gen.utils import (
    arc_path, angle_arc_points, get_sweep_flag, canonical_triangle_points, rotate_and_scale_points
)


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
    
    points = canonical_triangle_points(side1, side2, angle)
    t1 = rotate_and_scale_points(points, 0)
    rotation = random.uniform(30, 330)
    t2 = rotate_and_scale_points(points, rotation)
    side_color = "#4CAF50"
    angle_color = "#2196F3"
    radius = 28
    # Highlight two sides and the angle opposite the longer side
    if side1 >= side2:
        highlight_lines1 = [ (t1[0], t1[1]), (t1[0], t1[2]) ]
        highlight_lines2 = [ (t2[0], t2[1]), (t2[0], t2[2]) ]
        # Angle at B
        p1x, p1y, p2x, p2y = angle_arc_points(t1[1][0], t1[1][1], t1[0][0], t1[0][1], t1[2][0], t1[2][1], radius)
        sweep_flag = get_sweep_flag(t1[1][0], t1[1][1], p1x, p1y, p2x, p2y)
        a1 = f'<path d="{arc_path(t1[1][0], t1[1][1], p1x, p1y, p2x, p2y, radius, sweep_flag)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
        # Rotated
        p1x2, p1y2, p2x2, p2y2 = angle_arc_points(t2[1][0], t2[1][1], t2[0][0], t2[0][1], t2[2][0], t2[2][1], radius)
        sweep_flag2 = get_sweep_flag(t2[1][0], t2[1][1], p1x2, p1y2, p2x2, p2y2)
        a2 = f'<path d="{arc_path(t2[1][0], t2[1][1], p1x2, p1y2, p2x2, p2y2, radius, sweep_flag2)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
    else:
        highlight_lines1 = [ (t1[0], t1[1]), (t1[1], t1[2]) ]
        highlight_lines2 = [ (t2[0], t2[1]), (t2[1], t2[2]) ]
        # Angle at A
        p1x, p1y, p2x, p2y = angle_arc_points(t1[0][0], t1[0][1], t1[1][0], t1[1][1], t1[2][0], t1[2][1], radius)
        sweep_flag = get_sweep_flag(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y)
        a1 = f'<path d="{arc_path(t1[0][0], t1[0][1], p1x, p1y, p2x, p2y, radius, sweep_flag)}" fill="none" stroke="{angle_color}" stroke-width="2"/>'
        # Rotated
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
        'type': 'ssw',
        'highlighted_elements': {
            'sides': [side1, side2],  # The two sides that are the same
            'angle': angle  # The angle opposite the longer side
        }
    }