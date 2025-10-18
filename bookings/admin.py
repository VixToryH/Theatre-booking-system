from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'show', 'seat', 'status', 'price_paid', 'created_at')
    list_filter = ('status', 'show')
    search_fields = ('user__username', 'user__email')

