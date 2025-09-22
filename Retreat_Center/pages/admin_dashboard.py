from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Count, Sum, Q
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Booking, Event, Facility, Payment, ContactMessage, Testimonial, Review

class AdminDashboard:
    def __init__(self, admin_site):
        self.admin_site = admin_site
    
    def get_urls(self):
        urls = [
            path('dashboard/', self.admin_site.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return urls
    
    def dashboard_view(self, request):
        # Get current date and time
        now = timezone.now()
        today = now.date()
        this_month = now.replace(day=1)
        
        # Booking statistics
        total_bookings = Booking.objects.count()
        confirmed_bookings = Booking.objects.filter(status='confirmed').count()
        pending_bookings = Booking.objects.filter(status='pending').count()
        cancelled_bookings = Booking.objects.filter(status='cancelled').count()
        
        # Revenue statistics
        total_revenue = Payment.objects.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        monthly_revenue = Payment.objects.filter(
            status='completed',
            created_at__gte=this_month
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Event statistics
        total_events = Event.objects.count()
        active_events = Event.objects.filter(is_active=True).count()
        upcoming_events = Event.objects.filter(
            start_date__gte=now,
            is_active=True
        ).count()
        
        # Facility statistics
        total_facilities = Facility.objects.count()
        available_facilities = Facility.objects.filter(is_available=True).count()
        
        # Recent activity
        recent_bookings = Booking.objects.order_by('-created_at')[:5]
        recent_contacts = ContactMessage.objects.order_by('-created_at')[:5]
        recent_testimonials = Testimonial.objects.filter(is_approved=True).order_by('-created_at')[:3]
        recent_reviews = Review.objects.filter(is_approved=True).order_by('-created_at')[:3]
        
        # Monthly booking trends (last 6 months)
        monthly_stats = []
        for i in range(6):
            month_start = (now.replace(day=1) - timedelta(days=30*i)).replace(day=1)
            month_end = month_start + timedelta(days=32)
            month_end = month_end.replace(day=1) - timedelta(days=1)
            
            month_bookings = Booking.objects.filter(
                created_at__gte=month_start,
                created_at__lte=month_end
            ).count()
            
            month_revenue = Payment.objects.filter(
                status='completed',
                created_at__gte=month_start,
                created_at__lte=month_end
            ).aggregate(total=Sum('amount'))['total'] or 0
            
            monthly_stats.append({
                'month': month_start.strftime('%B %Y'),
                'bookings': month_bookings,
                'revenue': month_revenue
            })
        
        context = {
            'title': 'Retreat Center Dashboard',
            'total_bookings': total_bookings,
            'confirmed_bookings': confirmed_bookings,
            'pending_bookings': pending_bookings,
            'cancelled_bookings': cancelled_bookings,
            'total_revenue': total_revenue,
            'monthly_revenue': monthly_revenue,
            'total_events': total_events,
            'active_events': active_events,
            'upcoming_events': upcoming_events,
            'total_facilities': total_facilities,
            'available_facilities': available_facilities,
            'recent_bookings': recent_bookings,
            'recent_contacts': recent_contacts,
            'recent_testimonials': recent_testimonials,
            'recent_reviews': recent_reviews,
            'monthly_stats': monthly_stats,
        }
        
        return render(request, 'admin/dashboard.html', context)

# Custom admin site
class RetreatCenterAdminSite(admin.AdminSite):
    site_header = "ARC Retreat Center Administration"
    site_title = "ARC Admin"
    index_title = "Welcome to ARC Retreat Center Administration"
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.dashboard = AdminDashboard(self)
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = self.dashboard.get_urls()
        return custom_urls + urls

# Create custom admin site instance
retreat_admin_site = RetreatCenterAdminSite(name='retreat_admin')
