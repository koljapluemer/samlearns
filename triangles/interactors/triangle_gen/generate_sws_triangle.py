import math
import random
from triangles.interactors.triangle_gen.utils import generate_svg_triangle


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
    
    # Generate SVG data for two triangles
    # First triangle
    svg1 = generate_svg_triangle(side1, side2, side3, angle, 0, 'sws')
    # Second triangle (rotated)
    rotation = random.uniform(30, 330)
    svg2 = generate_svg_triangle(side1, side2, side3, angle, rotation, 'sws')
    
    return {
        'svg1': svg1,
        'svg2': svg2,
        'type': 'sws',
        'highlighted_elements': {
            'sides': [side1, side2],  # The two sides that are the same
            'angle': angle  # The included angle
        }
    }