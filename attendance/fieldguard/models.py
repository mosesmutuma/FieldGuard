from django.db import models
from django.contrib.auth.models import User

class AttendanceLog(models.Model):
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attendance_logs')
    timestamp = models.DateTimeField(auto_now_add=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    assigned_county = models.CharField(max_length=50, default='garissa')
    field_photo = models.ImageField(upload_to='field_verification_photos/')
    is_location_valid = models.BooleanField(default=False)
    verification_message = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.staff.username} - {self.timestamp}"

    def verify_location(self):
        lat, lng = float(self.latitude), float(self.longitude)
        county = self.assigned_county.lower()
        boundaries = {
            'garissa': (-2.50, 0.50, 39.00, 41.50),
            'wajir': (0.50, 3.50, 39.00, 41.00),
            'marsabit': (1.00, 4.50, 36.00, 39.50),
            'isiolo': (-0.50, 2.00, 36.50, 39.50),
            'mandera': (2.00, 4.30, 39.50, 41.90),
            'samburu': (0.50, 2.50, 36.20, 38.00)
        }
        if county not in boundaries: return False, "Out of system mapping operational zone."
        min_lat, max_lat, min_lng, max_lng = boundaries[county]
        if (min_lat <= lat <= max_lat) and (min_lng <= lng <= max_lng):
            return True, f"Verified inside {county.title()} sector bounds."
        return False, f"Coordinates mismatch outside designated operational zone."