from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from datetime import datetime, date
from django.db.models import Q, Avg, Count
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
import json

from .models import (
    Room, Booking, NewsletterSubscription, Service, ServiceBooking, Testimonial,
    Event, EventBooking, Review, UserProfile, Payment, Facility, FacilityBooking,
    Staff, ContactMessage
)

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
    if request.method == 'POST':
        # Handle booking form submission
        guest_name = request.POST.get('guest_name')
        guest_email = request.POST.get('guest_email')
        guest_phone = request.POST.get('guest_phone')
        room_id = request.POST.get('room')
        check_in_date = request.POST.get('check_in_date')
        check_out_date = request.POST.get('check_out_date')
        number_of_guests = request.POST.get('number_of_guests')
        special_requests = request.POST.get('special_requests', '')
        
        try:
            room = Room.objects.get(id=room_id)
            
            # Calculate total price
            from datetime import datetime
            check_in = datetime.strptime(check_in_date, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_date, '%Y-%m-%d').date()
            nights = (check_out - check_in).days
            total_price = room.price_per_night * nights
            
            # Create booking
            booking = Booking.objects.create(
                guest_name=guest_name,
                guest_email=guest_email,
                guest_phone=guest_phone,
                room=room,
                check_in_date=check_in_date,
                check_out_date=check_out_date,
                number_of_guests=int(number_of_guests),
                total_price=total_price,
                special_requests=special_requests,
                status='pending'
            )
            
            messages.success(request, f'Booking request submitted successfully! Booking ID: #{booking.id}. We will contact you soon to confirm your reservation.')
            return redirect('booking_confirmation', booking_id=booking.id)
            
        except Exception as e:
            messages.error(request, f'Error creating booking: {str(e)}')
    
    rooms = Room.objects.filter(is_available=True)
    return render(request, 'booking.html', {'rooms': rooms})

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

# Enhanced Views for New Features

def events(request):
    events = Event.objects.filter(is_active=True, start_date__gte=timezone.now()).order_by('start_date')
    return render(request, 'events.html', {'events': events})

def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'event_detail.html', {'event': event})

