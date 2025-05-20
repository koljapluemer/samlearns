from triangles.models import Topic, TopicProgress

def topic_progress(request):
    if not request.user.is_authenticated:
        return {'topics_with_progress': []}
    
    topics = Topic.objects.all()
    topics_with_progress = []
    
    for topic in topics:
        progress = TopicProgress.objects.filter(user=request.user, topic=topic).first()
        highest_streak = progress.highest_achieved_streak if progress else 0
        mastery_percentage = min(100, (highest_streak / 12) * 100)
        has_mastery = highest_streak >= 12
        
        topics_with_progress.append({
            'topic': topic,
            'highest_streak': highest_streak,
            'mastery_percentage': mastery_percentage,
            'has_mastery': has_mastery
        })
    
    return {'topics_with_progress': topics_with_progress} 