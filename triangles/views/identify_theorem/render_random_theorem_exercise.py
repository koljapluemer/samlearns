from django.shortcuts import render
import random
from triangles.interactors.triangle_gen.triangle_gen import generate_ssw_triangle, generate_wsw_triangle

def render_random_theorem_exercise(request):
    # Randomly choose between SSW and WSW
    theorem_type = random.choice(['ssw', 'wsw'])
    
    # Generate triangles based on the chosen theorem
    if theorem_type == 'ssw':
        triangle_data = generate_ssw_triangle()
    else:
        triangle_data = generate_wsw_triangle()
    
    # Prepare context for template
    context = {
        'triangle_data': triangle_data,
        'correct_theorem': theorem_type,
        'theorem_options': [
            {'id': 'ssw', 'label': 'SSW'},
            {'id': 'wsw', 'label': 'WSW'},
        ]
    }
    
    return render(request, 'triangles/identify_theorem.html', context)
