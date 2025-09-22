from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.db.models import Count, Sum
from .models import (
    Room, Booking, Service, ServiceBooking, NewsletterSubscription, Testimonial,
    Event, EventBooking, Review, UserProfile, Payment, Facility, FacilityBooking,
    Staff, ContactMessage
)

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
    actions = ['mark_as_confirmed', 'mark_as_cancelled', 'mark_as_completed']
    
    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status='confirmed')
        self.message_user(request, f'{updated} bookings marked as confirmed.', messages.SUCCESS)
    mark_as_confirmed.short_description = "Mark selected bookings as confirmed"
    
    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status='cancelled')
        self.message_user(request, f'{updated} bookings marked as cancelled.', messages.SUCCESS)
    mark_as_cancelled.short_description = "Mark selected bookings as cancelled"
    
    def mark_as_completed(self, request, queryset):
        updated = queryset.update(status='completed')
        self.message_user(request, f'{updated} bookings marked as completed.', messages.SUCCESS)
    mark_as_completed.short_description = "Mark selected bookings as completed"
    
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

# Additional Admin Classes for New Models

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'start_date', 'end_date', 'max_participants', 'current_participants', 'price_per_person', 'is_active', 'spots_remaining_display')
    list_filter = ('event_type', 'is_active', 'start_date')
    search_fields = ('name', 'description', 'location')
    readonly_fields = ('created_at', 'updated_at', 'spots_remaining_display')
    ordering = ('-start_date',)
    actions = ['activate_events', 'deactivate_events']
    
    def spots_remaining_display(self, obj):
        remaining = obj.spots_remaining
        if remaining <= 0:
            return format_html('<span style="color: red; font-weight: bold;">FULL</span>')
        elif remaining <= 5:
            return format_html('<span style="color: orange; font-weight: bold;">{} spots left</span>', remaining)
        else:
            return format_html('<span style="color: green;">{} spots left</span>', remaining)
    spots_remaining_display.short_description = 'Spots Remaining'
    
    def activate_events(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, f'{updated} events activated.', messages.SUCCESS)
    activate_events.short_description = "Activate selected events"
    
    def deactivate_events(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, f'{updated} events deactivated.', messages.SUCCESS)
    deactivate_events.short_description = "Deactivate selected events"

@admin.register(EventBooking)
class EventBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'participant_name', 'participant_email', 'event', 'number_of_participants', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'event', 'created_at')
    search_fields = ('participant_name', 'participant_email', 'event__name')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('is_approved', 'rating', 'created_at')
    search_fields = ('title', 'content', 'user__username')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone_number')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'payment_method', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'payment_method', 'created_at')
    search_fields = ('transaction_id', 'payment_reference')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'hourly_rate', 'is_available', 'booking_count')
    list_filter = ('is_available',)
    search_fields = ('name', 'description', 'amenities')
    actions = ['activate_facilities', 'deactivate_facilities']
    
    def booking_count(self, obj):
        count = obj.facilitybooking_set.count()
        return format_html('<span style="color: blue;">{} bookings</span>', count)
    booking_count.short_description = 'Total Bookings'
    
    def activate_facilities(self, request, queryset):
        updated = queryset.update(is_available=True)
        self.message_user(request, f'{updated} facilities activated.', messages.SUCCESS)
    activate_facilities.short_description = "Activate selected facilities"
    
    def deactivate_facilities(self, request, queryset):
        updated = queryset.update(is_available=False)
        self.message_user(request, f'{updated} facilities deactivated.', messages.SUCCESS)
    deactivate_facilities.short_description = "Deactivate selected facilities"

@admin.register(FacilityBooking)
class FacilityBookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'contact_name', 'contact_email', 'facility', 'start_time', 'end_time', 'number_of_people', 'total_price', 'status')
    list_filter = ('status', 'facility', 'start_time')
    search_fields = ('contact_name', 'contact_email', 'facility__name', 'purpose')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ('user', 'employee_id', 'position', 'department', 'hire_date', 'is_active')
    list_filter = ('department', 'position', 'is_active', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'employee_id', 'position')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)