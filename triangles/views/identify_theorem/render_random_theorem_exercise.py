from django.shortcuts import render
import random
from triangles.models import Topic
from triangles.interactors.triangle_gen.generate_sss_triangle import generate_sss_triangle
from triangles.interactors.triangle_gen.generate_ssw_triangle import generate_ssw_triangle
from triangles.interactors.triangle_gen.generate_sws_triangle import generate_sws_triangle
from triangles.interactors.triangle_gen.generate_wsw_triangle import generate_wsw_triangle

def render_random_theorem_exercise(request):
    # Get all topics that are congruence theorems
    congruence_theorems = Topic.objects.filter(is_congruence_theorem=True)
    
    if not congruence_theorems.exists():
        raise ValueError("No congruence theorem topics found in the database")
    
    # Randomly choose a theorem topic
    theorem_topic = random.choice(list(congruence_theorems))
    theorem_type = theorem_topic.name.lower()
    
    # Generate triangles based on the chosen theorem
    if theorem_type == 'sss':
        triangle_data = generate_sss_triangle()
    elif theorem_type == 'ssw':
        triangle_data = generate_ssw_triangle()
    elif theorem_type == 'sws':
        triangle_data = generate_sws_triangle()
    elif theorem_type == 'wsw':
        triangle_data = generate_wsw_triangle()
    else:
        raise ValueError(f"Unknown theorem type: {theorem_type}")
    
    # Prepare context for template
    context = {
        'triangle_data': triangle_data,
        'correct_theorem': theorem_type,
        'theorem_options': [
            {'id': 'sss', 'label': 'SSS'},
            {'id': 'ssw', 'label': 'SSW'},
            {'id': 'sws', 'label': 'SWS'},
            {'id': 'wsw', 'label': 'WSW'},
        ]
    }
    
    return render(request, 'triangles/identify_theorem.html', context)
