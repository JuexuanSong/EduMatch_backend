# users/admin.py - Fixed Version
from django.contrib import admin
from django.contrib.gis.admin import GISModelAdmin  # Use GISModelAdmin instead of OSMGeoAdmin
from .models import User, UserSkill

@admin.register(User)
class UserAdmin(GISModelAdmin):  # Changed from OSMGeoAdmin to GISModelAdmin
    list_display = ['name', 'email', 'campus', 'member_since', 'profile_completed']
    search_fields = ['name', 'email']
    list_filter = ['campus', 'member_since', 'profile_completed', 'is_active']
    readonly_fields = ['user_id', 'member_since', 'last_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'email', 'bio', 'image')
        }),
        ('Location', {
            'fields': ('location', 'longitude', 'latitude', 'campus')
        }),
        ('Status', {
            'fields': ('is_active', 'profile_completed', 'last_active', 'member_since')
        }),
        ('System', {
            'fields': ('user_id',)
        }),
    )

@admin.register(UserSkill)
class UserSkillAdmin(admin.ModelAdmin):
    list_display = ['user', 'skill', 'role', 'proficiency', 'created_at']
    list_filter = ['role', 'proficiency', 'created_at']
    search_fields = ['user__name', 'skill__name']
    autocomplete_fields = ['user', 'skill']