from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Room(models.Model):
    ROOM_TYPE_CHOICES = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('suite', 'Suite'),
        ('deluxe', 'Deluxe'),
        ('family', 'Family'),
        
    ]

    QUALITY_CHOICES = [
    ('premium', 'Premium'),
    ('standard', 'Standard'),
    ('basic', 'Basic'),
]

    name = models.CharField(max_length=100, unique=True)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    quality = models.CharField(max_length = 20, choices = QUALITY_CHOICES)
    description = models.TextField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    number_of_beds = models.IntegerField(default=1)
     
    image = models.ImageField(upload_to='room_images/', null=True, blank=True)
    amenities = models.TextField(help_text="Comma-separated list of amenities (e.g. WiFi, TV, AC, etc.)")
    room_number = models.CharField(max_length=10, unique=True)
    floor = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.room_type}) - Room {self.room_number}"


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True, null=True)
    guest_name = models.CharField(max_length=100, default='Guest')
    guest_email = models.EmailField(default='guest@example.com')
    guest_phone = models.CharField(max_length=20, default='N/A')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} - {self.room.name} by {self.guest_name}"


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.IntegerField(blank=True, null=True, help_text="Duration in minutes")
    is_available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='service_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ServiceBooking(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='service_bookings')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    scheduled_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service.name} for Booking {self.booking.id}"


class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    preferences = models.JSONField(default=dict, help_text="User preferences for types of updates")

    def __str__(self):
        return self.email


class Testimonial(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='testimonial_images/', null=True, blank=True)
    rating = models.IntegerField(default=5, choices=[(i, i) for i in range(1, 6)])
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.role}"
    
    class Meta:
        ordering = ['-created_at']



