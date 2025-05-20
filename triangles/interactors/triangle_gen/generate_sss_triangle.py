import math
import random
from triangles.interactors.triangle_gen.utils import (
    arc_path, angle_arc_points, get_sweep_flag, canonical_triangle_points, rotate_and_scale_points
)


def generate_sss_triangle():
    # Generate a random triangle with three sides of the same length
    # Returns data for two congruent triangles with different rotations
    
    # Generate random side length
    side = random.uniform(50, 100)
    
    # For equilateral triangle, all sides are equal and all angles are 60 degrees
    angle = 60
    
    # Get canonical points
    points = canonical_triangle_points(side, side, angle)
    
    # First triangle (no rotation)
    t1 = rotate_and_scale_points(points, 0)
    
    # Second triangle (random rotation)
    rotation = random.uniform(30, 330)
    t2 = rotate_and_scale_points(points, rotation)
    
    # Highlight all three sides
    side_color = "#4CAF50"
    polygon_points1 = f"{t1[0][0]},{t1[0][1]} {t1[1][0]},{t1[1][1]} {t1[2][0]},{t1[2][1]}"
    polygon_points2 = f"{t2[0][0]},{t2[0][1]} {t2[1][0]},{t2[1][1]} {t2[2][0]},{t2[2][1]}"
    highlight_lines1 = [ (t1[i], t1[(i+1)%3]) for i in range(3) ]
    highlight_lines2 = [ (t2[i], t2[(i+1)%3]) for i in range(3) ]
    
    # Generate SVG data for two triangles
    svg1 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            <polygon points="{polygon_points1}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines1])}
        </g>
    </svg>
    '''
    svg2 = f'''
    <svg viewBox="0 0 200 200" width="200" height="200">
        <g>
            <polygon points="{polygon_points2}" fill="none" stroke="black" stroke-width="5"/>
            {''.join([f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{side_color}" stroke-width="5"/>' for (x1, y1), (x2, y2) in highlight_lines2])}
        </g>
    </svg>
    '''
    
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'sss',
        'highlighted_elements': {
            'sides': [side, side, side]  # All three sides are equal
        }
    }