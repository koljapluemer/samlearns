from django.db import models
from django.conf import settings

class Topic(models.Model):
    name = models.CharField(max_length=255)
    is_congruence_theorem = models.BooleanField(default=False, help_text="If True, this topic represents a triangle congruence theorem (SSS, SSW, SWS, or WSW)")

    def __str__(self):
        return self.name

    def get_streak(self, user):
        """
        Get the current streak for this topic for the given user.
        Returns 0 if no progress exists.
        """
        try:
            progress = self.user_progress.get(user=user)
            return progress.streak
        except TopicProgress.DoesNotExist:
            return 0

class ClozeTemplate(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='cloze_templates')
    content = models.TextField()
    possible_gap_indices = models.JSONField(help_text="List of indices where gaps can be placed")

    def __str__(self):
        return f"Cloze for {self.topic.name}"

    def get_gap_at_index(self, gap_index: int) -> str:
        """
        Returns the word at the given gap index.
        The gap_index is the index in the list of words where the gap should be.
        """
        words = self.content.split()
        if gap_index >= len(words):
            raise ValueError(f"Gap index {gap_index} is out of range for template {self}")
        return words[gap_index]

class ImageExerciseTemplate(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='image_exercises')
    prompt = models.TextField()

    def __str__(self):
        return f"Image exercise for {self.topic.name}"

class TopicProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='user_progress')
    streak = models.PositiveIntegerField(default=1)
    highest_achieved_streak = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username}'s progress in {self.topic.name}"

class ClozeTemplateGapProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cloze_progress')
    template = models.ForeignKey(ClozeTemplate, on_delete=models.CASCADE, related_name='user_progress')
    gap_index = models.PositiveIntegerField()
    streak = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ['user', 'template', 'gap_index']

    def __str__(self):
        return f"{self.user.username}'s progress in {self.template} gap {self.gap_index}"


class Distractor(models.Model):
    content = models.TextField()
    
    class Meta:
        unique_together = ['content']

    def __str__(self):
        return self.content

class LearningEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='learning_events')
    timestamp = models.DateTimeField(auto_now_add=True)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='learning_events')
    exercise_type = models.CharField(max_length=255, help_text="The type of exercise that was completed")
    cloze_template = models.ForeignKey(
        ClozeTemplate, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='learning_events'
    )
    streak_before_answer = models.PositiveIntegerField(default=0)
    possible_answers = models.JSONField(help_text="List of possible answers for the exercise")
    answer_given = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username}'s learning event in {self.topic.name} at {self.timestamp}"