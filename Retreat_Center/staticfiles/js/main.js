// Main JavaScript for ARC Retreat Center

$(document).ready(function() {
    // Initialize WOW animations
    if (typeof WOW !== 'undefined') {
        new WOW().init();
    }
    
    // Initialize Owl Carousel for testimonials
    if ($('.testimonial-carousel').length) {
        $('.testimonial-carousel').owlCarousel({
            loop: true,
            margin: 10,
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1,
                    nav: false
                },
                600: {
                    items: 1,
                    nav: false
                },
                1000: {
                    items: 1,
                    nav: false,
                    loop: true
                }
            }
        });
    }
    
    // Initialize date pickers
    if ($('.datetimepicker-input').length) {
        $('.datetimepicker-input').datetimepicker({
            format: 'YYYY-MM-DD',
            minDate: moment()
        });
    }
    
    // Back to top button
    $(window).scroll(function() {
        if ($(this).scrollTop() > 100) {
            $('.back-to-top').fadeIn();
        } else {
            $('.back-to-top').fadeOut();
        }
    });
    
    $('.back-to-top').click(function() {
        $('html, body').animate({scrollTop: 0}, 1000);
        return false;
    });
    
    // Counter animation
    if ($('.counter').length) {
        $('.counter').counterUp({
            delay: 10,
            time: 1000
        });
    }
    
    // Smooth scrolling for anchor links
    $('a[href*="#"]:not([href="#"])').click(function() {
        if (location.pathname.replace(/^\//, '') == this.pathname.replace(/^\//, '') && location.hostname == this.hostname) {
            var target = $(this.hash);
            target = target.length ? target : $('[name=' + this.hash.slice(1) + ']');
            if (target.length) {
                $('html, body').animate({
                    scrollTop: target.offset().top - 100
                }, 1000);
                return false;
            }
        }
    });
});

// ===== NOTIFICATION SYSTEM =====
class NotificationSystem {
    constructor() {
        this.createNotificationContainer();
        this.bindEvents();
    }

    createNotificationContainer() {
        // Create notification container if it doesn't exist
        if (!document.getElementById('notification-container')) {
            const container = document.createElement('div');
            container.id = 'notification-container';
            container.style.cssText = `
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
                max-width: 400px;
            `;
            document.body.appendChild(container);
        }
    }

