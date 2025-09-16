def is_match(user_a, user_b, max_distance_km=30):
    if not are_nearby(user_a, user_b, max_distance_km):
        return False

    a_wants = set(user_a['wannaLearn'])
    a_teaches = set(user_a['canTeach'])
    b_wants = set(user_b['wannaLearn'])
    b_teaches = set(user_b['canTeach'])

    return bool((a_teaches & b_wants) or (b_teaches & a_wants))
