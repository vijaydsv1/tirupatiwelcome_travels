from django.contrib import admin
from .models import GalleryImage, Booking

class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_at')

class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'service', 'phone', 'status', 'created_at')
    list_filter = ('service', 'status')

admin.site.register(GalleryImage, GalleryImageAdmin)
admin.site.register(Booking, BookingAdmin)
