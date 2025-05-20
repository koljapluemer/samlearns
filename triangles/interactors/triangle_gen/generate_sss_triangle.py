import math
import random
from triangles.interactors.triangle_gen.utils import generate_svg_triangle


def generate_sss_triangle():
    # Generate a random triangle with three sides of the same length
    # Returns data for two congruent triangles with different rotations
    
    # Generate random side length
    side = random.uniform(50, 100)
    
    # For equilateral triangle, all sides are equal and all angles are 60 degrees
    angle = 60
    
    # Generate SVG data for two triangles
    # First triangle
    svg1 = generate_svg_triangle(side, side, side, angle, 0, 'sss')
    # Second triangle (rotated)
    rotation = random.uniform(30, 330)
    svg2 = generate_svg_triangle(side, side, side, angle, rotation, 'sss')
    
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'sss',
        'highlighted_elements': {
            'sides': [side, side, side]  # All three sides are equal
        }
    }