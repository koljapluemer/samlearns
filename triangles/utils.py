from django.contrib.auth.models import User
from triangles.models import Topic, ClozeTemplate
import random


def get_random_topic() -> Topic:
    topics = Topic.objects.all()
    if not topics:
        return None
    return random.choice(topics)


def get_due_topic() -> Topic:
    return get_random_topic()


def get_due_gap_index_for_cloze_template(user: User, cloze_template: ClozeTemplate) -> int:
    # for now, ignore any user data, just get random one
    possible_gaps = cloze_template.possible_gap_indices
    if not possible_gaps:
        return 0
    return random.choice(possible_gaps)