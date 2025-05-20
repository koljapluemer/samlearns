from django.shortcuts import render
from guest_user.decorators import allow_guest_user

@allow_guest_user
def all_topics_learned(request):
    return render(request, 'triangles/do_something_else.html')
