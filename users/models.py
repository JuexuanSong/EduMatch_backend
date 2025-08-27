# users/models.py - Fixed with Properly Typed Custom UserManager
import uuid
from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.gis.geos import Point
from typing import Any, Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from django.contrib.auth.models import UserManager as BaseUserManagerType
else:
    BaseUserManagerType = BaseUserManager

class UserManager(BaseUserManagerType):
    """Custom user manager for email-based authentication"""
    
    def create_user(self, email: str, name: str, password: Optional[str] = None, **extra_fields: Any) -> 'User':
        """Create and return a regular user with an email and password"""
        if not email:
            raise ValueError('The Email field must be set')
        if not name:
            raise ValueError('The Name field must be set')
            
        email = self.normalize_email(email)
        
        # Remove username from extra_fields if it exists to avoid conflict
        extra_fields.pop('username', None)
        
        user = self.model(
            email=email,
            name=name,
            username=email,  # Set username to email for compatibility
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email: str, name: str, password: Optional[str] = None, **extra_fields: Any) -> 'User':
        """Create and return a superuser with an email and password"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
            
        return self.create_user(email, name, password, **extra_fields)

class User(AbstractUser):
    CAMPUS_CHOICES = [
        ('Arlington', 'Arlington'),
        ('Boston', 'Boston'),
        ('Burlington', 'Burlington'),
        ('Charlotte', 'Charlotte'),
        ('London', 'London'),
        ('Miami', 'Miami'),
        ('Oakland', 'Oakland'),
        ('Portland', 'Portland'),
        ('Seattle', 'Seattle'),
        ('Silicon Valley', 'Silicon Valley'),
        ('Toronto', 'Toronto'),
        ('Vancouver', 'Vancouver'),
    ]
    
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    location = models.PointField(blank=True, null=True, srid=4326)
    campus = models.CharField(max_length=20, choices=CAMPUS_CHOICES, blank=True, null=True)
    last_active = models.DateTimeField(blank=True, null=True)
    member_since = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    profile_completed = models.BooleanField(default=False)

    # Use custom manager
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    
    def __str__(self):
        return self.name or self.email
    
    @property
    def longitude(self):
        return self.location.x if self.location else None
    
    @property
    def latitude(self):
        return self.location.y if self.location else None

class UserSkill(models.Model):
    ROLE_CHOICES = [
        ('TEACH', 'Teach'),
        ('LEARN', 'Learn'),
    ]
    
    PROFICIENCY_CHOICES = [
        ('BEGINNER', 'Beginner'),
        ('INTERMEDIATE', 'Intermediate'),
        ('ADVANCED', 'Advanced'),
    ]
    
    user_skill_id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_skills')
    skill = models.ForeignKey('skills.Skill', on_delete=models.CASCADE, related_name='user_skills')
    role = models.CharField(max_length=5, choices=ROLE_CHOICES)
    proficiency = models.CharField(max_length=12, choices=PROFICIENCY_CHOICES, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'skill', 'role']
    
    def __str__(self):
        return f"{self.user.name} - {self.skill.name} ({self.role})"
