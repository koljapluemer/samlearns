from django.contrib import admin

from .models import Distractor, Topic, ClozeTemplate, ImageExerciseTemplate, TopicProgress, ClozeTemplateGapProgress, ImageExerciseProgress, LearningEvent

admin.site.register(Topic)  
admin.site.register(ClozeTemplate)
admin.site.register(ImageExerciseTemplate)
admin.site.register(TopicProgress)
admin.site.register(ClozeTemplateGapProgress)
admin.site.register(ImageExerciseProgress)
admin.site.register(LearningEvent)
admin.site.register(Distractor)