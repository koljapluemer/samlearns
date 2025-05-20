from django.contrib.auth.models import User
from triangles.models import Topic


# later, make this dependent on the topic streak for the user
def user_should_get_image_instead_of_cloze_exercise(user: User, topic: Topic) -> bool:
    return False
