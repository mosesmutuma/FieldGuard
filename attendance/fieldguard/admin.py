from django.contrib import admin
from django.utils.html import format_html
from .models import AttendanceLog

@admin.register(AttendanceLog)
class AttendanceLogAdmin(admin.ModelAdmin):
    list_display = ('staff', 'timestamp', 'assigned_county', 'is_location_valid', 'view_on_map')
    list_filter = ('is_location_valid', 'assigned_county', 'timestamp', 'staff')
    readonly_fields = ('staff', 'timestamp', 'latitude', 'longitude', 'assigned_county', 'field_photo', 'is_location_valid', 'verification_message')

    def view_on_map(self, obj):
        url = f"https://www.google.com/maps?q={obj.latitude},{obj.longitude}"
        return format_html(f'<a href="{url}" target="_blank" style="color: #026aa7; font-weight: bold;">🗺️ Locate on Google Maps</a>')
    
    view_on_map.short_description = "Map Verification Link"