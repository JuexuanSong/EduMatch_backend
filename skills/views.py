from rest_framework import generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Skill
from .serializers import SkillSerializer

class SkillListView(generics.ListAPIView):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticated]

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_skill(request):
    serializer = SkillSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)