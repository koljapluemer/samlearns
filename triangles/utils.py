from django.contrib.auth.models import User
from triangles.models import Distractor, Topic, ClozeTemplate
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


def get_all_lowercase_distractors() -> list[Distractor]:
    """Returns all distractors that start with a lowercase letter."""
    return list(Distractor.objects.filter(content__regex=r'^[a-zäöüß]'))


def get_all_uppercase_distractors() -> list[Distractor]:
    """Returns all distractors that start with an uppercase letter."""
    return list(Distractor.objects.filter(content__regex=r'^[A-ZÄÖÜ]'))


def get_random_relevant_distractor(correct_answer: str) -> Distractor:
    """
    Returns a random distractor that matches the case of the correct answer.
    Ensures the distractor is not the same as the correct answer.
    """
    # Determine if the correct answer starts with uppercase
    is_uppercase = correct_answer[0].isupper() if correct_answer else False
    
    # Get appropriate distractors based on case
    if is_uppercase:
        distractors = get_all_uppercase_distractors()
    else:
        distractors = get_all_lowercase_distractors()
    
    # Filter out the correct answer
    distractors = [d for d in distractors if d.content != correct_answer]
    
    # Return a random distractor if available
    return random.choice(distractors) if distractors else None