from django.db import models

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



