import math
import random
from triangles.interactors.triangle_gen.utils import generate_svg_triangle


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