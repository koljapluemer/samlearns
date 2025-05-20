from triangles.models import Distractor


def get_all_uppercase_distractors() -> list[Distractor]:
    """Returns all distractors that start with an uppercase letter."""
    return list(Distractor.objects.filter(content__regex=r'^[A-ZÄÖÜ]'))


