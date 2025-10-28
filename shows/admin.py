from django.contrib import admin
from .models import Theater, Seat, Show

@admin.register(Theater)
class TheaterAdmin(admin.ModelAdmin):
    list_display = ('name', 'address')
    search_fields = ('name', 'address')


@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('row', 'number', 'is_vip', 'price')
    list_filter = ('is_vip',)
    search_fields = ('row', 'number')


@admin.register(Show)
class ShowAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'time', 'status')
    list_filter = ('status', 'date')
    search_fields = ('title', 'description')
    ordering = ('-date', '-time')
    filter_horizontal = ('genres',)
