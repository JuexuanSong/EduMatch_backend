from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from .models import User, UserSkill
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer
from skills.models import Skill

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if isinstance(user, list):
            user = user[0]  # Take the first user if a list is returned
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'user_id': getattr(user, 'user_id', getattr(user, 'id', None)),
            'name': getattr(user, 'name', ''),
            'email': getattr(user, 'email', ''),
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        validated_data = getattr(serializer, 'validated_data', {})
        user = validated_data.get('user') if isinstance(validated_data, dict) else None
        if not user:
            return Response({'error': 'Invalid credentials or user not found.'}, status=status.HTTP_400_BAD_REQUEST)
        token, created = Token.objects.get_or_create(user=user)
        
        # Update last active
        from django.utils import timezone
        user.last_active = timezone.now()
        user.save()
        
        return Response({
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email,
            'token': token.key
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        request.user.auth_token.delete()
        return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
    except:
        return Response({'error': 'Error logging out'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
        
        # Generate password reset token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # Send email
        current_site = get_current_site(request)
        subject = 'Password Reset Request'
        message = f"""
        Hello {user.name},
        
        You requested a password reset. Click the link below to reset your password:
        http://{current_site.domain}/reset-password/{uid}/{token}/
        
        If you didn't request this, please ignore this email.
        """
        
        send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
        
        return Response({'message': 'Password reset email sent'}, status=status.HTTP_200_OK)
    except User.DoesNotExist:
        return Response({'error': 'User with this email does not exist'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def update_skills(request):
    user = request.user
    target_skills = request.data.get('target_skills', [])
    offer_skills = request.data.get('offer_skills', [])
    
    # Clear existing skills
    UserSkill.objects.filter(user=user).delete()
    
    # Add target skills (LEARN)
    for skill_name in target_skills:
        skill, created = Skill.objects.get_or_create(name=skill_name)
        UserSkill.objects.create(user=user, skill=skill, role='LEARN')
    
    # Add offer skills (TEACH)
    for skill_name in offer_skills:
        skill, created = Skill.objects.get_or_create(name=skill_name)
        UserSkill.objects.create(user=user, skill=skill, role='TEACH')
    
    return Response({'message': 'Skills updated successfully'}, status=status.HTTP_200_OK)
