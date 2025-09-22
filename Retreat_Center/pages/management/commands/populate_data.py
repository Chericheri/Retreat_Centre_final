from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from pages.models import (
    Room, Service, Event, Facility, Testimonial, Staff, UserProfile
)
from decimal import Decimal
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create rooms
        rooms_data = [
            {
                'name': 'Standard Single Room',
                'room_type': 'single',
                'quality': 'standard',
                'description': 'Comfortable single room with all basic amenities for a pleasant stay.',
                'price_per_night': Decimal('5000.00'),
                'room_number': '101',
                'floor': 1,
                'number_of_beds': 1,
                'amenities': 'WiFi, TV, AC, Private Bathroom, Room Service'
            },
            {
                'name': 'Deluxe Double Room',
                'room_type': 'double',
                'quality': 'premium',
                'description': 'Spacious deluxe room with premium amenities and beautiful views.',
                'price_per_night': Decimal('8000.00'),
                'room_number': '201',
                'floor': 2,
                'number_of_beds': 2,
                'amenities': 'WiFi, TV, AC, Private Bathroom, Mini Bar, Room Service, Balcony'
            },
            {
                'name': 'Executive Suite',
                'room_type': 'suite',
                'quality': 'premium',
                'description': 'Luxurious executive suite with separate living area and premium services.',
                'price_per_night': Decimal('12000.00'),
                'room_number': '301',
                'floor': 3,
                'number_of_beds': 2,
                'amenities': 'WiFi, TV, AC, Private Bathroom, Mini Bar, Room Service, Balcony, Living Room'
            },
            {
                'name': 'Family Room',
                'room_type': 'family',
                'quality': 'standard',
                'description': 'Perfect for families with children, featuring multiple beds and family-friendly amenities.',
                'price_per_night': Decimal('10000.00'),
                'room_number': '102',
                'floor': 1,
                'number_of_beds': 3,
                'amenities': 'WiFi, TV, AC, Private Bathroom, Room Service, Extra Beds'
            }
        ]
        
        for room_data in rooms_data:
            room, created = Room.objects.get_or_create(
                room_number=room_data['room_number'],
                defaults=room_data
            )
            if created:
                self.stdout.write(f'Created room: {room.name}')
        
        # Create services
        services_data = [
            {
                'name': 'Spa & Wellness',
                'description': 'Relax and rejuvenate with our premium spa treatments and massages.',
                'price': Decimal('3000.00'),
                'duration': 60,
                'is_available': True
            },
            {
                'name': 'Yoga Classes',
                'description': 'Professional yoga sessions for all levels in our peaceful retreat.',
                'price': Decimal('2000.00'),
                'duration': 90,
                'is_available': True
            },
            {
                'name': 'Conference Facilities',
                'description': 'State-of-the-art conference rooms for your business meetings.',
                'price': Decimal('5000.00'),
                'duration': 240,
                'is_available': True
            },
            {
                'name': 'Wedding Packages',
                'description': 'Complete wedding solutions with beautiful venues and catering.',
                'price': Decimal('50000.00'),
                'duration': 480,
                'is_available': True
            },
            {
                'name': 'Restaurant Service',
                'description': 'Gourmet dining experience with local and international cuisine.',
                'price': Decimal('1500.00'),
                'duration': 60,
                'is_available': True
            },
            {
                'name': 'Room Service',
                'description': '24/7 room service for your comfort and convenience.',
                'price': Decimal('500.00'),
                'duration': 30,
                'is_available': True
            }
        ]
        
        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                name=service_data['name'],
                defaults=service_data
            )
            if created:
                self.stdout.write(f'Created service: {service.name}')
        
        # Create events
        events_data = [
            {
                'name': 'Meditation Retreat Weekend',
                'description': 'A peaceful weekend retreat focused on meditation and mindfulness practices.',
                'event_type': 'retreat',
                'start_date': datetime.now() + timedelta(days=30),
                'end_date': datetime.now() + timedelta(days=32),
                'max_participants': 20,
                'price_per_person': Decimal('15000.00'),
                'location': 'Main Meditation Hall',
                'is_active': True
            },
            {
                'name': 'Corporate Wellness Workshop',
                'description': 'Team building and wellness workshop for corporate groups.',
                'event_type': 'workshop',
                'start_date': datetime.now() + timedelta(days=45),
                'end_date': datetime.now() + timedelta(days=45, hours=8),
                'max_participants': 30,
                'price_per_person': Decimal('8000.00'),
                'location': 'Conference Room A',
                'is_active': True
            },
            {
                'name': 'Yoga Teacher Training',
                'description': 'Intensive yoga teacher training program for aspiring instructors.',
                'event_type': 'yoga',
                'start_date': datetime.now() + timedelta(days=60),
                'end_date': datetime.now() + timedelta(days=67),
                'max_participants': 15,
                'price_per_person': Decimal('25000.00'),
                'location': 'Yoga Studio',
                'is_active': True
            }
        ]
        
        for event_data in events_data:
            event, created = Event.objects.get_or_create(
                name=event_data['name'],
                defaults=event_data
            )
            if created:
                self.stdout.write(f'Created event: {event.name}')
        
        # Create facilities
        facilities_data = [
            {
                'name': 'Conference Room A',
                'description': 'Large conference room with modern AV equipment and seating for up to 50 people.',
                'capacity': 50,
                'hourly_rate': Decimal('2000.00'),
                'amenities': 'Projector, Whiteboard, WiFi, Air Conditioning, Catering Available',
                'is_available': True
            },
            {
                'name': 'Yoga Studio',
                'description': 'Peaceful yoga studio with natural lighting and yoga mats provided.',
                'capacity': 25,
                'hourly_rate': Decimal('1500.00'),
                'amenities': 'Yoga Mats, Mirrors, Sound System, Natural Lighting',
                'is_available': True
            },
            {
                'name': 'Meditation Hall',
                'description': 'Quiet meditation hall perfect for spiritual gatherings and meditation sessions.',
                'capacity': 75,
                'hourly_rate': Decimal('1000.00'),
                'amenities': 'Cushions, Sound System, Natural Lighting, Peaceful Environment',
                'is_available': True
            },
            {
                'name': 'Wedding Garden',
                'description': 'Beautiful outdoor garden space perfect for weddings and special events.',
                'capacity': 100,
                'hourly_rate': Decimal('5000.00'),
                'amenities': 'Outdoor Space, Garden Setting, Sound System, Catering Available',
                'is_available': True
            }
        ]
        
        for facility_data in facilities_data:
            facility, created = Facility.objects.get_or_create(
                name=facility_data['name'],
                defaults=facility_data
            )
            if created:
                self.stdout.write(f'Created facility: {facility.name}')
        
        # Create testimonials
        testimonials_data = [
            {
                'name': 'Sarah Johnson',
                'role': 'Guest',
                'content': 'The retreat center was absolutely wonderful! The staff was friendly, the rooms were clean, and the atmosphere was so peaceful. I would definitely come back again.',
                'rating': 5,
                'is_approved': True
            },
            {
                'name': 'Michael Brown',
                'role': 'Corporate Client',
                'content': 'Perfect place for our corporate retreat. The conference facilities were excellent and the food was delicious. Highly recommended for business events.',
                'rating': 5,
                'is_approved': True
            },
            {
                'name': 'David & Emily Wilson',
                'role': 'Wedding Couple',
                'content': 'We had our wedding at ANN\'s Retreat Center and it was magical! The team took care of every detail and made our special day perfect.',
                'rating': 5,
                'is_approved': True
            },
            {
                'name': 'Lisa Chen',
                'role': 'Yoga Instructor',
                'content': 'The yoga studio is perfect for classes. The natural lighting and peaceful environment create the ideal setting for yoga practice.',
                'rating': 5,
                'is_approved': True
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'Created testimonial: {testimonial.name}')
        
        # Create a superuser if it doesn't exist
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username='admin',
                email='admin@annsretreat.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            self.stdout.write('Created superuser: admin (password: admin123)')
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample data!')
        )
