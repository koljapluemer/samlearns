from django.core.management.base import BaseCommand
from triangles.models import ClozeTemplate, Distractor
import string

class Command(BaseCommand):
    help = 'Generates distractors for all Cloze templates based on their gap indices'

    def add_arguments(self, parser):
        parser.add_argument(
            '--purge',
            action='store_true',
            help='Delete all existing distractors before generating new ones',
        )

    def handle(self, *args, **options):
        if options['purge']:
            self.stdout.write("Purging all existing distractors...")
            Distractor.objects.all().delete()
            self.stdout.write(self.style.SUCCESS("Successfully purged all distractors"))

        # Get all Cloze templates
        cloze_templates = ClozeTemplate.objects.all()
        
        for template in cloze_templates:
            self.stdout.write(f"Processing template: {template}")
            
            # Get the content and split it into words
            content = template.content
            words = content.split()
            
            # Get the gap indices
            gap_indices = template.possible_gap_indices
            
            for gap_index in gap_indices:
                if gap_index < len(words):
                    # Get the word at this gap and clean it
                    word = words[gap_index].strip(string.punctuation + string.whitespace)
                    
                    # Create Distractor object
                    Distractor.objects.get_or_create(content=word)
                    self.stdout.write(f"Created distractor: {word}")
                else:
                    self.stdout.write(self.style.WARNING(f"Gap index {gap_index} is out of range for template {template}")) 