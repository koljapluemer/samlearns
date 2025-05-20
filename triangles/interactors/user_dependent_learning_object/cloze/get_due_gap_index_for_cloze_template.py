import random

from django.contrib.auth.models import User

from triangles.models import ClozeTemplate


def get_due_gap_index_for_cloze_template(user: User, cloze_template: ClozeTemplate) -> int:
    # for now, ignore any user data, just get random one
    possible_gaps = cloze_template.possible_gap_indices
    if not possible_gaps:
        return 0
    return random.choice(possible_gaps)


