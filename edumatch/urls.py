"""
URL configuration for edumatch project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin
from django.urls import path, include  # include is needed to include app URLs

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('matcher.urls')),  # include matcher app URLs under /api/
]
