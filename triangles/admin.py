from django.contrib import admin

from .models import Distractor, Topic, ClozeTemplate, ImageExerciseTemplate, TopicProgress, ClozeTemplateGapProgress, ImageExerciseProgress, LearningEvent

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_congruence_theorem')
    list_filter = ('is_congruence_theorem',)
    search_fields = ('name',)

@admin.register(ClozeTemplate)
class ClozeTemplateAdmin(admin.ModelAdmin):
    list_display = ('topic', 'content_preview')
    list_filter = ('topic',)
    search_fields = ('content', 'topic__name')

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(ImageExerciseTemplate)
class ImageExerciseTemplateAdmin(admin.ModelAdmin):
    list_display = ('topic', 'prompt_preview')
    list_filter = ('topic',)
    search_fields = ('prompt', 'topic__name')

    def prompt_preview(self, obj):
        return obj.prompt[:100] + '...' if len(obj.prompt) > 100 else obj.prompt
    prompt_preview.short_description = 'Prompt Preview'

@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'streak')
    list_filter = ('topic', 'user')
    search_fields = ('user__username', 'topic__name')

@admin.register(ClozeTemplateGapProgress)
class ClozeTemplateGapProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'gap_index', 'streak')
    list_filter = ('template__topic', 'user')
    search_fields = ('user__username', 'template__topic__name')

@admin.register(ImageExerciseProgress)
class ImageExerciseProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'template', 'streak')
    list_filter = ('template__topic', 'user')
    search_fields = ('user__username', 'template__topic__name')

@admin.register(Distractor)
class DistractorAdmin(admin.ModelAdmin):
    list_display = ('content_preview',)
    search_fields = ('content',)

    def content_preview(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    content_preview.short_description = 'Content Preview'

@admin.register(LearningEvent)
class LearningEventAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'timestamp', 'streak_before_answer', 'answer_given')
    list_filter = ('topic', 'user', 'timestamp')
    search_fields = ('user__username', 'topic__name', 'answer_given')
    date_hierarchy = 'timestamp'
