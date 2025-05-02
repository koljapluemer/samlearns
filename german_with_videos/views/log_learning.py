from rest_framework import serializers, views
from rest_framework.response import Response
from german_with_videos.models import WordLearningEvent
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

class WordLearningEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordLearningEvent
        fields = ['anon_id', 'original_word_string', 'selected_button', 'snippet_identifier']

class BatchWordLearningEventView(views.APIView):
    def post(self, request):
        try:
            events = request.data.get('events', [])
            logger.info(f"Received {len(events)} learning events")
            
            serializer = WordLearningEventSerializer(data=events, many=True)
            
            if serializer.is_valid():
                serializer.save()
                logger.info("Successfully saved learning events")
                return Response({'status': 'success', 'saved_count': len(events)})
            
            logger.error(f"Validation errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
            
        except Exception as e:
            logger.error(f"Error processing learning events: {str(e)}")
            return Response({'error': str(e)}, status=500)
