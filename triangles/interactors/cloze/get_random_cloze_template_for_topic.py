from triangles.models import ClozeTemplate, Topic

def get_random_cloze_template_for_topic(topic: Topic) -> ClozeTemplate:
    return ClozeTemplate.objects.filter(topic=topic).order_by('?').first()