    show(message, type = 'success', duration = 5000) {
        const container = document.getElementById('notification-container');
        const notification = document.createElement('div');
        
        // Generate unique ID
        const id = 'notification-' + Date.now();
        notification.id = id;
        
        // Set notification styles based on type
        const styles = this.getNotificationStyles(type);
        notification.style.cssText = styles;
        
        // Create notification content
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-icon">
                    ${this.getIcon(type)}
                </div>
                <div class="notification-message">
                    <strong>${this.getTitle(type)}</strong>
                    <p>${message}</p>
                </div>
                <button class="notification-close" onclick="this.parentElement.parentElement.remove()">
                    <i class="fa fa-times"></i>
                </button>
            </div>
        `;
        
        // Add animation classes
        notification.classList.add('notification', 'notification-' + type, 'notification-enter');
        
        // Insert at the beginning of container
        container.insertBefore(notification, container.firstChild);
        
        // Trigger enter animation
        setTimeout(() => {
            notification.classList.remove('notification-enter');
            notification.classList.add('notification-show');
        }, 10);
        
        // Auto remove after duration
        setTimeout(() => {
            this.remove(id);
        }, duration);
        
        return id;
    }

    remove(id) {
        const notification = document.getElementById(id);
        if (notification) {
            notification.classList.add('notification-exit');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }
    }

    getNotificationStyles(type) {
        const baseStyles = `
            margin-bottom: 10px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            overflow: hidden;
            transform: translateX(100%);
            opacity: 0;
            transition: all 0.3s ease;
        `;

        const typeStyles = {
            success: `
                background: linear-gradient(135deg, #28a745, #20c997);
                color: white;
                border-left: 4px solid #1e7e34;
            `,
            error: `
                background: linear-gradient(135deg, #dc3545, #e74c3c);
                color: white;
                border-left: 4px solid #bd2130;
            `,
            warning: `
                background: linear-gradient(135deg, #ffc107, #ffb300);
                color: #212529;
                border-left: 4px solid #e0a800;
            `,
            info: `
                background: linear-gradient(135deg, #17a2b8, #20c997);
                color: white;
                border-left: 4px solid #138496;
            `
        };

        return baseStyles + typeStyles[type] || typeStyles.info;
    }

    getIcon(type) {
        const icons = {
            success: '<i class="fa fa-check-circle"></i>',
            error: '<i class="fa fa-exclamation-circle"></i>',
            warning: '<i class="fa fa-exclamation-triangle"></i>',
            info: '<i class="fa fa-info-circle"></i>'
        };
        return icons[type] || icons.info;
    }

    getTitle(type) {
        const titles = {
            success: 'Success!',
            error: 'Error!',
            warning: 'Warning!',
            info: 'Information'
        };
        return titles[type] || titles.info;
    }

    bindEvents() {
        // Listen for custom events
        document.addEventListener('bookingSuccess', (e) => {
            this.show('Your booking has been confirmed successfully!', 'success', 6000);
        });

        document.addEventListener('bookingError', (e) => {
            this.show('There was an error processing your booking. Please try again.', 'error', 6000);
        });

        document.addEventListener('serviceBooked', (e) => {
            this.show('Service has been booked successfully!', 'success', 5000);
        });

        document.addEventListener('profileUpdated', (e) => {
            this.show('Your profile has been updated successfully!', 'success', 4000);
        });

        document.addEventListener('reviewSubmitted', (e) => {
            this.show('Thank you for your review! It will be published after approval.', 'info', 5000);
        });

        document.addEventListener('newsletterSubscribed', (e) => {
            this.show('You have been subscribed to our newsletter!', 'success', 4000);
        });
    }
}

// Initialize notification system
const notifications = new NotificationSystem();

// ===== DJANGO MESSAGES HANDLER =====
$(document).ready(function() {
    // Handle Django messages
    const djangoMessages = document.getElementById('django-messages');
    if (djangoMessages) {
        const messageElements = djangoMessages.querySelectorAll('div[data-level]');
        messageElements.forEach(element => {
            const level = element.getAttribute('data-level');
            const message = element.getAttribute('data-message');
            
            // Map Django message levels to notification types
            let notificationType = 'info';
            switch(level) {
                case 'success':
                    notificationType = 'success';
                    break;
                case 'error':
                case 'danger':
                    notificationType = 'error';
                    break;
                case 'warning':
                    notificationType = 'warning';
                    break;
                case 'info':
                case 'debug':
                    notificationType = 'info';
                    break;
            }
            
            // Show notification
            notifications.show(message, notificationType, 6000);
        });
        
        // Remove the Django messages container
        djangoMessages.remove();
    }
});

// ===== FORM SUBMISSION HANDLERS =====
$(document).ready(function() {
    // Handle booking forms
    $('form[action*="book"]').on('submit', function(e) {
        const submitBtn = $(this).find('button[type="submit"]');
        if (submitBtn.length) {
            submitBtn.html('<i class="fa fa-spinner fa-spin"></i> Processing...');
            submitBtn.prop('disabled', true);
        }
    });

    // Handle service booking
    $('form[action*="book-service"]').on('submit', function(e) {
        setTimeout(() => {
            notifications.show('Service booking request submitted successfully!', 'success', 5000);
        }, 1000);
    });

    // Handle facility booking
    $('form[action*="book-facility"]').on('submit', function(e) {
        setTimeout(() => {
            notifications.show('Facility booking request submitted successfully!', 'success', 5000);
        }, 1000);
    });

    // Handle profile updates
    $('form[action*="profile"]').on('submit', function(e) {
        setTimeout(() => {
            notifications.show('Profile updated successfully!', 'success', 4000);
        }, 1000);
    });

    // Handle review submissions
    $('form[action*="add-review"]').on('submit', function(e) {
        setTimeout(() => {
            notifications.show('Review submitted successfully! Thank you for your feedback.', 'success', 5000);
        }, 1000);
    });

    // Handle newsletter subscription
    $('form[action*="subscribe"]').on('submit', function(e) {
        setTimeout(() => {
            notifications.show('Successfully subscribed to newsletter!', 'success', 4000);
        }, 1000);
    });
});

// ===== CSS ANIMATIONS =====
const style = document.createElement('style');
style.textContent = `
    .notification {
        position: relative;
        margin-bottom: 10px;
    }

    .notification-content {
        display: flex;
        align-items: flex-start;
        padding: 15px;
        position: relative;
    }

    .notification-icon {
        font-size: 20px;
        margin-right: 12px;
        margin-top: 2px;
        flex-shrink: 0;
    }

    .notification-message {
        flex: 1;
    }

    .notification-message strong {
        display: block;
        margin-bottom: 4px;
        font-size: 14px;
    }

    .notification-message p {
        margin: 0;
        font-size: 13px;
        line-height: 1.4;
    }

    .notification-close {
        position: absolute;
        top: 8px;
        right: 8px;
        background: none;
        border: none;
        color: inherit;
        cursor: pointer;
        font-size: 12px;
        opacity: 0.7;
        transition: opacity 0.2s;
    }

    .notification-close:hover {
        opacity: 1;
    }

    .notification-enter {
        transform: translateX(100%);
        opacity: 0;
    }

    .notification-show {
        transform: translateX(0);
        opacity: 1;
    }

    .notification-exit {
        transform: translateX(100%);
        opacity: 0;
    }

    /* Success notification specific styles */
    .notification-success .notification-icon {
        color: rgba(255, 255, 255, 0.9);
    }

    /* Error notification specific styles */
    .notification-error .notification-icon {
        color: rgba(255, 255, 255, 0.9);
    }

    /* Warning notification specific styles */
    .notification-warning .notification-icon {
        color: rgba(33, 37, 41, 0.8);
    }

    /* Info notification specific styles */
    .notification-info .notification-icon {
        color: rgba(255, 255, 255, 0.9);
    }
`;
document.head.appendChild(style);