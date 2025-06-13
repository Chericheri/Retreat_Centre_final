from django.urls import path
from .import views


urlpatterns = [

path('', views.home, name='home'),
path('rooms/', views.room, name = 'room'),
path('about/', views.about, name='about'),
path('service/', views.service, name='service'),
path('booking/', views.booking, name='booking'),
path('testimonial/', views.testimonial, name='testimonial'),
path('contact/', views.contact, name='contact'),


]