from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('room/', views.room, name='room'),
    path('booking/', views.booking, name='booking'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('testimonial/', views.testimonial, name='testimonial'),
    
    # Booking system
    path('book-room/<int:room_id>/', views.book_room, name='book_room'),
    path('book-service/<int:service_id>/', views.book_service, name='book_service'),
    path('booking-confirmation/<int:booking_id>/', views.booking_confirmation, name='booking_confirmation'),
    
    # Events
    path('events/', views.events, name='events'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),
    path('book-event/<int:event_id>/', views.book_event, name='book_event'),
    path('event-booking-confirmation/<int:booking_id>/', views.event_booking_confirmation, name='event_booking_confirmation'),
    
    # Facilities
    path('facilities/', views.facilities, name='facilities'),
    path('book-facility/<int:facility_id>/', views.book_facility, name='book_facility'),
    path('facility-booking-confirmation/<int:booking_id>/', views.facility_booking_confirmation, name='facility_booking_confirmation'),
    
    # Reviews and testimonials
    path('reviews/', views.reviews, name='reviews'),
    path('add-review/', views.add_review, name='add_review'),
    path('add-testimonial/', views.add_testimonial, name='add_testimonial'),
    
    # User features
    path('register/', views.user_register, name='register'),
    path('profile/', views.user_profile, name='user_profile'),
    path('my-bookings/', views.user_bookings, name='user_bookings'),
    
    # Contact and newsletter
    path('contact-form/', views.contact_form, name='contact_form'),
    path('subscribe-newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
    
    # Search
    path('search/', views.search, name='search'),
]