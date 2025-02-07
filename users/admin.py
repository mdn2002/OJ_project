from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'role', 'display_name', 'affiliation', 'is_active')
    list_filter = ('role', 'is_active')
    search_fields = ('username', 'team_name', 'display_name')

