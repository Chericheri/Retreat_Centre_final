from django.shortcuts import render
from .models import Room

# Create your views here.



def home (request):
    return render (request, 'index.html')


def room (request):
    rooms = Room.objects.all()
    return render (request,'room.html', {'rooms':rooms})

def about (request):
    return render (request, 'about.html')

def service (request):
    return render (request, 'service.html')

def booking (request):
    return render (request, 'booking.html')

def testimonial (request):
    return render (request, 'testimonial.html')

def contact (request):
    return render (request, 'contact.html')