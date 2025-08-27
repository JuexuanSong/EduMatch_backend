# users/serializers.py - Simple Version
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.gis.geos import Point
from .models import User, UserSkill

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        
        if email and password:
            user = authenticate(username=email, password=password)
            if user:
                if user.is_active:
                    data['user'] = user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Invalid credentials.')
        else:
            raise serializers.ValidationError('Must provide email and password.')
        
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    target_skills = serializers.SerializerMethodField()
    offer_skills = serializers.SerializerMethodField()
    longitude = serializers.FloatField(write_only=True, required=False)
    latitude = serializers.FloatField(write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['user_id', 'name', 'email', 'bio', 'image', 'campus', 
                 'longitude', 'latitude', 'target_skills', 'offer_skills', 
                 'profile_completed', 'member_since']
    
    def get_target_skills(self, obj):
        return [us.skill.name for us in obj.user_skills.filter(role='LEARN')]
    
    def get_offer_skills(self, obj):
        return [us.skill.name for us in obj.user_skills.filter(role='TEACH')]
    
    def update(self, instance, validated_data):
        longitude = validated_data.pop('longitude', None)
        latitude = validated_data.pop('latitude', None)
        
        if longitude is not None and latitude is not None:
            instance.location = Point(longitude, latitude, srid=4326)
        
        return super().update(instance, validated_data)