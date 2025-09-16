from .models import Match

def create_match(user1, user2):
    if user1.id > user2.id:
        user1, user2 = user2, user1
    return Match.objects.create(user1=user1, user2=user2)
