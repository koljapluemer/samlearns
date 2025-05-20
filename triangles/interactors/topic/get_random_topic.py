import random

from triangles.models import Topic


def get_random_topic() -> Topic:
    topics = Topic.objects.all()
    if not topics:
        return None
    return random.choice(topics)

