from triangles.models import Distractor


def get_all_lowercase_distractors() -> list[Distractor]:
    """Returns all distractors that start with a lowercase letter."""
    return list(Distractor.objects.filter(content__regex=r'^[a-zäöüß]'))
