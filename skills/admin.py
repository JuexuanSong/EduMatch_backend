# skills/admin.py - Enhanced Version
from django.contrib import admin
from .models import Skill

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'is_trending', 'created_at']
    search_fields = ['name', 'category']
    list_filter = ['category', 'is_trending', 'created_at']
    ordering = ['name']