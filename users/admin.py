from django.contrib import admin
from .models import UserProfile, PerformanceType

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'get_performance_types', 'created_at')
    search_fields = ('user__username', 'user__email', 'phone')

    def get_performance_types(self, obj):
        return ", ".join([str(t) for t in obj.preferred_performance_types.all()])
    get_performance_types.short_description = "Жанри"

@admin.register(PerformanceType)
class PerformanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
