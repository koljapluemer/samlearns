from django.http import HttpResponse
from django.template.loader import render_to_string

def submit_theorem_answer(request):
    if request.method == 'POST':
        selected_theorem = request.POST.get('selected_theorem')
        correct_theorem = request.POST.get('correct_theorem')
        
        is_correct = selected_theorem == correct_theorem
        
        # Render the result message
        result_html = render_to_string(
            'triangles/identify_theorem/result_message.html',
            {
                'is_correct': is_correct,
                'selected_theorem': selected_theorem.upper(),
                'correct_theorem': correct_theorem.upper()
            }
        )
        
        return HttpResponse(result_html)
    
    return HttpResponse('Invalid request method', status=400) 