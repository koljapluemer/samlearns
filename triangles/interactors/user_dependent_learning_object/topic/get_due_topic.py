
from triangles.interactors.topic import get_random_topic
from triangles.models import Topic
from django.contrib.auth.models import User

# for this minimal implementation, we actually ignore any user data
# and just return a random topic
def get_due_topic(user: User) -> Topic:
    return get_random_topic()