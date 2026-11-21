from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'full_name', 'department', 'batch_year', 'is_available_for_mentorship']
    search_fields = ['user__email', 'full_name', 'department']
    list_filter = ['department', 'batch_year', 'is_available_for_mentorship']