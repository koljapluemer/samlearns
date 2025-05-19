from django.shortcuts import render

def home(request):
    return render(request, 'mushrooms/home.html') 