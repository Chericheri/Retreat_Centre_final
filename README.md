# ANN's Retreat Center (ARC) - Django Web Application

A comprehensive retreat center management system built with Django, featuring room booking, event management, facility rentals, and more.

## Features

### 🏨 **Core Features**
- **Room Management**: Multiple room types with booking system
- **Event Management**: Workshops, retreats, conferences, and special events
- **Facility Booking**: Conference rooms, yoga studios, meditation halls
- **Service Management**: Spa, yoga classes, restaurant, room service
- **User Authentication**: Registration, login, user profiles
- **Admin Panel**: Comprehensive admin interface with Jazzmin

### 🎯 **Key Capabilities**
- **Booking System**: Complete booking workflow with confirmations
- **Payment Integration**: Ready for M-Pesa, card payments, bank transfers
- **Reviews & Testimonials**: Customer feedback system
- **Newsletter Subscription**: Email marketing capabilities
- **Search Functionality**: Search across rooms, events, services, facilities
- **Responsive Design**: Mobile-friendly Bootstrap interface

### 📱 **User Features**
- User registration and profiles
- Booking history and management
- Event participation
- Review submission
- Newsletter subscription

### 🔧 **Admin Features**
- Complete booking management
- Event and facility management
- User and staff management
- Payment tracking
- Review moderation
- Analytics and reporting

## Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)
- Git

### Quick Start

1. **Clone the repository**
```bash
git clone <repository-url>
cd Retreat_Center_final
```

2. **Create and activate virtual environment**
```bash
# Windows
python -m venv retreat
retreat\Scripts\activate

# macOS/Linux
python -m venv retreat
source retreat/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run migrations**
```bash
cd Retreat_Center
python manage.py migrate
```

5. **Create sample data**
```bash
python manage.py populate_data
```

6. **Create superuser**
```bash
python manage.py createsuperuser
```

7. **Start development server**
```bash
python manage.py runserver
```

8. **Access the application**
- **Main Site**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Default Admin**: username: `admin`, password: `admin123`

## Project Structure

```
Retreat_Center/
├── manage.py
├── Retreat_Center/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── pages/
│   ├── models.py          # Data models
│   ├── views.py           # View functions
│   ├── urls.py            # URL patterns
│   ├── admin.py           # Admin configuration
│   ├── templates/         # HTML templates
│   ├── static/           # Static files (CSS, JS, images)
│   └── management/       # Management commands
├── media/                # User uploaded files
└── requirements.txt      # Python dependencies
```

## Models Overview

### Core Models
- **Room**: Room types, pricing, amenities
- **Booking**: Room reservations with guest information
- **Service**: Spa, yoga, restaurant services
- **Event**: Workshops, retreats, conferences
- **Facility**: Conference rooms, studios, halls
- **UserProfile**: Extended user information
- **Payment**: Payment tracking and processing
- **Review**: Customer reviews and ratings
- **Staff**: Employee management
- **ContactMessage**: Contact form submissions

## Key Features Explained

### 🏨 **Room Booking System**
- Multiple room types (Single, Double, Suite, Family)
- Quality levels (Standard, Premium, Basic)
- Real-time availability checking
- Guest information collection
- Booking confirmations

### 🎪 **Event Management**
- Event creation and management
- Participant registration
- Capacity management
- Event types: Workshops, Retreats, Conferences, Yoga, etc.
- Pricing per person

### 🏢 **Facility Booking**
- Hourly rate booking system
- Capacity management
- Purpose tracking
- Special requirements handling

### 💳 **Payment System**
- Multiple payment methods (M-Pesa, Card, Bank Transfer, Cash)
- Payment status tracking
- Transaction ID management
- Refund capabilities

### 👥 **User Management**
- User registration and authentication
- Profile management
- Booking history
- Review submission

## Admin Panel Features

The admin panel includes:
- **Dashboard**: Overview of bookings, events, and revenue
- **Booking Management**: View and manage all bookings
- **Event Management**: Create and manage events
- **User Management**: Manage users and profiles
- **Payment Tracking**: Monitor payments and transactions
- **Review Moderation**: Approve/reject reviews
- **Staff Management**: Employee records and management

## API Endpoints

### Main URLs
- `/` - Home page
- `/rooms/` - Room listings
- `/events/` - Event listings
- `/facilities/` - Facility listings
- `/services/` - Service listings
- `/booking/` - Booking form
- `/contact/` - Contact page
- `/search/` - Search functionality

### User URLs
- `/register/` - User registration
- `/profile/` - User profile
- `/my-bookings/` - User booking history

### Booking URLs
- `/book-room/<id>/` - Book specific room
- `/book-event/<id>/` - Book specific event
- `/book-facility/<id>/` - Book specific facility

## Customization

### Adding New Room Types
1. Update `ROOM_TYPE_CHOICES` in `models.py`
2. Add corresponding admin filters
3. Update templates as needed

### Adding New Event Types
1. Update `EVENT_TYPE_CHOICES` in `models.py`
2. Add event type filters in admin
3. Update event templates

### Payment Integration
The system is ready for payment integration:
- M-Pesa integration
- Card payment processing
- Bank transfer handling
- Cash payment tracking

## Deployment

### Production Settings
1. Update `settings.py` for production:
   - Set `DEBUG = False`
   - Configure database
   - Set up email backend
   - Configure static files
   - Set up media files

2. Environment variables:
   - `SECRET_KEY`
   - `DATABASE_URL`
   - `EMAIL_HOST`
   - `EMAIL_HOST_PASSWORD`

### Database
- Default: SQLite (development)
- Production: PostgreSQL (recommended)
- MySQL support available

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Email: info@annsretreat.com
- Phone: +254 798 167 083

## Changelog

### Version 1.0.0
- Initial release
- Complete booking system
- Event management
- Facility booking
- User authentication
- Admin panel
- Payment tracking
- Review system

---

**ANN's Retreat Center** - Your peaceful getaway in Nairobi, Kenya
