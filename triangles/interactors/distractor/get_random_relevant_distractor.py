import random
from triangles.interactors.distractor import get_all_uppercase_distractors
from triangles.interactors.distractor import get_all_lowercase_distractors
from triangles.models import Distractor


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