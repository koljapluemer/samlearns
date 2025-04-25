from django.shortcuts import render

def home(request):
    return render(request, 'trees_of_germany/home.html', {
        'title': 'Ready to learn the trees of Germany?'
    }) 