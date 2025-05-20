import math
import random
from triangles.interactors.triangle_gen.utils import generate_svg_triangle


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