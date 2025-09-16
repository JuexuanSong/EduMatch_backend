from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Match, Profile

User = get_user_model()

class UserProfileSerializer(serializers.ModelSerializer):
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image_url = serializers.CharField(source='profile.image_url', read_only=True)
    can_teach = serializers.ListField(source='profile.can_teach', read_only=True)
    wanna_learn = serializers.ListField(source='profile.wanna_learn', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'bio', 'image_url', 'can_teach', 'wanna_learn']


class MatchSerializer(serializers.ModelSerializer):
    user1 = UserProfileSerializer(read_only=True)
    user2 = UserProfileSerializer(read_only=True)

    class Meta:
        model = Match
        fields = ['id', 'user1', 'user2', 'created_at']
