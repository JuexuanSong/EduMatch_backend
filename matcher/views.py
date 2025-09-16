from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .models import Match

User = get_user_model()

def get_matches(request):
    user_id = request.GET.get('user_id')
    if not user_id:
        return JsonResponse({"error": "user_id parameter is required"}, status=400)

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)

    # Get matches where user is either user1 or user2
    matches = Match.objects.filter(user1=user) | Match.objects.filter(user2=user)

    matches_data = []
    for match in matches:
        def serialize_user(u):
            profile = getattr(u, 'profile', None)
            return {
                "id": u.id,
                "username": u.username,
                "bio": profile.bio if profile and profile.bio else "",
                "image_url": profile.image_url if profile and profile.image_url else "",
                "can_teach": profile.can_teach if profile and profile.can_teach else [],
                "wanna_learn": profile.wanna_learn if profile and profile.wanna_learn else [],
            }

        matches_data.append({
            "id": match.id,
            "user1": serialize_user(match.user1),
            "user2": serialize_user(match.user2),
            "created_at": match.created_at.isoformat(),
        })

    return JsonResponse(matches_data, safe=False)
