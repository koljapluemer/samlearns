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
    
    # Hardcoded German explanations
    raw_options = [
        {'id': 'sws', 'label': 'Kongruenzsatz sws: Zwei Seiten haben die gleiche Länge, und der eingeschlossene Winkel ist gleich groß.'},
        {'id': 'sss', 'label': 'Kongruenzsatz sss: Alle drei Seitenlängen stimmen überein'},
        {'id': 'wsw', 'label': 'Kongruenzsatz wsw: Eine Seitenlänge und die beiden anliegenden Winkel stimmen überein'},
        {'id': 'ssw', 'label': 'Kongruenzsatz SsW: Zwei Seiten und die Größe des Winkels gegenüber der längeren Seite stimmen überein'},
    ]
    theorem_options = []
    for opt in raw_options:
        if ':' in opt['label']:
            title, explanation = opt['label'].split(':', 1)
        else:
            title, explanation = opt['label'], ''
        theorem_options.append({
            'id': opt['id'],
            'title': title.strip(),
            'explanation': explanation.strip(),
        })
    
    context = {
        'triangle_data': triangle_data,
        'correct_theorem': theorem_type,
        'theorem_options': theorem_options,
    }
    
    return render(request, 'triangles/identify_theorem.html', context)
