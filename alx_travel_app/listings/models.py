from django.db import models
from django.utils import timezone
import uuid
from django.contrib.auth.models import AbstractUser
from django.db.models.constraints import UniqueConstraint
# Create your models here.

'''Model representing a listing in the travel app.'''
class Listing(models.model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        constraints = [
            UniqueConstraint(fields=['created_at', 'updated_at'], name='unique_created_updated_price')
        ]

# Create your models here.
def __str__(self):
    """String representation of the Listing model."""
    return f"{self.title} - {self.price} - {'Active' if self.is_active else 'Inactive'}"

class Booking(models.Model):
    """Model representing a booking for a listing."""
    booking_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    property_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bookings')
    user_id = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='bookings')
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='listing_bookings')
    start_date = models.DateField()
    end_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['property_id','user_id', 'start_date', 'end_date'], name='unique_booking_dates')
        ]

        def __str__(self):
            return f"Booking {self.booking_id} for {self.property_id.title} by {self.user_id.username} from {self.start_date} to {self.end_date} - {self.status}"
        
