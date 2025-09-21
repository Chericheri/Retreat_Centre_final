from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Room, Booking, NewsletterSubscription, Service, ServiceBooking, Testimonial
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime

# Create your views here.

def index(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'index.html')

def room(request):
    rooms = Room.objects.all()
    return render(request, 'room.html', {'rooms': rooms})

def about(request):
    return render(request, 'about.html')

def service(request):
    services = Service.objects.filter(is_available=True)
    return render(request, 'service.html', {'services': services})

def booking(request):
    return render(request, 'booking.html')

def testimonial(request):
    testimonials = Testimonial.objects.filter(is_approved=True)
    return render(request, 'testimonial.html', {'testimonials': testimonials})

def add_testimonial(request):
    if request.method == 'POST':
        try:
            testimonial = Testimonial.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=request.POST.get('name'),
                role=request.POST.get('role'),
                content=request.POST.get('content'),
                rating=int(request.POST.get('rating', 5)),
                image=request.FILES.get('image')
            )
            messages.success(request, 'Thank you for your testimonial! It will be reviewed and published soon.')
        except Exception as e:
            messages.error(request, f'Error submitting testimonial: {str(e)}')
    return redirect('testimonial')

def contact(request):
    return render(request, 'contact.html')

def team(request):
    return render(request, 'team.html')

def book_room(request, room_id):
    if request.method == 'POST':
        try:
            room = Room.objects.get(id=room_id)
            check_in = datetime.strptime(request.POST.get('check_in'), '%Y-%m-%d').date()
            check_out = datetime.strptime(request.POST.get('check_out'), '%Y-%m-%d').date()
            guests = int(request.POST.get('guests', 1))
            
            # Calculate total price
            nights = (check_out - check_in).days
            total_price = room.price_per_night * nights
            
            # Create booking with guest information
            booking = Booking.objects.create(
                room=room,
                check_in_date=check_in,
                check_out_date=check_out,
                number_of_guests=guests,
                total_price=total_price,
                special_requests=request.POST.get('special_requests', ''),
                guest_name=request.POST.get('guest_name', ''),
                guest_email=request.POST.get('guest_email', ''),
                guest_phone=request.POST.get('guest_phone', '')
            )
            
            # Update room availability
            room.is_available = False
            room.save()
            
            messages.success(request, 'Room booked successfully! Please check your email for payment instructions.')
            return redirect('booking_confirmation', booking_id=booking.id)
            
        except Exception as e:
            messages.error(request, f'Error booking room: {str(e)}')
            return redirect('room')
    
    return redirect('room')

def book_service(request, service_id):
    if request.method == 'POST':
        try:
            service = Service.objects.get(id=service_id)
            booking_id = request.POST.get('booking_id')
            quantity = int(request.POST.get('quantity', 1))
            scheduled_date = datetime.strptime(request.POST.get('scheduled_date'), '%Y-%m-%d').date()
            
            # Get the associated room booking
            booking = Booking.objects.get(id=booking_id)
            
            # Create service booking
            service_booking = ServiceBooking.objects.create(
                booking=booking,
                service=service,
                quantity=quantity,
                scheduled_date=scheduled_date,
                total_price=service.price * quantity
            )
            
            messages.success(request, 'Service booked successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
            
        except Exception as e:
            messages.error(request, f'Error booking service: {str(e)}')
            return redirect('service')
    
    return redirect('service')

def subscribe_newsletter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                subscription, created = NewsletterSubscription.objects.get_or_create(
                    email=email,
                    defaults={'is_active': True}
                )
                if not created:
                    subscription.is_active = True
                    subscription.save()
                messages.success(request, 'Successfully subscribed to newsletter!')
            except Exception as e:
                messages.error(request, f'Error subscribing to newsletter: {str(e)}')
        else:
            messages.error(request, 'Please provide a valid email address.')
    
    return redirect(request.META.get('HTTP_REFERER', 'home'))

def booking_confirmation(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    service_bookings = ServiceBooking.objects.filter(booking=booking)
    return render(request, 'booking_confirmation.html', {
        'booking': booking,
        'service_bookings': service_bookings
    })