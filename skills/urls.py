from django.urls import path
from . import views

urlpatterns = [
    path('', views.SkillListView.as_view(), name='skill_list'),
    path('create/', views.create_skill, name='create_skill'),
]