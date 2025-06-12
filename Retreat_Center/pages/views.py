from django.shortcuts import render
from .models import Room

# Create your views here.



def home (request):
    return render (request, 'index.html')


def room (request):
    rooms = Room.objects.all()
    return render (request,'room.html', {'rooms':rooms})