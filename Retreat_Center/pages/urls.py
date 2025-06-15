from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('room/', views.room, name='room'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    
    # New URL patterns
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('book-service/<int:service_id>/', views.book_service, name='book_service'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
]