def book_event(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        try:
            participant_name = request.POST.get('participant_name')
            participant_email = request.POST.get('participant_email')
            participant_phone = request.POST.get('participant_phone')
            number_of_participants = int(request.POST.get('number_of_participants', 1))
            special_requests = request.POST.get('special_requests', '')
            
            total_price = event.price_per_person * number_of_participants
            
            # Check if event has available spots
            if event.current_participants + number_of_participants > event.max_participants:
                messages.error(request, 'Not enough spots available for this event.')
                return redirect('event_detail', event_id=event.id)
            
            # Create event booking
            event_booking = EventBooking.objects.create(
                event=event,
                participant_name=participant_name,
                participant_email=participant_email,
                participant_phone=participant_phone,
                number_of_participants=number_of_participants,
                total_price=total_price,
                special_requests=special_requests
            )
            
            # Update event participants
            event.current_participants += number_of_participants
            event.save()
            
            messages.success(request, 'Event booking successful! Please check your email for confirmation.')
            return redirect('event_booking_confirmation', booking_id=event_booking.id)
            
        except Exception as e:
            messages.error(request, f'Error booking event: {str(e)}')
            return redirect('event_detail', event_id=event.id)
    
    return render(request, 'book_event.html', {'event': event})

def event_booking_confirmation(request, booking_id):
    booking = get_object_or_404(EventBooking, id=booking_id)
    return render(request, 'event_booking_confirmation.html', {'booking': booking})

def facilities(request):
    facilities = Facility.objects.filter(is_available=True)
    return render(request, 'facilities.html', {'facilities': facilities})

def book_facility(request, facility_id):
    facility = get_object_or_404(Facility, id=facility_id)
    
    if request.method == 'POST':
        try:
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_phone = request.POST.get('contact_phone')
            start_time = datetime.strptime(request.POST.get('start_time'), '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
            end_time = datetime.strptime(request.POST.get('end_time'), '%Y-%m-%dT%H:%M').replace(tzinfo=timezone.utc)
            purpose = request.POST.get('purpose')
            number_of_people = int(request.POST.get('number_of_people', 1))
            special_requirements = request.POST.get('special_requirements', '')
            
            # Calculate total price
            hours = (end_time - start_time).total_seconds() / 3600
            total_price = facility.hourly_rate * hours if facility.hourly_rate else 0
            
            # Create facility booking
            facility_booking = FacilityBooking.objects.create(
                facility=facility,
                start_time=start_time,
                end_time=end_time,
                purpose=purpose,
                number_of_people=number_of_people,
                total_price=total_price,
                special_requirements=special_requirements,
                contact_name=contact_name,
                contact_email=contact_email,
                contact_phone=contact_phone
            )
            
            messages.success(request, 'Facility booking successful! Please check your email for confirmation.')
            return redirect('facility_booking_confirmation', booking_id=facility_booking.id)
            
        except Exception as e:
            messages.error(request, f'Error booking facility: {str(e)}')
            return redirect('facilities')
    
    return render(request, 'book_facility.html', {'facility': facility})

def facility_booking_confirmation(request, booking_id):
    booking = get_object_or_404(FacilityBooking, id=booking_id)
    return render(request, 'facility_booking_confirmation.html', {'booking': booking})

def reviews(request):
    reviews = Review.objects.filter(is_approved=True).order_by('-created_at')
    return render(request, 'reviews.html', {'reviews': reviews})

def add_review(request):
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
            title = request.POST.get('title')
            content = request.POST.get('content')
            booking_id = request.POST.get('booking_id')
            event_booking_id = request.POST.get('event_booking_id')
            
            booking = None
            event_booking = None
            
            if booking_id:
                booking = get_object_or_404(Booking, id=booking_id)
            if event_booking_id:
                event_booking = get_object_or_404(EventBooking, id=event_booking_id)
            
            review = Review.objects.create(
                user=request.user if request.user.is_authenticated else None,
                booking=booking,
                event_booking=event_booking,
                rating=rating,
                title=title,
                content=content
            )
            
            messages.success(request, 'Thank you for your review! It will be published after moderation.')
            return redirect('reviews')
            
        except Exception as e:
            messages.error(request, f'Error submitting review: {str(e)}')
    
    return redirect('reviews')

def contact_form(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone', '')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            
            ContactMessage.objects.create(
                name=name,
                email=email,
                phone=phone,
                subject=subject,
                message=message
            )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
            
        except Exception as e:
            messages.error(request, f'Error sending message: {str(e)}')
    
    return redirect('contact')

def user_register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create user profile
            UserProfile.objects.create(user=user)
            messages.success(request, 'Account created successfully! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        profile.phone_number = request.POST.get('phone_number', '')
        profile.address = request.POST.get('address', '')
        if request.POST.get('date_of_birth'):
            profile.date_of_birth = datetime.strptime(request.POST.get('date_of_birth'), '%Y-%m-%d').date()
        if request.FILES.get('profile_picture'):
            profile.profile_picture = request.FILES.get('profile_picture')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')
    
    return render(request, 'user_profile.html', {'profile': profile})

@login_required
def user_bookings(request):
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    event_bookings = EventBooking.objects.filter(user=request.user).order_by('-created_at')
    facility_bookings = FacilityBooking.objects.filter(user=request.user).order_by('-created_at')
    
    return render(request, 'user_bookings.html', {
        'bookings': bookings,
        'event_bookings': event_bookings,
        'facility_bookings': facility_bookings
    })

def search(request):
    query = request.GET.get('q', '')
    results = {
        'rooms': [],
        'events': [],
        'services': [],
        'facilities': []
    }
    
    if query:
        results['rooms'] = Room.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).filter(is_available=True)
        
        results['events'] = Event.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).filter(is_active=True, start_date__gte=timezone.now())
        
        results['services'] = Service.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).filter(is_available=True)
        
        results['facilities'] = Facility.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        ).filter(is_available=True)
    
    return render(request, 'search.html', {'results': results, 'query': query})