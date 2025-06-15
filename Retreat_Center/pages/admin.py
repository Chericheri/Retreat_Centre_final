from django.contrib import admin
from .models import Room, Booking, Service, ServiceBooking, NewsletterSubscription, Testimonial

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'room_type', 'quality', 'price_per_night', 'is_available', 'room_number', 'floor')
    list_filter = ('room_type', 'quality', 'is_available', 'floor')
    search_fields = ('name', 'room_number', 'description')
    ordering = ('room_number',)

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'guest_name', 'guest_email', 'guest_phone', 'room', 'check_in_date', 'check_out_date', 'number_of_guests', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'check_in_date', 'check_out_date', 'room')
    search_fields = ('guest_name', 'guest_email', 'guest_phone', 'room__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Guest Information', {
            'fields': ('guest_name', 'guest_email', 'guest_phone')
        }),
        ('Booking Details', {
            'fields': ('room', 'check_in_date', 'check_out_date', 'number_of_guests', 'total_price', 'status')
        }),
        ('Additional Information', {
            'fields': ('special_requests', 'created_at', 'updated_at')
        }),
    )

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'duration', 'is_available')
    list_filter = ('is_available',)
    search_fields = ('name', 'description')

@admin.register(ServiceBooking)
class ServiceBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'booking', 'service', 'quantity', 'scheduled_date', 'total_price', 'created_at')
    list_filter = ('scheduled_date', 'service')
    search_fields = ('booking__guest_name', 'service__name')
    readonly_fields = ('created_at',)

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('email', 'is_active', 'subscribed_at')
    list_filter = ('is_active', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'rating', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('name', 'content', 'role')
    readonly_fields = ('created_at',)